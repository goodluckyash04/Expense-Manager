import calendar
from itertools import chain
from django.db.models import Q
from django.contrib import messages
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponseServerError, JsonResponse
from .decorators import auth_user
from .models import *


# ..........................................Expense Management.............................................

@auth_user
def addexpense(request, user):
    try:
        category = request.POST.get("category", "Other")
        payment_type = request.POST.get("payment_type", "Expense")
        payment_date_str = request.POST.get("payment_date", "")

        try:
            payment_date = datetime.strptime(payment_date_str, "%Y-%m-%dT%H:%M")
        except ValueError:
            raise ValidationError("Invalid payment date format. Please use YYYY-MM-DDTHH:MM format.")

        if category == "Loan":
            loan_name = request.POST.get('loan_name', '')
            amount = int(request.POST.get('amount', 0))
            no = int(request.POST.get('description', 1))

            if not loan_name:
                raise ValueError("Loan name is required.")

            if amount <= 0:
                raise ValueError("Loan amount must be greater than zero.")


            existing_loan = Loan.objects.filter(title__iexact=loan_name, created_by=user).first()

            if existing_loan:
                # Loan with the same name and user already exists, use the existing one
                loan_data = existing_loan
                created = False
            else:
                # Loan with the same name and user does not exist, create a new one
                loan_data, created = Loan.objects.get_or_create(
                    title=loan_name,
                    created_by=user,
                    defaults={
                        'amount': amount,
                        'started_on': payment_date_str
                    }
                )


            if created:
                loanData = loan_data
                current_month = payment_date.month
                current_year = payment_date.year

                for i in range(1, no + 1):
                    # Calculate the desired date manually (4th of every month)
                    desired_month = current_month + i
                    desired_year = current_year + (desired_month - 1) // 12
                    desired_month = (desired_month - 1) % 12 + 1
                    desired_date = datetime(desired_year, desired_month, 4)

                    desired_date_str = desired_date.strftime('%Y-%m-%dT%H:%M')

                    Payment.objects.create(
                        payment_type='Expense',
                        category="EMI",
                        payment_date=desired_date_str,
                        amount=amount / no,
                        description=f"EMI {i}({loan_name})",
                        payment_for="Myself",
                        payment_by=user
                    )

                    EMI.objects.create(
                        loan=loanData,
                        paid_on=desired_date_str,
                        amount=-(amount / no),
                        note=f"EMI {i}",
                    )
            else:
                messages.error(request, "Loan Exist")
                return redirect('home')
        else:
            payment_for = request.POST.get("payment_for", "Myself").title()
            amount = int(request.POST.get("amount", 0))
            description = request.POST.get("description", "")

            if amount <= 0:
                raise ValueError("Expense amount must be greater than zero.")

            Payment.objects.create(
                payment_type=payment_type,
                category=category,
                payment_date=payment_date_str,
                amount=amount,
                description=description,
                payment_for=payment_for,
                payment_by=user
            )
        messages.success(request, f'{payment_type} added Succesfully')
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
        print(str(e))
        return HttpResponseServerError()


@auth_user
def editEntry(request, id):
    try:
        entry = get_object_or_404(Payment, id=id)
        if request.method == "GET":
            return JsonResponse({
                "payment_type": entry.payment_type,
                "category": entry.category,
                "payment_date": entry.payment_date,
                "amount": entry.amount,
                "description": entry.description,
                "payment_for": entry.payment_for,
            })

        entry.category = request.POST.get("category", entry.category)
        entry.payment_date = request.POST.get("payment_date", entry.payment_date)
        entry.amount = request.POST.get("amount", entry.amount)
        entry.description = request.POST.get("description", entry.description)
        entry.payment_for = request.POST.get("payment_for", entry.payment_for).title()
        entry.save()

        messages.success(request, "Entry updated successfully")
    except ObjectDoesNotExist:
        messages.error(request, "Entry not found")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@auth_user
def reports(request, user):
    try:
        payment_data = Payment.objects.filter(payment_by=user).order_by('payment_date')

        total, expense = calculate_total_expense(payment_data)

        return render(request, "reports.html", {
            "user": user,
            "paymentData": payment_data,
            "total": total,
            "expenseTotal": expense
        })
    except Exception as e:
        messages.error(request, f"An error occurred: will get back soon")
        return render(request, "reports.html", {
            "user": user,
            "paymentData": [],
            "total": 0,
            "expenseTotal": 0
        })


@auth_user
def currentMonthreports(request, user):
    try:
        current_year = datetime.now().year
        current_month = datetime.now().month

        paymentData = Payment.objects.filter(payment_by=user, payment_date__month=current_month,
                                             payment_date__year=current_year).order_by('-payment_date')

        current_month_name = calendar.month_name[current_month]
        total, expenseTotal = calculate_total_expense(paymentData)

        return render(request, "reports.html", {
            "user": user,
            "paymentData": paymentData,
            "expenseTotal": expenseTotal,
            "total": total,
            "key": f"{current_month_name} {current_year}"
        })
    except Exception as e:
        messages.error(request, f"An error occurred: will get back soon")
        return redirect('reports')


