import calendar
import traceback
from itertools import chain
from django.db.models import Q
from django.contrib import messages
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponseServerError, JsonResponse
from django.utils import timezone

from .decorators import auth_user
from .models import Transaction, FinancialProduct


# ..........................................Transaction Management.............................................

@auth_user
def create_transaction(request, user):
    try:
        category = request.POST.get("category", "Other")
        type = request.POST.get("type")
        # date = datetime.strptime(request.POST.get("date"),"%Y-%m-%dT%H:%M")
        date = request.POST.get("date")
        beneficiary = request.POST.get("beneficiary", "Self").title()
        amount = int(request.POST.get("amount", 0.0))
        description = request.POST.get("description", "")
        status = request.POST.get("status", "completed")
        mode = request.POST.get("mode", "Online")
        mode_detail = request.POST.get("mode_detail")

        if type == 'Income':
            beneficiary = 'Self'
            status = "Completed"
            mode = None
            mode_detail = None

        if amount <= 0:
            raise ValueError("Expense amount must be greater than zero.")

        try:
            existing_transaction = Transaction.objects.get(type = type,
                category = category,
                date = date,
                amount = amount,
                beneficiary = beneficiary,
                description = description,
                status = status,
                mode = mode,
                mode_detail = mode_detail,
                created_by = user,
                is_deleted = False)
            if existing_transaction:
                raise ValueError("Transaction Already Exist")
        except ObjectDoesNotExist:
            Transaction.objects.create(
                type = type,
                category = category,
                date = date,
                amount = amount,
                beneficiary = beneficiary,
                description = description,
                status = status,
                mode = mode,
                mode_detail = mode_detail,
                created_by = user,
            )
            messages.success(request, f'{type} Transaction Added')
        return redirect('home')
    except ValidationError as e:
        messages.error(request, str(e))
        return redirect('home')
    except ValueError as e:
        messages.error(request, str(e))
        return redirect('home')
    except Exception as e:
        messages.error(request, "An unexpected error occurred.")
        # Log the error for debugging purposes
        print(traceback.print_exc())
        return HttpResponseServerError()

@auth_user
def update_transaction(request, id):
    try:
        entry = get_object_or_404(Transaction, id=id)
        if request.method == "GET":
            return JsonResponse({
                "type": entry.type,
                "category": entry.category,
                "date": entry.date,
                "amount": entry.amount,
                "description": entry.description,
                "beneficiary": entry.beneficiary,
                "mode_detail": entry.mode_detail,
                "mode": entry.mode,
                "status": entry.status
            })

        entry.category = request.POST.get("category", entry.category)
        entry.date = request.POST.get("date", entry.date)
        entry.amount = request.POST.get("amount", entry.amount)
        entry.description = request.POST.get("description", entry.description)
        entry.beneficiary = request.POST.get("beneficiary", entry.beneficiary).title()
        entry.mode_detail = request.POST.get("mode_detail", entry.mode_detail).title()
        entry.mode = request.POST.get("mode", entry.mode).title()
        entry.save()

        messages.success(request, "Transaction Updated")
    except ObjectDoesNotExist:
        messages.error(request, "Entry not found")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@auth_user
