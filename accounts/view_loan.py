from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import F, Sum
from .models import Loan, EMI, DeletedEMI
from .decorators import auth_user
import math

def get_loan_data(user):
    return Loan.objects.filter(created_by=user).order_by(F('status').desc(), 'title')


def get_loan_by_id(id):
    return get_object_or_404(Loan, id=id)


def get_emi_data_by_loan_id(id):
    return EMI.objects.filter(loan_id=id).order_by(F('paid_on').desc())

# ...............................................Loan Management...................................

@auth_user
def addloan(request, user):
    if request.method == "GET":
        loanData = get_loan_data(user)
        return render(request, 'addLoan.html', {'user': user, "loanData": loanData})

    Loan.objects.create(
        title=request.POST['title'],
        amount=request.POST['amount'],
        started_on=request.POST['started_on'],
        created_by=user
    )

    return redirect('home')

@auth_user
def loanHome(request, user):
    loanData = get_loan_data(user)
    return render(request, 'loanHome.html', {'loanData': loanData, 'user': user})

@auth_user
def loanReport(request, id, user):
    loanData = get_loan_by_id(id)
    emiData = get_emi_data_by_loan_id(id)
    
    total = emiData.aggregate(Sum('amount'))['amount__sum'] or 0
    total += loanData.amount
    
    return render(request, 'loanReport.html', {'user': user, 'loanData': loanData, 'emiData': emiData, 'total': math.ceil(total)})
@auth_user
def searchLoan(request, user):
    search_query = request.GET.get('search', '')
    loanData = Loan.objects.filter(title__icontains=search_query).order_by(F("status").desc())
    return render(request, 'loanHome.html', {'user': user, "loanData": loanData})

@auth_user
def updateLoanStatus(request, id):
    loanData = get_loan_by_id(id)
    loanData.status = "Closed" if loanData.status == "Open" else "Open"
    loanData.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@auth_user
def addEMI(request, id):
    loanData = get_loan_by_id(id)
    if request.method == 'POST':
        EMI.objects.create(
            loan=loanData,
            paid_on=request.POST['paid_on'],
            amount=-int(request.POST['amount']),
            note=request.POST['note'],
        )
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@auth_user
def editEmi(request, id):
    emi_data = get_object_or_404(EMI, id=id)
    
    if request.method == "GET":
        return JsonResponse({
            'id': emi_data.id,
            'loan': Loan.objects.get(id=emi_data.loan_id).title,
            'paid_on': emi_data.paid_on,
            'amount': emi_data.amount,
            'note': emi_data.note,
        })
    
    loan = request.POST.get('loan')
    if loan:
        Loan.objects.filter(id=emi_data.loan_id).update(title=loan)

    emi_data.paid_on = request.POST['paid_on']
    emi_data.amount = request.POST['amount']
    emi_data.note = request.POST['note']
    emi_data.save()
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@auth_user
def deleteLoan(request, id):
    if not EMI.objects.filter(loan_id=id).exists():
        current_loan = get_loan_by_id(id)
        current_loan.delete()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@auth_user
def deleteEmi(request, id, user):
    emi_data = get_object_or_404(EMI, id=id)
    
    DeletedEMI.objects.create(
        loan=emi_data.loan.title,
        paid_on=emi_data.paid_on,
        amount=emi_data.amount,
        note=emi_data.note,
        created_by=user
    )
    
    emi_data.delete()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@auth_user
def undoEntries(request, id, user):
    delete_emi = get_object_or_404(DeletedEMI, id=id)
    loan_data = get_object_or_404(Loan, title=delete_emi.loan, created_by=user)
    
    if loan_data:
        EMI.objects.create(
            loan=loan_data,
            paid_on=delete_emi.paid_on,
            amount=delete_emi.amount,
            note=delete_emi.note
        )
    
    delete_emi.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@auth_user
def deletedEntries(request, user):
    deleteEmi = DeletedEMI.objects.filter(created_by=user.id)
    return render(request, 'deletedEntries.html', {"data": deleteEmi, "user": user})
