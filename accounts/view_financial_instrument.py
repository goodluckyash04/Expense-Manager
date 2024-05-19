import datetime
import traceback

from django.contrib import messages
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404
# from django.http import JsonResponse, HttpResponseRedirect
# from django.db.models import F, Sum
from .models import FinancialProduct, Transaction
from .decorators import auth_user
# import math
#
# def get_loan_data(user):
#     return Loan.objects.filter(created_by=user).order_by(F('status').desc(), 'title')
#
#
# def get_loan_by_id(id):
#     return get_object_or_404(Loan, id=id)
#
#
# def get_emi_data_by_loan_id(id):
#     return EMI.objects.filter(loan_id=id).order_by(F('paid_on').desc())
#
# ...............................................Loan Management...................................

@auth_user
def create_finance(request, user):
    try:
        name = request.POST.get("name", "")
        type = request.POST.get("type", "")
        amount = int(request.POST.get("amount", 0.0))
        no_of_installments = int(request.POST.get("no_of_installments", ""))
        started_on = request.POST.get("started_on", "")
        print(started_on)
        try:
            existing_transaction = FinancialProduct.objects.get(
                name=name,
                type=type,
                amount=amount,
                no_of_installments=no_of_installments,
                started_on=started_on,
                created_by=user)
            if existing_transaction:
                raise ValueError(f"{type} Already Exist")
        except ObjectDoesNotExist:

            new_product = FinancialProduct.objects.create(
                name = name,
                type = type,
                amount = amount,
                no_of_installments = no_of_installments,
                started_on = started_on,
                created_by = user
            )

            # Add EMI Transaction
            emi_amount = round((amount/no_of_installments),2)
            payment_date = datetime.datetime.strptime(started_on,"%Y-%m-%d")
            current_month = payment_date.month
            current_year = payment_date.year
            current_day = payment_date.day
            for i in range(0,no_of_installments):
                desired_month = current_month + i
                desired_year = current_year + (desired_month - 1) // 12
                desired_month = (desired_month - 1) % 12 + 1
                desired_date = datetime.datetime(desired_year, desired_month, current_day)

                desired_date_str = desired_date.strftime('%Y-%m-%d')

                Transaction.objects.create(
                    type="Expense",
                    category="EMI",
                    date=desired_date_str,
                    amount=emi_amount,
                    beneficiary= 'Self',
                    description= f'{name} EMI {i+1}',
                    status="Pending",
                    mode="Online",
                    mode_detail="Loan",
                    created_by=user,
                    source = new_product
                )

        messages.success(request, f'{type}  Added')
        return redirect('home')
    except ValidationError as e:
        messages.error(request, str(e))
        return redirect('home')
    except ValueError as e:
        print(traceback.print_exc())
        messages.error(request, str(e))
        return redirect('home')
    except Exception as e:
        messages.error(request, "An unexpected error occurred.")
        print(traceback.print_exc())
        return HttpResponseServerError()

# @auth_user
# def loanHome(request, user):
#     loanData = get_loan_data(user)
#     return render(request, 'financial_instrument/loanHome.html', {'loanData': loanData, 'user': user})
#
# @auth_user
# def loanReport(request, id, user):
#     loanData = get_loan_by_id(id)
#     emiData = get_emi_data_by_loan_id(id)
#
#     total = emiData.aggregate(Sum('amount'))['amount__sum'] or 0
#     total += loanData.amount
#
#     return render(request, 'financial_instrument/loanReport.html', {'user': user, 'loanData': loanData, 'emiData': emiData, 'total': math.ceil(total)})
# @auth_user
# def searchLoan(request, user):
#     search_query = request.GET.get('search', '')
#     loanData = Loan.objects.filter(title__icontains=search_query).order_by(F("status").desc())
#     return render(request, 'financial_instrument/loanHome.html', {'user': user, "loanData": loanData})
#
# @auth_user
# def updateLoanStatus(request, id):
#     loanData = get_loan_by_id(id)
#     loanData.status = "Closed" if loanData.status == "Open" else "Open"
#     loanData.save()
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#
# @auth_user
# def addEMI(request, id):
#     loanData = get_loan_by_id(id)
#     if request.method == 'POST':
#         EMI.objects.create(
#             financial_instrument=loanData,
#             paid_on=request.POST['paid_on'],
#             amount=-int(request.POST['amount']),
#             note=request.POST['note'],
#         )
#
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#
# @auth_user
# def editEmi(request, id):
#     emi_data = get_object_or_404(EMI, id=id)
#
#     if request.method == "GET":
#         return JsonResponse({
#             'id': emi_data.id,
#             'financial_instrument': Loan.objects.get(id=emi_data.loan_id).title,
#             'paid_on': emi_data.paid_on,
#             'amount': emi_data.amount,
#             'note': emi_data.note,
#         })
#
#     financial_instrument = request.POST.get('financial_instrument')
#     if financial_instrument:
#         Loan.objects.filter(id=emi_data.loan_id).update(title=financial_instrument)
#
#     emi_data.paid_on = request.POST['paid_on']
#     emi_data.amount = request.POST['amount']
#     emi_data.note = request.POST['note']
#     emi_data.save()
#
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#
# @auth_user
# def deleteLoan(request, id):
#     if not EMI.objects.filter(loan_id=id).exists():
#         current_loan = get_loan_by_id(id)
#         current_loan.delete()
#
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#
# @auth_user
# def deleteEmi(request, id, user):
#     emi_data = get_object_or_404(EMI, id=id)
#
#     DeletedEMI.objects.create(
#         financial_instrument=emi_data.financial_instrument.title,
#         paid_on=emi_data.paid_on,
#         amount=emi_data.amount,
#         note=emi_data.note,
#         created_by=user
#     )
#
#     emi_data.delete()
#
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#
# @auth_user
# def undoEntries(request, id, user):
#     delete_emi = get_object_or_404(DeletedEMI, id=id)
#     loan_data = get_object_or_404(Loan, title=delete_emi.financial_instrument, created_by=user)
#
#     if loan_data:
#         EMI.objects.create(
#             financial_instrument=loan_data,
#             paid_on=delete_emi.paid_on,
#             amount=delete_emi.amount,
#             note=delete_emi.note
#         )
#
#     delete_emi.delete()
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#
# @auth_user
# def deletedEntries(request, user):
#     deleteEmi = DeletedEMI.objects.filter(created_by=user.id)
#     return render(request, 'financial_instrument/deletedEntries.html', {"data": deleteEmi, "user": user})