def transaction_detail(request, user):
    try:
        type = request.GET.getlist('type', [])
        category = request.GET.get('category', '')
        beneficiary = request.GET.get('beneficiary', '')
        daterange = request.GET.get('daterange', '')
        mode = request.GET.get('mode', '')
        status = request.GET.get('status', '')
        search_query = request.GET.get("search", '').strip()

        filterData = flag1 = Q(created_by=user,is_deleted = False)
        filter_remaining_amount = Q(created_by=user, is_deleted=False, status="Pending")
        start_date = timezone.now().date().replace(day=1)

        if search_query:
            if search_query.isdigit():
                # Try to filter by amount
                filterData &= Q(amount=search_query)
            else:
                # If filtering by amount fails, filter by beneficiary and description
                filterData &= Q(
                    Q(beneficiary__icontains=search_query) |
                    Q(description__icontains=search_query)
                )

        if beneficiary:
            filterData &= Q(beneficiary__iexact=beneficiary.title())
        if type:
            filterData &= Q(type__in=type)
        if category:
            filterData &= Q(category=category)
        if mode:
            filterData &= Q(mode=mode)
        if status:
            filterData &= Q(status=status)

        if daterange:
            date = daterange.split(" - ")
            startdate = date[0].strip()
            enddate = date[1].strip()
            start_date = datetime.strptime(startdate, "%d/%m/%Y")
            end_date = datetime.strptime(enddate, "%d/%m/%Y")
            filterData &= Q(date__gte=start_date, date__lte=end_date)

        if filterData == flag1:
            search_query = datetime.now().strftime("%B %Y")
            now = datetime.now()
            current_year = now.year
            current_month = now.month
            filterData &= Q(date__year=current_year, date__month=current_month)

        transaction_data = Transaction.objects.filter(filterData).order_by('date')

        income = expense = emi = investment = pending_amount = paid_amount = total = 0

        for i in transaction_data:
            if i.type == "Income":
                income += i.amount
            elif i.type == "Expense":
                expense += i.amount

            if i.category == "Investment":
                investment += i.amount
            elif i.category == "EMI":
                emi += i.amount

            if i.status == "Completed":
                paid_amount += i.amount
            elif i.status == "Pending":
                pending_amount += i.amount
        print(start_date)
        filter_remaining_amount &= Q(date__lt=start_date)

        previous_pending = sum(trn.amount for trn in Transaction.objects.filter(filter_remaining_amount))

        transaction_calculation = {
            "income": income,
            "expense": expense,
            "emi": emi,
            "investment": investment,
            "pending_amount": pending_amount,
            "paid_amount": paid_amount,
            "previous_pending":previous_pending,
            "total": income - expense
        }
        CATEGORIES = ['Shopping', 'Food', 'Investment', 'Utilities', 'Groceries', 'Entertainment', 'EMI', 'Salary','Other']

        return render(request, "transaction/transactionDetails.html", {
            "user": user,
            "transaction_data": transaction_data,
            "transaction_calculation": transaction_calculation,
            "data":{
                "type": type,
                "category": category,
                "beneficiary": beneficiary,
                "daterange": daterange,
                "mode":mode,
                "status":status,
                "key": search_query,
            },
            "categories": CATEGORIES
        })
    except Exception as e:
        print(traceback.print_exc())
        messages.error(request, f"An error occurred: try again after some time")
        return render(request, "transaction/transactionDetails.html", {
             "user": user,
            "transaction_data": transaction_data,
            "transaction_calculation": transaction_calculation,
            "categories": CATEGORIES,
            "data":{
                "type": type,
                "category": category,
                "beneficiary": beneficiary,
                "daterange": daterange,
                "mode":mode,
                "status":status,
                "key": search_query
            }
        })

@auth_user
def fetch_deleted_transaction(request, user):
    try:
        transaction_detail = Transaction.objects.filter(created_by=user.id,is_deleted =True).order_by('-deleted_at')
        return render(request, 'transaction/deletedTransactions.html', {"data": transaction_detail, "user": user})
    except Exception as e:
        print(traceback.print_exc())
        messages.error(request, f"An error occurred: will get back soon")
        return redirect('home')


@auth_user
def delete_transaction(request, id = None):
    try:
        if request.method == "GET":
            del_list = [id]
        else:
            del_list = request.POST.getlist('record_ids','')
        print(del_list)
        for id in del_list:
            entry = Transaction.objects.get(id=id)
            entry.is_deleted = True
            entry.deleted_at = datetime.now()
            entry.save()

    # in case of emi source is not null



        messages.success(request, f'Transaction deleted')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        messages.error(request, f"An error occurred: will get back soon")
        return redirect('transaction-detail')


def undo_transaction(request, id=None):
    try:
        if request.method == "GET":
            undo_list = [id]
        else:
            undo_list = request.POST.getlist('record_ids', '')

        for id in undo_list:
            entry = Transaction.objects.get(id=id)
            if entry.source_id is not None:
                product = FinancialProduct.objects.get(id = entry.source_id)
                if product.is_deleted:
                    product.is_deleted = False
                    product.save()

            entry.is_deleted = False
            entry.deleted_at = None
            entry.save()
        messages.success(request, f'Transaction Reversed')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        messages.error(request, f"An error occurred: will get back soon")
        return redirect('getDeletedEntries')


def update_transaction_status(request, id):
    try:
        if request.method == "GET":
            trasaction_list = [id]
        else:
            trasaction_list = request.POST.getlist('record_ids', '')

        for id in trasaction_list:
            entry = Transaction.objects.get(id=id)
            entry.status = "Completed" if entry.status == "Pending" else "Pending"
            entry.save()
        messages.success(request, f'Transaction Status Updated')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        messages.error(request, f"An error occurred: will get back soon")
        return redirect('transaction-detail')



