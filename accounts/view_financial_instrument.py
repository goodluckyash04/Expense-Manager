import datetime
import decimal
import traceback
from django.contrib import messages
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponseServerError, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F, Sum, Q
from .models import FinancialProduct, Transaction
from .decorators import auth_user
# import math


# ...............................................Loan Management...................................

def desired_date(start_date,i):
    payment_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    current_month = payment_date.month
    current_year = payment_date.year
    current_day = payment_date.day
    desired_month = current_month + i
    desired_year = current_year + (desired_month - 1) // 12
    desired_month = (desired_month - 1) % 12 + 1
    desired_date = datetime.datetime(desired_year, desired_month, current_day)
    return desired_date.strftime('%Y-%m-%d')



@auth_user
def create_finance(request, user):
    try:
        name = request.POST.get("name", "")
        type = request.POST.get("type", "")
        amount = int(request.POST.get("amount", 0.0))
        no_of_installments = int(request.POST.get("no_of_installments", 1))
        started_on = request.POST.get("started_on", "")

        if no_of_installments < 1:
            raise ValueError('Installments can not be Zero(0)')

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

            for i in range(0,no_of_installments):
                sub = 'EMI' if type == 'Loan' else 'SIP'
                Transaction.objects.create(
                    type="Expense",
                    category="EMI" if type == 'Loan' else 'Investment',
                    date=desired_date(started_on,i),
                    amount=emi_amount,
                    beneficiary= 'Self',
                    description= f'{name} {sub} {i+1}',
                    status= "Pending",
                    mode="Online",
                    mode_detail= type,
                    created_by=user,
                    source = new_product
                )

        messages.success(request, f'{type}  Added')
        return redirect('utilities')
    except ValidationError as e:
        messages.error(request, str(e))
        return redirect('utilities')
    except ValueError as e:
        print(traceback.print_exc())
        messages.error(request, str(e))
        return redirect('utilities')
    except Exception as e:
        messages.error(request, "An unexpected error occurred.")
        print(traceback.print_exc())
        return HttpResponseServerError()

@auth_user
def finance_details(request, user):
    try:
        search_query = request.GET.get('search','').strip()
        print("search_query",search_query)
        query = Q(created_by=user, is_deleted=False)
        if search_query:
            query &=Q(name__icontains=search_query) | Q(type=search_query)
        print(query)
        details = FinancialProduct.objects.filter(query).order_by(F('status').desc(), 'name')
        for product in details:
            installments = Transaction.objects.filter(source=product.id,is_deleted = False)
            remaining_transactions = [trn for trn in installments if trn.status != "Completed"]
            product.remaining_amount = sum(trn.amount for trn in remaining_transactions)
            product.remaining_installments = len(remaining_transactions)
        return render(request, 'financial_instrument/financeHome.html', {'details': details,'search_query':search_query,'user': user})
    except Exception as e:
        messages.error(request, "An unexpected error occurred.")
        print(traceback.print_exc())
        return HttpResponseServerError()


