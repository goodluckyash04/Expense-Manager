from django.shortcuts import render,redirect
from .models import *
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta
from itertools import chain
from django.db.models import Q
import calendar



# ..........................................Expense Management.............................................

def addexpense(request):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])

        if request.POST["category"] == "M_Loan":
            no = int(request.POST['description'])
            if no == 0:
                no = 1
            date_object = datetime.strptime(request.POST["payment_date"], "%Y-%m-%dT%H:%M")
            for i in range(1,no+1):
                desired_date = date_object.replace(day=4, hour=0, minute=1) + relativedelta(months=i)
                desired_date_str = desired_date.strftime('%Y-%m-%dT%H:%M')
                Payment.objects.create(
                payment_type = 'Expense',
                category = "M_Loan",
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
            if request.POST['category']:
                categoryData = request.POST['category']
            else:
                categoryData = "Loan"
            if request.POST["payment_for"] :
                paid_for = request.POST["payment_for"].title()
            else:
                paid_for = "Myself"
            Payment.objects.create(
                payment_type = request.POST["payment_type"],
                category = categoryData,
                payment_date = request.POST["payment_date"],
                amount = request.POST["amount"],
                description = request.POST["description"],
                payment_for = paid_for,
                payment_by = user
            )
        return redirect('home')
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
            if request.POST['category']:
                if request.POST['payment_type'] != 'Loan':
                    categoryData = request.POST['category']
                else:
                    categoryData = "Loan"
            if 'payment_for' in request.POST:
                if request.POST["payment_for"] :
                    if request.POST['payment_type'] != 'Income':
                        paid_for = request.POST["payment_for"].title()
                    else:
                        paid_for = "Myself"
            else:
                paid_for = "Myself"

                    
            entry.payment_type = request.POST["payment_type"]
            entry.category = categoryData
            entry.payment_date = request.POST["payment_date"]
            entry.amount = request.POST["amount"]
            entry.description = request.POST["description"]
            entry.payment_for = paid_for
            entry.save()
            if request.session["key"] == "current":
                return redirect('currentMonthreports')
            elif request.session["key"] == "report":
                return redirect('reports')
            elif request.session["key"] == "search_report":
                return redirect('search_report')
       
    else:
        return redirect('login')

    

def reports(request):
    if 'username' in request.session:
        request.session["key"] = "report"
        user = User.objects.get(username = request.session["username"])
        paymentData =Payment.objects.filter(payment_by = user ).order_by('payment_date')
        total = 0
        for i in paymentData:
            if i.payment_type == "Expense":
                total-=i.amount
            else:
                total+=i.amount
        return render(request,"reports.html",{"user":user,"paymentData":paymentData,"total":total})
    else:
        return redirect("login")


def currentMonthreports(request):
    if 'username' in request.session:
        request.session["key"] = "current"
        user = User.objects.get(username = request.session["username"])
        current_year = datetime.now().year
        current_month = datetime.now().month
        paymentData = Payment.objects.filter(Q(payment_by = user ) & Q(payment_date__month=current_month) & Q(payment_date__year=current_year)).order_by('-payment_date')
        current_month_name = calendar.month_name[current_month]
        total = 0
        expenseTotal = 0
        for i in paymentData:
            if i.payment_type == "Expense":
                total-=i.amount
            else:
                total+=i.amount
            if i.payment_type != "Loan":
                if i.payment_type == "Expense":
                    expenseTotal-=i.amount
                else:
                    expenseTotal+=i.amount
        return render(request,"reports.html",{"user":user,"paymentData":paymentData,"expenseTotal":expenseTotal,"total":total,"key":f"{current_month_name} {current_year}"})
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
        expenseTotal = 0
        for i in paymentData:
            if i.payment_type == "Expense":
                total-=i.amount
            else:
                total+=i.amount

        return render(request,"reports.html",{"user":user,"paymentData":paymentData,"total":total,"key":value})
    else:
        return redirect("login")

def filter_report(request):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])
        key = {'payment_type': request.POST.getlist('payment_type'), 
               'category': request.POST['category'], 
               'payment_for': request.POST['payment_for'], 
               'startdate': request.POST['startdate'], 'enddate': request.POST['enddate']}

        filterData = Q(payment_by=user)
        if request.POST['payment_for'] != "Other":
            if request.POST["payment_for"]:
                filterData &= Q(payment_for=request.POST["payment_for"])
            if request.POST.getlist('payment_type'):
                filterData &= Q(payment_type__in=request.POST.getlist('payment_type'))
            if request.POST["category"]:
                filterData &= Q(category=request.POST["category"])
            if request.POST["startdate"] and request.POST["enddate"]:
                endDate = datetime.strptime(request.POST['enddate'],("%Y-%m-%d"))
                toDate = endDate + timedelta(days=1)
                filterData &= Q(payment_date__range=[request.POST["startdate"], toDate.strftime("%Y-%m-%d")])
            paymentData = Payment.objects.filter(filterData)
        else:
            if request.POST.getlist('payment_type'):
                filterData &= Q(payment_type__in=request.POST.getlist('payment_type'))
            if request.POST["category"]:
                filterData &= Q(category=request.POST["category"])
            if request.POST["startdate"] and request.POST["enddate"]:
                filterData &= Q(payment_date__range=[request.POST["startdate"], request.POST['enddate']])

            paymentData =Payment.objects.filter(filterData).exclude(payment_for__in = ["Mom","Dad","Myself","Home"] )

        total = 0
        expenseTotal = 0    
        for i in paymentData:
            if i.payment_type == "Expense":
                total-=i.amount
            else:
                total+=i.amount
            if i.payment_type != "Loan":
                if i.payment_type == "Expense":
                    expenseTotal-=i.amount
                else:
                    expenseTotal+=i.amount   
        return render(request,"reports.html",{"user":user,"paymentData":paymentData.order_by("payment_date"),"total":total,"expenseTotal":expenseTotal,"data":key})
    else:
        return redirect("login")


