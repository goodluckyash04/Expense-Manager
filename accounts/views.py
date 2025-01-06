import traceback
from datetime import datetime,timedelta

from django.db.models import Q,Sum,Case, When, Value, CharField
from dateutil.relativedelta import relativedelta
from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseServerError
from django.utils.crypto import get_random_string
from .models import User, LedgerTransaction, Transaction
from .decorators import auth_user
from decimal import Decimal
from django.utils import timezone


# ...........................................About..................................................

@auth_user
def about(request,user):
    return render(request,"about.html",{"user":user})



# ...........................................Dashboard..................................................


@auth_user
def dashboard(request,user):
    try:
        transactions = Transaction.objects.filter(created_by=user,is_deleted = False)
        income = sum(entry.amount for entry in transactions if entry.type.lower() == 'income'and not entry.is_deleted)
        expense = sum(entry.amount for entry in transactions if entry.type.lower() == 'expense' and entry.date <= datetime.now().date())
        investment = sum(entry.amount for entry in transactions if entry.category.lower() == 'investment' and entry.date <= datetime.now().date())
        overdue = sum(entry.amount for entry in transactions if entry.category.lower() == 'emi'and entry.status.lower()=="pending")
        
        #---------------------- Financial Overview ----------------------------
        context = {}
        max_amount = max([income, expense, income-expense, investment, overdue])

        context["finance_view"] =  {
                "labels": ["Income", "Expense", "Savings", "Investments", "Overdue"],
                "data": [income, expense, income-expense, investment, overdue],
                "max": round(max_amount + max_amount/10) 
            }
        
        #---------------------- Category wise Expense ----------------------------
        category_wise_data = {}
        for txn in [entry for entry in transactions if entry.type.lower() == 'expense' and entry.date <= datetime.now().date() ]:
            if txn.category in category_wise_data:
                category_wise_data[txn.category] += txn.amount 
            else:
                category_wise_data[txn.category] = txn.amount 
        context['category_wise_data'] = category_wise_data

        #--------------------- Monthly savings of last 12 month ----------------------

        # Current date and time
        current_date = timezone.now()
        current_year = current_date.year
        current_month = current_date.month

        # Calculate the last 12 months, handling year transitions correctly
        last_12_months = [(current_date - relativedelta(months=i)).month for i in range(12)]
        last_12_months_years = [
            (current_date - relativedelta(months=i)).year for i in range(12)
        ]

        # Query transactions for the last 12 months
        transactions = Transaction.objects.filter(
            created_by=user,
            is_deleted=False,
            date__year__in=last_12_months_years,
            date__month__in=last_12_months,
        ).values('date__year', 'date__month').annotate(
            total_expense=Sum('amount', filter=Q(type='Expense')),
            total_income=Sum('amount', filter=Q(type='Income'))
        )

        # Prepare the savings data with formatted labels like Jan'24
        savings_data = {}
        for i in range(12):
            month = last_12_months[i]
            year = last_12_months_years[i]

            # Find the corresponding transaction for the month and year
            month_data = next(
                (transaction for transaction in transactions 
                if transaction['date__month'] == month and transaction['date__year'] == year), 
                {}
            )
            total_expense = month_data.get('total_expense') or 0
            total_income = month_data.get('total_income') or 0

            savings = total_income - total_expense
            label = datetime(year, month, 1).strftime("%b'%y")  # Format as Jan'24
            savings_data[label] = float(savings)

        context["savings"] = savings_data


        #---------------------------------- Year wise Income Expense -----------------------
        transactions = Transaction.objects.filter(
            created_by=user,
            is_deleted=False,
            date__month__lte=current_month,
            date__year__lte=current_year,
        ).values('date__year').annotate(
            total_expense=Sum('amount', filter=Q(type='Expense')),
            total_income=Sum('amount', filter=Q(type='Income'))
        )
        year_wise_data = {} 
        year_wise_data['income'] = [i['total_income'] for i in transactions]
        year_wise_data['expense'] = [i['total_expense'] for i in transactions]
        year_wise_data['label'] = [i['date__year'] for i in transactions]

        context['year_wise_data'] = year_wise_data

        # -----------------------current month category wise expense---------------------
        category_wise = {}

        category_expenses = Transaction.objects.filter(
            created_by=user,
            is_deleted=False,
            date__month=current_month,
            date__year=current_year,
            type='Expense'
        ).values('category').annotate(
            amount=Sum('amount')
        )

        total = Transaction.objects.filter(
            created_by=user,
            is_deleted=False,
            date__month=current_month,
            date__year=current_year,
        ).values('type').annotate(
            amount=Sum('amount')
        )

        category_wise['labels'] = [i['category'] for i in category_expenses]
        category_wise['amount'] = [i['amount'] for i in category_expenses]

        income_total = next((item['amount'] for item in total if item['type'] == 'Income'), 0)
        expense_total = next((item['amount'] for item in total if item['type'] == 'Expense'), 0)

        category_wise['labels'].append('Balance')
        category_wise['amount'].append(income_total - expense_total)

        context["category_wise_month"] = category_wise

        import json
        def convert_decimal(obj):
            if isinstance(obj, Decimal):
                return float(obj)  # Convert Decimal to float (or str(obj) for string)
            return obj
        context = {'data': json.dumps(context,default=convert_decimal),'user':user}

        return render(request,'dashboard.html',context=context)
    except Exception as e:
        messages.error(request, "An unexpected error occurred.")
        # Log the error for debugging purposes
        print(str(e))
        return HttpResponseServerError()