@auth_user
def update_finance_detail(request,id, user):
    try:
        details = get_object_or_404(FinancialProduct, created_by=user, id=id)
        if request.method == "GET":
            return JsonResponse({
                "type": details.type,
                "name":details.name,
                "started_on":details.started_on,
                "amount": details.amount,
                "no_of_installments":details.no_of_installments
            })

        name = request.POST.get("name", "")
        i_type = request.POST.get("type", "")
        started_on = request.POST.get("started_on", "")
        amount = decimal.Decimal(request.POST.get("amount", 0.0))
        no_of_installments = int(request.POST.get("no_of_installments", 1))

        if no_of_installments < 1:
            raise ValueError('Installments can not be Zero(0)')

        sub = 'SIP' if i_type == 'SIP' else 'EMI'
        transactions = Transaction.objects.filter(created_by=user, source_id=id, is_deleted=False)

        # name update
        details.name = name
        for index, trn in enumerate(transactions, 1):
            trn.description = f'{name} {sub} {index}'
            trn.save()

        # type update
        if i_type != details.type:
            details.type = i_type
            for index,trn in enumerate(transactions,1):
                trn.category = "EMI" if i_type == 'Loan' else 'Investment'
                trn.mode_detail = i_type
                trn.description = f'{name} {sub} {index}'
                trn.save()

        # start date update only if all pending else changes only pending date
        if datetime.datetime.strptime(started_on,"%Y-%m-%d").date() != details.started_on:
            no_of_paid_installments = sum(1 if trn.status == "Completed" else 0 for trn in transactions)
            dates = [trn.date for trn in transactions if trn.status == "Completed"]
            if dates:
                for date in dates:
                    print(date,started_on)
                    if date >= datetime.datetime.strptime(started_on,"%Y-%m-%d").date():
                        raise ValueError(f'Date can not be less than {date}.')
            if not no_of_paid_installments:
                details.started_on = started_on

            for i,trn in enumerate(transactions,0):
                if i >= no_of_paid_installments:
                    i = i-no_of_paid_installments
                    trn.date = desired_date(started_on,i)
                    trn.save()

        # amount or installment changes
        if amount != details.amount or no_of_installments != details.no_of_installments:
            previous_installments = details.no_of_installments
            completed_transaction = sum(1 if x.status == 'Completed' else 0 for x in transactions )

            if completed_transaction:
                paid_amount = sum(x.amount if x.status == 'Completed' else 0 for x in transactions)

                if amount < paid_amount:
                    raise ValueError(f'Amount cannot be less than total paid amount {paid_amount}')

                if no_of_installments < completed_transaction:
                    raise ValueError(f'Installments cannot be less than {completed_transaction}')

                if amount > paid_amount and no_of_installments == completed_transaction:
                    raise ValueError(f'Installments cannot be less than {completed_transaction+1}')

                remaining_amount = amount - paid_amount
                remaining_installments = no_of_installments - completed_transaction
                emi_amount = round((remaining_amount / remaining_installments), 2) if remaining_installments else 0

                details.amount = amount
                details.no_of_installments = no_of_installments

                if no_of_installments > previous_installments:
                    new_trn = no_of_installments - previous_installments
                    for trn in transactions:
                        if trn.status != 'Completed':
                            trn.amount = emi_amount
                            trn.save()
                    for i in range(previous_installments,previous_installments+new_trn):
                        new = transactions.last()
                        print(new)
                        Transaction.objects.create(
                            type=new.type,
                            category=new.category,
                            date= desired_date(new.date.strftime("%Y-%m-%d"), 1),
                            amount= emi_amount,
                            beneficiary='Self',
                            description=f'{name} {sub} {i + 1}',
                            status="Pending",
                            mode="Online",
                            mode_detail=details.type,
                            created_by=user,
                            source=details
                        )

                if no_of_installments < previous_installments:
                    for index, trn in enumerate(transactions,1):
                        if index <= no_of_installments:
                            if trn.status != 'Completed':
                                trn.amount = emi_amount
                                trn.save()
                        else:
                            trn.delete()
                else:
                    for trn in transactions:
                        if trn.status != 'Completed':
                            trn.amount = emi_amount
                            trn.save()


            # if not all transactions are pending
            else:
                details.amount = amount
                details.no_of_installments = no_of_installments
                emi_amount = round((amount / no_of_installments), 2)
                if no_of_installments > previous_installments:
                    new_trn = no_of_installments - previous_installments
                    for trn in transactions:
                        trn.amount = emi_amount
                        trn.save()
                    for i in range(previous_installments, previous_installments + new_trn):
                        new = transactions.last()
                        print(new)
                        Transaction.objects.create(
                            type=new.type,
                            category=new.category,
                            date=desired_date(new.date.strftime("%Y-%m-%d"), 1),
                            amount=emi_amount,
                            beneficiary='Self',
                            description=f'{name} {sub} {i + 1}',
                            status="Pending",
                            mode="Online",
                            mode_detail=details.type,
                            created_by=user,
                            source=details
                        )
                if no_of_installments < previous_installments:
                    for index, trn in enumerate(transactions, 1):
                        if index <= no_of_installments:
                            trn.amount = emi_amount
                            trn.save()
                        else:
                            trn.delete()
                else:
                    for trn in transactions:
                        trn.amount = emi_amount
                        trn.save()

        details.save()
        messages.success(request, f'Updated Succesfully')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except ValueError as e:
        print(traceback.print_exc())
        messages.error(request, str(e))
        return redirect('finance-details')
    except Exception as e:
        messages.error(request, "An unexpected error occurred.")
        print(traceback.print_exc())
        return HttpResponseServerError()


@auth_user
def fetch_financial_transaction(request,id, user):
    try:
        product_details = FinancialProduct.objects.get(created_by=user,id=id)
        if not product_details:
            raise ValueError('No Details Found')
        all_transaction = Transaction.objects.filter(created_by=user,source=id,is_deleted = False).order_by('-date')
        paid_trn = [trn for trn in all_transaction if trn.status == "Completed"]
        product_details.paid_amount = sum(trn.amount for trn in paid_trn)
        product_details.paid_installment = sum(1 for trn in paid_trn)
        product_details.remaining_amount = product_details.amount - product_details.paid_amount
        return render(request, 'financial_instrument/installmentDetails.html', {'all_transaction': all_transaction, "product_details" :product_details,'user': user})
    except ValueError as e:
        print(traceback.print_exc())
        messages.error(request, str(e))
        return redirect('finance-details')
    except Exception as e:
        messages.error(request, "An unexpected error occurred.")
        print(traceback.print_exc())
        return HttpResponseServerError()


@auth_user
def update_instrument_status(request, id, user):
    try:
        product_details = FinancialProduct.objects.get(created_by=user, id=id )
        if not product_details:
            raise ValueError('No Details Found')
        all_transaction = Transaction.objects.filter(created_by=user, source=id, is_deleted=False)
        paid_trn = [trn for trn in all_transaction if trn.status == "Pending"]
        if paid_trn:
            raise ValueError(f'Can not Close {product_details.name.title()}  due to {len(paid_trn)} pending Installments')
        if product_details.status == "Open":
            product_details.status = 'Closed'
        else:
            product_details.status = 'Open'
        product_details.save()
        messages.info(request, f'{product_details.name.title()} Status updated')
        return redirect('finance-details')
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except ValueError as e:
        print(traceback.print_exc())
        messages.error(request, str(e))
        return redirect('finance-details')
    except Exception as e:
        messages.error(request, "An unexpected error occurred.")
        print(traceback.print_exc())
        return HttpResponseServerError()


@auth_user
def remove_instrument(request, id, user):
    try:
        if Transaction.objects.filter(created_by=user, source=id, is_deleted=False):
            messages.error(request, f"Instrument with installments cannot be deleted")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        current_product = FinancialProduct.objects.get(created_by=user, id=id, is_deleted=False)
        current_product.is_deleted = True
        current_product.deleted_at = datetime.datetime.today()
        current_product.save()
        messages.success(request, f"{current_product.name} deleted successfully")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        messages.error(request, "An unexpected error occurred.")
        print(traceback.print_exc())
        return HttpResponseServerError()
