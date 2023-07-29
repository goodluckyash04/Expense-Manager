from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta
from itertools import chain
from django.db.models import Q
import random,string
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
from django.urls import reverse


# ...........................................Home Page..................................................


def home(request):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])
        return render(request,"home.html",{"user":user})
    else:
        return redirect('login')


# ...........................................User Management..................................................

def login(request):
    if 'username' in request.session:
        return redirect("home")
    else:
        if request.method == "GET":
            msg = ""
            if 'forgot_password_msg' in request.session:
                msg = request.session.get('forgot_password_msg', None)
                del request.session['forgot_password_msg']
            return render(request,"login.html",{"msg":msg})
        else:
            if User.objects.filter(username=request.POST['username'].lower()).exists():
                user = User.objects.get(username=request.POST['username'].lower())
                if check_password(request.POST['password'],user.password):
                    request.session["username"] = user.username
                    return redirect("home")
                else:
                    return render(request,"login.html",{"msg":"Invalid Credential"})

            else:
                return render(request,"login.html",{"msg":"user Does not exist"})


def signup(request):
    if request.method == "GET":
        return render(request,"signup.html")
    else:
        if User.objects.filter(username=request.POST['username'].lower()).exists():
            return render(request,"signup.html",{"msg":"User Exist"})
        else:
            if request.POST['password'] == request.POST["rpassword"]:
                User.objects.create(
                    name = request.POST['name'],
                    username = request.POST['username'].lower(),
                    email = request.POST['email'],
                    password = make_password(request.POST['password'])
                )
                return render(request,"login.html",{"msg":"User Created.Login to Continue"})
            else:
                return render(request,"signup.html",{"msg":"Both Password Should be Same"})


def logout(request):
    del request.session['username']
    return redirect('login')


def forgotPassword(request):
    if request.method == "GET":
        return render(request,"forgotPassword.html")
    else:
        try:
            user = User.objects.get(username = request.POST["username"].lower())
            newPassword = get_random_string(8)
            sub = "Change in Account"
            message = f"Use This Password to Login to ypur account:\n{newPassword}\n\n Do Not Share With anyone"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(sub, message, from_email, recipient_list)
            user.password =  make_password(newPassword)
            user.save()
            maskedEmail =hide_email(user.email)
            msg = f"Password sent to {maskedEmail}"
            request.session['forgot_password_msg'] = msg
            return redirect('login')
        except:
            return render(request,"forgotPassword.html",{"msg":"User Does not exist"})


def changePassword(request):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])
        if request.method == "GET":
            return render(request,"changePassword.html",{"user":user})
        else:
            if check_password(request.POST['old_password'],user.password):
                if request.POST['password'] == request.POST['c_password']:
                    user.password =  make_password(request.POST['password'])
                    user.save()
                    return redirect('addexpense')
                else:
                    return render(request,"changePassword.html",{"user":user,"msg":"confirm Password Should Match"})
            else:
                return render(request,"changePassword.html",{"user":user,"msg":"Old Password Incorrect"})



# ..........................................Expense Management.............................................

def addexpense(request):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])
        paymentData =Payment.objects.filter(Q(payment_by =user) & Q(payment_date__month = datetime.today().month) ).order_by('-payment_date')
        if request.method == "GET":
            request.session["key"] = "dashboard"
            return render(request,"addExpense.html",{"user":user,"paymentData":paymentData})
        elif request.method == "POST":
            if request.POST["payment_type"] == "EMI":
                no = int(request.POST['description'])
                if no == 0:
                    no = 1
                date_object = datetime.strptime(request.POST["payment_date"], "%Y-%m-%dT%H:%M")
                for i in range(1,no+1):
                    desired_date = date_object.replace(day=4, hour=0, minute=1) + relativedelta(months=i)
                    desired_date_str = desired_date.strftime('%Y-%m-%dT%H:%M')
                    Payment.objects.create(
                    payment_type = 'Expense',
                    category = "Loan",
                    payment_date = desired_date_str,
                    amount = int(request.POST["amount"])/no,
                    description = f"EMI {i}({request.POST['loan_name']})",
                    payment_for = "Myself",
                    payment_by = user
                )
                Loan.objects.create(
                    title = request.POST['loan_name'],
                    amount = request.POST['amount'],
                    started_on =  request.POST['payment_date'],
                    created_by =user
                )
            else:    
                Payment.objects.create(
                    payment_type = request.POST["payment_type"],
                    category = request.POST["category"],
                    payment_date = request.POST["payment_date"],
                    amount = request.POST["amount"],
                    description = request.POST["description"],
                    payment_for = request.POST["payment_for"].title(),
                    payment_by = user
                )
            return render(request,"addExpense.html",{"msg":f'{request.POST["payment_type"]} added.',"user":user,"paymentData":paymentData})
    else:
        return redirect("login")


