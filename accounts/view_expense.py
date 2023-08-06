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
        paymentData =Payment.objects.filter(Q(payment_by =user) & Q(payment_date__month = datetime.today().month) ).order_by('-payment_date')
        if request.method == "GET":
            request.session["key"] = "dashboard"
            return render(request,"addExpense.html",{"user":user,"paymentData":paymentData})
        elif request.method == "POST":
            if request.POST["category"] == "Loan":
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
            print(entry.__dict__)
            return render(request,'editExpense.html',{'entry':entry,key:key})
        else:
            if request.POST['category']:
                    categoryData = request.POST['category']
            else:
                categoryData = "Loan"
            if request.POST["payment_for"] :
                paid_for = request.POST["payment_for"].title()
            else:
                paid_for = "Myself"
                    
            entry.payment_type = request.POST["payment_type"]
            entry.category = categoryData
            entry.payment_date = request.POST["payment_date"]
            entry.amount = request.POST["amount"]
            entry.description = request.POST["description"]
            entry.payment_for = paid_for
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


def currentMonthreports(request):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])
        current_year = datetime.now().year
        current_month = datetime.now().month
        paymentData = Payment.objects.filter(Q(payment_by = user ) & Q(payment_date__month=current_month) & Q(payment_date__year=current_year))
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

