from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Reminder
from django.utils import timezone
from django.contrib import messages
from .decorators import auth_user
from datetime import date
from django.http import JsonResponse, HttpResponseRedirect


@auth_user
def add_reminder(request,user):
    if request.method == "POST":
        # Get form data
        title = request.POST.get('title')
        description = request.POST.get('description')
        reminder_date = request.POST.get('reminder_date')  # Changed to reminder_date
        frequency = request.POST.get('frequency')
        custom_repeat_days = request.POST.get('custom_repeat_days')

        # Convert the reminder date string to a Date object
        reminder_date = timezone.datetime.strptime(reminder_date, "%Y-%m-%d").date()

        # Check for existing reminder with the same title and date
        existing_reminder = Reminder.objects.filter(title=title, reminder_date=reminder_date).first()

        if existing_reminder:
            # If a duplicate reminder exists, add an error message
            messages.error(request, "A reminder with this title and date already exists.")
            return redirect('home')  # Redirect back to the form or to another page

        # Create the reminder object
        reminder = Reminder(
            title=title,
            description=description,
            reminder_date=reminder_date,
            frequency=frequency,
            created_by=user,
            custom_repeat_days=custom_repeat_days if frequency == 'custom' else None
        )

        # Save the reminder to the database
        reminder.save()

        # Redirect or return a success message
        messages.success(request, "Reminder added successfully!")
    return redirect('home')  # Adjust based on where you want to go after saving


@auth_user
def todays_reminder(request, user):
    # Get current month, year, and day
    current_month = date.today().month
    current_year = date.today().year
    current_day = date.today().day
    today = date.today()

    all_reminders = []

    # List to store reminders for this month based on frequency
    reminders = Reminder.objects.filter(created_by=user, is_deleted=False)

    for reminder in reminders:
        if reminder.reminder_date > today:
            continue

        if reminder.frequency == Reminder.DAILY:
            all_reminders.append(reminder)

        elif reminder.frequency == Reminder.MONTHLY:
            # For monthly reminders, check if the day and month match
            if reminder.reminder_date.day == current_day :
                all_reminders.append(reminder)

        elif reminder.frequency == Reminder.YEARLY:
            # For yearly reminders, check if the month and day match
            if reminder.reminder_date.day == current_day and reminder.reminder_date.month == current_month:
                all_reminders.append(reminder)

        elif reminder.frequency == Reminder.CUSTOM:
            # Custom frequency logic: Check if current date is a multiple of the custom interval days
            if reminder.custom_repeat_days:
                # Calculate the number of days between the reminder date and today
                delta_days = (today - reminder.reminder_date).days
                
                # Check if delta_days is a multiple of the custom interval
                if delta_days >= 0 and delta_days % reminder.custom_repeat_days == 0:
                    all_reminders.append(reminder)

    return render(request, 'reminder/viewReminder.html', {"user": user, 'reminders': all_reminders,'key':"today"})

@auth_user
def reminder_list(request, user):

    # List to store reminders for this month based on frequency
    reminders = Reminder.objects.filter(created_by=user, is_deleted=False)

    return render(request, 'reminder/viewReminder.html', {"user": user, 'reminders': reminders, 'key':"all"})


@auth_user
def cancel_reminder(request, user,id):

    # List to store reminders for this month based on frequency
    reminder = Reminder.objects.filter(created_by=user, id=id).first()

    if not reminder:
        # If a duplicate reminder exists, add an error message
        messages.error(request, "A reminder with this id does not exists.")
    reminder.is_deleted = True
    reminder.save()
    messages.success(request, "Reminder Canceled !")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))