def editEntry(request,id):
    if 'username' in request.session:
        entry = Payment.objects.get(id = id)
        if request.method == "GET":
            if 'value' in request.session:
                key = request.session['value']
            else:
                key = None
            return render(request,'editExpense.html',{'entry':entry,key:key})
        else:
            entry.payment_type = request.POST["payment_type"]
            entry.category = request.POST["category"]
            entry.payment_date = request.POST["payment_date"]
            entry.amount = request.POST["amount"]
            entry.description = request.POST["description"]
            entry.payment_for = request.POST["payment_for"].title()
            entry.save()
            if request.session["key"] == "dashboard":
                return redirect('addexpense')
            elif request.session["key"] == "report":
                return redirect('reports')
            elif request.session["key"] == "search_report":
                return redirect('search_report')
            # next = request.POST.get('next', '/')
            # return HttpResponseRedirect(next)
    else:
        return redirect('addexpense')


def deleteentry(request,id):
    if 'username' in request.session:
        entry = Payment.objects.get(id = id)
        entry.delete()
        if request.session["key"] == "dashboard":
                return redirect('addexpense')
        elif request.session["key"] == "report":
            return redirect('reports')
        elif request.session["key"] == "search_report":
                return redirect('search_report')
       
    else:
        return redirect('addexpense')
    

def reports(request):
    if 'username' in request.session:
        request.session["key"] = "report"
        user = User.objects.get(username = request.session["username"])
        paymentData =Payment.objects.filter(payment_by = user )
        total = 0
        for i in paymentData:
            if i.payment_type == "Expense":
                total-=i.amount
            else:
                total+=i.amount
        return render(request,"reports.html",{"user":user,"paymentData":paymentData,"total":total})
    else:
        return redirect("login")


def search_report(request):
    if 'username' in request.session:
        request.session['key'] = "search_report"
        if 'search' in request.POST:
            value = request.POST["search"]
            request.session['value'] = request.POST["search"]
           
        else: 
            value = request.session['value']
        user = User.objects.get(username = request.session["username"])
    try:
        paymentData =Payment.objects.filter(payment_by = user ).filter(amount = value)
    except:
        paymentData1 =Payment.objects.filter(payment_by = user ).filter(payment_for = value.title())
        paymentData2 =Payment.objects.filter(payment_by = user ).filter(description__icontains= value)
        paymentData = list(chain(paymentData1,paymentData2))
    total = 0
    for i in paymentData:
        if i.payment_type == "Expense":
            total-=i.amount
        else:
            total+=i.amount
    return render(request,"reports.html",{"user":user,"paymentData":paymentData,"total":total,"key":value})


def filter_report(request):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])
        key = {'payment_type': request.POST['payment_type'], 
               'category': request.POST['category'], 
               'payment_for': request.POST['payment_for'], 
               'startdate': request.POST['startdate'], 'enddate': request.POST['enddate']}

        filterData = Q(payment_by=user)
        if request.POST['payment_for'] != "Other":
            if request.POST["payment_for"]:
                filterData &= Q(payment_for=request.POST["payment_for"])
            if request.POST["payment_type"]:
                filterData &= Q(payment_type=request.POST["payment_type"])
            if request.POST["category"]:
                filterData &= Q(category=request.POST["category"])
            if request.POST["startdate"] and request.POST["enddate"]:
                endDate = datetime.strptime(request.POST['enddate'],("%Y-%m-%d"))
                toDate = endDate + timedelta(days=1)
                filterData &= Q(payment_date__range=[request.POST["startdate"], toDate.strftime("%Y-%m-%d")])
            paymentData = Payment.objects.filter(filterData)
        else:
            if request.POST["payment_type"]:
                filterData &= Q(payment_type=request.POST["payment_type"])
            if request.POST["category"]:
                filterData &= Q(category=request.POST["category"])
            if request.POST["startdate"] and request.POST["enddate"]:
                filterData &= Q(payment_date__range=[request.POST["startdate"], request.POST['enddate']])

            paymentData =Payment.objects.filter(filterData).exclude(payment_for__in = ["Mom","Dad","Myself"] )

        total = 0
        for i in paymentData:
            if i.payment_type == "Expense":
                total-=i.amount
            else:
                total+=i.amount
       
        return render(request,"reports.html",{"user":user,"paymentData":paymentData.order_by("payment_date"),"total":total,"data":key})
    else:
        return redirect("login")
        