def deleteentry(request,id):
    if 'username' in request.session:
        entry = Payment.objects.get(id = id)
        DeletePayment.objects.create(
                payment_type = entry.payment_type,
                category = entry.category,
                payment_date = entry.payment_date,
                amount = entry.amount,
                description = entry.description,
                payment_for = entry.payment_for,
                payment_by = entry.payment_by
            )
        entry.delete()
        if request.session["key"] == "current":
                return redirect('currentMonthreports')
        elif request.session["key"] == "report":
            return redirect('reports')
        elif request.session["key"] == "search_report":
                return redirect('search_report')
       
    else:
        return redirect('login')


def delete_records(request):
    if 'username' in request.session:
        del_list = request.POST.getlist('record_ids')
        for i in del_list:
            entry = Payment.objects.get(id = i)
            DeletePayment.objects.create(
                    payment_type = entry.payment_type,
                    category = entry.category,
                    payment_date = entry.payment_date,
                    amount = entry.amount,
                    description = entry.description,
                    payment_for = entry.payment_for,
                    payment_by = entry.payment_by
                )
            entry.delete()
        if request.session["key"] == "current":
                return redirect('currentMonthreports')
        elif request.session["key"] == "report":
            return redirect('reports')
        elif request.session["key"] == "search_report":
                return redirect('search_report')
    else:
        return redirect('login')

def getDeletedEntries(request):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])

        deletePay = DeletePayment.objects.filter(payment_by =user.id)
        return render(request,'deleteExpense.html',{"data":deletePay,"user":user})
    else:
        return redirect('login')
    
def undoDelEntries(request,id):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])
        entry = DeletePayment.objects.get(id = id)
        Payment.objects.create(
            payment_type = entry.payment_type,
            category = entry.category,
            payment_date = entry.payment_date,
            amount = entry.amount,
            description = entry.description,
            payment_for = entry.payment_for,
            payment_by = user
        )
        entry.delete()
        return redirect('getDeletedEntries')
    else:
        return redirect('login')