from django.shortcuts import render,redirect
from .models import *


# ...............................................Loan Management...................................

def addloan(request):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])
        loanData = Loan.objects.filter(created_by=user).order_by("title") 

        if request.method == "GET":
            return render(request,'addLoan.html',{'user':user,"loanData":loanData})
        else:
            Loan.objects.create(
                title = request.POST['title'],
                amount = request.POST['amount'],
                started_on =  request.POST['started_on'],
                created_by =user
            )
        return redirect('home')
    else:
        return redirect("login")


def loanHome(request):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])
        loanData = Loan.objects.filter(created_by=user).order_by("-status","title") 
        return render(request,'loanHome.html',{"loanData":loanData})
    else:
        return redirect('login')    
    

def updateLoanStatus(request,id):
    if 'username' in request.session:
        loanData = Loan.objects.get(id=id)

        if loanData.status == "Open":
            loanData.status = "Closed"
        else:
            loanData.status = "Open"

        loanData.save()
        return redirect('loanHome')
    else:
        return redirect('login')    
    

def loanReport(request,id):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])
        
        if request.method == "GET":
            loanData = Loan.objects.get(id= id)
            emiData = EMI.objects.filter(loan_id = id ).order_by('-paid_on')
            
            total = loanData.amount
            for i in emiData:
                total += i.amount
            return render(request,'loanReport.html',{'user':user,"loanData":loanData,'emiData':emiData,'total':total})
    else:
        return redirect('login')    



def addEMI(request,id):
    if 'username' in request.session:
        loanData = Loan.objects.get(id= id)
        EMI.objects.create(
            loan = loanData,
            paid_on = request.POST['paid_on'],
            amount = -int(request.POST['amount']),
            note = request.POST['note'],
        )
        return redirect('loanReport',id=id)
    else:
        return redirect('login')

def deleteLoan(request,id):
    if 'username' in request.session:
        emis = EMI.objects.filter(loan_id = id)
        if not emis:
            current_Loan = Loan.objects.get(id = id)
            current_Loan.delete()
        return redirect('loanHome')
    else:
        return redirect('login')

def deleteEmi(request,id):
    if 'username' in request.session:
        current_EMI = EMI.objects.get(id = id)
        loandata = Loan.objects.get(id=current_EMI.loan_id)
        current_EMI.delete()
        return redirect('loanReport',id=loandata.id)
    else:
        return redirect('login')