def delete_records(request):
    if 'username' in request.session:
        del_list = request.POST.getlist('record_ids')
        for i in del_list:
            Payment.objects.get(id = i).delete()
        if request.session['key'] == "search_report":
             return redirect('search_report')
        else:
            return redirect('reports')
    else:
        return redirect('login')



# ............................................Task Management...........................................

def addTask(request):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])
        taskData =Task.objects.filter(Q(created_by =user) & Q(complete_by__month= datetime.today().month) & Q(status = "Pending") ).order_by('-complete_by')
        # taskData =Task.objects.filter(created_by =user)
        print(taskData)
        if request.method == "GET":
            request.session["key"] = "dashboard"
            return render(request,"tasks.html",{"user":user,"taskData":taskData})
        elif request.method == "POST":
            Task.objects.create(
                priority = request.POST["priority"],
                task_title = request.POST["task_title"],
                complete_by = request.POST["complete_by"],
                task_detail = request.POST["task_detail"],
                status = "Pending",
                completed_on = request.POST["complete_by"],
                created_by = user
            )
            return render(request,"tasks.html",{"msg":"task added","user":user,"taskData":taskData})
    else:
        return redirect("login")


def updatetask(request,id):
    current_task = Task.objects.get(id = id)
    current_task.completed_on = datetime.today()
    current_task.status = "Completed"
    current_task.save()
    return redirect('addTask')


def incomplete(request,id):
    current_task = Task.objects.get(id = id)
    current_task.completed_on = datetime.today()
    current_task.status = "Pending"
    current_task.save()
    return redirect('taskReports')


def deletetask(request,id):
    current_task = Task.objects.get(id = id)
    current_task.completed_on = datetime.today()
    current_task.status = "Deleted"
    current_task.save()
    return redirect('addTask')


def permdeletetask(request,id):
    current_task = Task.objects.get(id = id)
    print(current_task)
    current_task.delete()
    return redirect('taskReports')


def taskReports(request):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])
    taskData = Task.objects.filter(created_by = user)
    return render(request,'taskReport.html',{'user':user,'taskData':taskData})

# ...............................................Loan Management...................................

def loan(request):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])
        loanData = Loan.objects.filter(created_by=user).order_by("title") 

        if request.method == "GET":
            return render(request,'loan.html',{'user':user,"loanData":loanData})
        else:
            Loan.objects.create(
                title = request.POST['title'],
                amount = request.POST['amount'],
                started_on =  request.POST['started_on'],
                created_by =user
            )
            return render(request,'loan.html',{'user':user,"loanData":loanData})
    else:
        return redirect("login")


def loanEMI(request):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])
        loanData = Loan.objects.filter(created_by=user).order_by("title") 
        loan = Loan.objects.get(title = request.POST['loan'])
        EMI.objects.create(
            loan = loan,
            amount = request.POST['amount'],
            note = request.POST['note'],
        )
    return render(request,'loan.html',{'user':user,"loanData":loanData})


def loanReport(request):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])
        loanData = Loan.objects.filter(created_by=user).order_by("title") 

        if request.method == "GET":
            return render(request,'loanReport.html',{'user':user,"loanData":loanData})
        else:
            emiData = EMI.objects.filter(loan__title= request.POST['loan'])
            loan = Loan.objects.get(title = request.POST['loan'])
            loan_amount = loan
            total = loan.amount
            for i in emiData:
                total-= i.amount
            return render(request,'loanReport.html',{'user':user,"emiData":emiData,"loanData":loanData,"loan_amount":loan_amount,"total":total})
    else:
        return redirect('login')    


def deleteEmi(request,id):
    current_EMI = EMI.objects.get(id = id)
    current_EMI.delete()
    return redirect('loanReport')


def deleteLoan(request,id):
    current_Loan = Loan.objects.get(id = id)
    current_Loan.delete()
    return redirect('loan')






# .............................................EXTRAS................................................

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

    
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