@auth_user
def search_report(request, user):
    try:
        try:
            paymentData = Payment.objects.filter(payment_by=user).filter(amount=request.GET.get("search", ''))
        except:
            paymentData1 = Payment.objects.filter(payment_by=user).filter(
                payment_for__icontains=request.GET.get("search", '').title())
            paymentData2 = Payment.objects.filter(payment_by=user).filter(
                description__icontains=request.GET.get("search", ''))
            paymentData = list(chain(paymentData1, paymentData2))
        total, expenseTotal = calculate_total_expense(paymentData)

        return render(request, "reports.html", {
            "user": user,
            "paymentData": paymentData,
            "expenseTotal": expenseTotal,
            "total": total,
            "key": request.GET.get("search", '')
        })
    except Exception as e:
        messages.error(request, f"An error occurred: will get back soon")
        return redirect('reports')


@auth_user
def filter_report(request, user):
    try:
        payment_type = request.GET.getlist('payment_type', [])
        category = request.GET.get('category', '')
        payment_for = request.GET.get('payment_for', '')
        startdate = request.GET.get('startdate', '')
        enddate = request.GET.get('enddate', '')

        filterData = Q(payment_by=user)

        if payment_for:
            filterData &= Q(payment_for__iexact=payment_for.title())
        if payment_type:
            filterData &= Q(payment_type__in=payment_type)
        if category:
            filterData &= Q(category=category)
        if startdate and enddate:
            end_date = datetime.strptime(enddate, "%Y-%m-%d")
            to_date = end_date + timedelta(days=1)
            filterData &= Q(payment_date__range=[startdate, to_date.strftime("%Y-%m-%d")])

        paymentData = Payment.objects.filter(filterData)

        total, expenseTotal = calculate_total_expense(paymentData)

        return render(request, "reports.html", {
            "user": user,
            "paymentData": paymentData.order_by("payment_date"),
            "total": total,
            "expenseTotal": expenseTotal,
            "data": {
                "payment_type": payment_type,
                "category": category,
                "payment_for": payment_for,
                "startdate": startdate,
                "enddate": enddate,
            },
        })
    except Exception as e:
        messages.error(request, f"An error occurred: will get back soon")
        return redirect('reports')


@auth_user
def deleteentry(request, id):
    try:
        entry = Payment.objects.get(id=id)
        DeletePayment.objects.create(
            payment_type=entry.payment_type,
            category=entry.category,
            payment_date=entry.payment_date,
            amount=entry.amount,
            description=entry.description,
            payment_for=entry.payment_for,
            payment_by=entry.payment_by
        )
        entry.delete()
        messages.success(request,
                         f'succesfully deleted entry {entry.amount} from {entry.payment_date.strftime("%d-%b-%Y")}')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        messages.error(request, f"An error occurred: will get back soon")
        return redirect('reports')


@auth_user
def delete_records(request):
    try:
        del_list = request.POST.getlist('record_ids')
        for i in del_list:
            entry = Payment.objects.get(id=i)
            DeletePayment.objects.create(
                payment_type=entry.payment_type,
                category=entry.category,
                payment_date=entry.payment_date,
                amount=entry.amount,
                description=entry.description,
                payment_for=entry.payment_for,
                payment_by=entry.payment_by
            )
            entry.delete()
        messages.success(request, f'succesfully deleted')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        messages.error(request, f"An error occurred: will get back soon")
        return redirect('reports')


@auth_user
def getDeletedEntries(request, user):
    try:
        deletePay = DeletePayment.objects.filter(payment_by=user.id).order_by('-deleted_at')
        return render(request, 'deleteExpense.html', {"data": deletePay, "user": user})
    except Exception as e:
        messages.error(request, f"An error occurred: will get back soon")
        return redirect('reports')


@auth_user
def undoDelEntries(request, id, user):
    try:
        entry = DeletePayment.objects.get(id=id)
        Payment.objects.create(
            payment_type=entry.payment_type,
            category=entry.category,
            payment_date=entry.payment_date,
            amount=entry.amount,
            description=entry.description,
            payment_for=entry.payment_for,
            payment_by=user
        )
        entry.delete()
        messages.success(request,
                         f'succesfully Undo entry {entry.amount} from {entry.payment_date.strftime("%d-%b-%Y")}')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        messages.error(request, f"An error occurred: will get back soon")
        return redirect('getDeletedEntries')


def undoMultipleDelEntries(request, user):
    try:
        undo_list = request.POST.getlist('record_ids')
        for i in undo_list:
            entry = DeletePayment.objects.get(id=i)
            Payment.objects.create(
                payment_type=entry.payment_type,
                category=entry.category,
                payment_date=entry.payment_date,
                amount=entry.amount,
                description=entry.description,
                payment_for=entry.payment_for,
                payment_by=user
            )
            entry.delete()
        messages.success(request, f'succesfully Undo entry')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        messages.error(request, f"An error occurred: will get back soon")
        return redirect('getDeletedEntries')


def calculate_total_expense(payment_data):
    total = 0
    expense_total = 0

    for payment in payment_data:
        if payment.payment_type == "Expense" or payment.category == "Debit":
            total -= payment.amount
        else:
            total += payment.amount

        if payment.payment_type != "Loan":
            if payment.payment_type == "Expense":
                expense_total -= payment.amount
            else:
                expense_total += payment.amount

    return total, expense_total