# ...........................................Home Page..................................................

@auth_user
def home(request,user):
    try:
        items = [
            {
                "title": "TRANSACTION",
                "description": "Maintain Your Day to Day Transaction",
                "modal_target": "#expensemodal",
                "modal_button_icon": 'fa-plus',
                "report_url": "/transaction-detail/",
                "report_button_icon":  datetime.today().strftime("%b'%y").upper(),
                "delete_url": "/deleted-transaction-detail/",
                "delete_button_icon": 'fa-trash-can',
                "class_suffix": " mb-3 mb-sm-0"

            },
            {
                "title": "TASK",
                "description": "Don't Stress Your Brain Add Your Todos",
                "modal_target": "#taskmodal",
                "modal_button_icon": 'fa-plus',
                "report_url": "/currentMonthTaskReport/",
                "report_button_icon": datetime.today().strftime("%b'%y").upper(),
                "delete_url": "/taskReports/",
                "delete_button_icon": 'fa-square-poll-horizontal',
                "class_suffix": " mb-3"
            },
            {
                "title": "FINANCE",
                "description": "Keep track of Your Virtual Loan/Sip ",
                "modal_target": "#financeModal",
                "modal_button_icon": 'fa-plus',
                "report_url": "/finance-details/",
                "report_button_icon": 'fa-square-poll-horizontal',
                # "delete_url": "/deletedEntries/",
                # "delete_button_icon": 'fa-trash-can',
                # "class_suffix": ""
            },
            {
                "title": "LEDGER",
                "description": "Keep track of your Payable and Receivables",
                "modal_target": "#ledgerModal",
                "modal_button_icon": 'fa-plus',
                "report_url": "/ledger-transaction-details/",
                "report_button_icon": 'fa-square-poll-horizontal',
                "delete_url": "/deleted-ledger-transaction/",
                "delete_button_icon": 'fa-trash-can',
                "class_suffix": ""
            },
             {
                "title": "REMINDER",
                "description": "Don't remember special days, stop worrying! Let the reminders handle it",
                "modal_target": "#taskmodal",
                "modal_button_icon": 'fa-plus',
                "report_url": "/view-today-reminder/",
                "report_button_icon": datetime.today().strftime("%b'%y").upper(),
                "delete_url": "/taskReports/",
                "delete_button_icon": 'fa-square-poll-horizontal',
                "class_suffix": ""
            },
        ]
        counterparties = LedgerTransaction.objects.filter(created_by=user).values_list('counterparty', flat=True).distinct()
        return render(request,"home.html",{"user":user,'items': items, "counterparties":counterparties})
    except Exception as e:
        messages.error(request, "An unexpected error occurred.")
        # Log the error for debugging purposes
        print(str(e))
        return HttpResponseServerError()


