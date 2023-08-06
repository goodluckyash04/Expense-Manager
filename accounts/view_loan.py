from django.shortcuts import render,redirect
from .models import *
from django.db.models import Q



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