# ...........................................User Management..................................................

def login(request):

    if 'username' in request.session:
        return redirect("dashboard")

    if request.method == "GET":
        msg = request.session.pop('forgot_password_msg', '')
        return render(request, "auth/login.html", {"msg": msg})

    if not User.objects.filter(username=request.POST['username'].lower()).exists():
        return render(request,"auth/login.html",{"msg":"user Does not exist"})


    user = User.objects.get(username=request.POST['username'].lower())

    if not check_password(request.POST['password'],user.password):
        return render(request,"auth/login.html",{"msg":"Invalid Credential"})

    request.session["username"] = user.username
    return redirect("dashboard")


def signup(request):
    if request.method == "GET":
        return render(request, "auth/signup.html")

    if request.method == "POST":
        username = request.POST.get('username', '').lower()
        password = request.POST.get('password', '')
        rpassword = request.POST.get('rpassword', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')

        if not username or not password or not rpassword:
            return render(request, "auth/signup.html", {"msg": "All fields are required."})

        if User.objects.filter(username=username).exists():
            return render(request, "auth/signup.html", {"msg": "Username already exists."})

        if password != rpassword:
            return render(request, "auth/signup.html", {"msg": "Passwords do not match."})

        try:
            User.objects.create(
                username=username,
                password=make_password(password),
                name=name,
                email=email,
            )
            return render(request, "auth/login.html", {"msg": "User Created. Login to Continue"})
        except Exception as e:
            traceback.print_exc()
            messages.error(request, str(e))
            # Log the error for debugging purposes
            print()
            return render(request, "auth/signup.html",{"msg":str(e)})


def logout(request):
    try:
        del request.session['username']
    except KeyError:
        pass  # 'username' key may not be present in the session

    return redirect('login')


def forgotPassword(request):
    if request.method == "GET":
        return render(request, "auth/forgotPassword.html")

    if request.method == "POST":
        try:
            username = request.POST.get("username", "").lower()
            user = User.objects.get(Q(username=username) | Q(email=username))

            new_password = get_random_string(8)
            sub = "Change in Account"
            message = f"Use This Password to Login to your account:\n{new_password}\n\n Do Not Share With anyone"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            print(sub, message, from_email, recipient_list)
            send_mail(sub, message, from_email, recipient_list)

            user.password = make_password(new_password)
            user.save()

            masked_email = hide_email(user.email)
            msg = f"Password sent to {masked_email}"
            request.session['forgot_password_msg'] = msg

            return redirect('login')
        except User.DoesNotExist:
            return render(request, "auth/forgotPassword.html", {"msg": "User does not exist"})
        except:
            print(traceback.print_exc())
            # Handle other exceptions if necessary
            return render(request, "auth/forgotPassword.html", {"msg": "An error occurred. Please try again."})

    return render(request, "auth/forgotPassword.html")


@auth_user
def changePassword(request, user):
    if request.method == "GET":
        return render(request, "auth/changePassword.html", {"user": user})

    old_password = request.POST.get('old_password', '')
    new_password = request.POST.get('password', '')
    confirm_password = request.POST.get('c_password', '')

    if not check_password(old_password, user.password):
        return render(request, "auth/changePassword.html", {"user": user, "msg": "Old Password Incorrect"})

    if new_password != confirm_password:
        return render(request, "auth/changePassword.html", {"user": user, "msg": "Confirm Password Should Match"})

    user.password = make_password(new_password)
    user.save()

    return redirect('dashboard')



# .............................................EXTRAS................................................


def dateConvert(date_value):
    date_string = date_value
    date_object = datetime.strptime(date_string, "%Y-%m-%d")
    formatted_date = date_object.strftime("%d%b%y").upper()
    return formatted_date


def hide_email(value):
    parts = value.split('@')
    username = parts[0]
    domain = parts[1]
    username = username[:2] + '*' * 8 + username[-1:]  # Hide all characters except the first two and last
    return f"{username}@{domain}"



# hashed_pwd = make_password("plain_text")
# check_password("plain_text",hashed_pwd)  # returns True

