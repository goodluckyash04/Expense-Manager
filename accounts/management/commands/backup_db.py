# from django.core.management.base import BaseCommand
# from django.core.management import call_command
# import os
# import datetime

# class Command(BaseCommand):
#     help = 'Backup the database'

#     def handle(self, *args, **options):
#         print("he")
#         backup_dir = 'D:\expense_manager\backup'
#         if not os.path.exists(backup_dir):
#             os.makedirs(backup_dir)

#         backup_file = os.path.join(backup_dir, f'db_backup_{datetime.datetime.now().strftime("%Y-%m-%d")}.json')

#         with open(backup_file, 'w') as f:
#             call_command('dumpdata', stdout=f)
#         print("Backup data generated successfully.")

# Without Storing to system
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.core.mail import EmailMessage,send_mail
import io
import traceback;
import datetime
from django.conf import settings


class Command(BaseCommand):
    help = 'Backup the database and send as an email attachment'
    def handle(self, *args, **options):
        try:
            print("Starting the backup process...")
            in_memory_file = io.BytesIO()  # Use io.StringIO() for text-based data
            
            call_command('dumpdata', stdout=in_memory_file)
            print("Backup data generated successfully.")
            # Sending email with the backup data as an attachment
            subject = 'Daily Database Backup'
            message = 'Please find the attached database backup file.'
            from_email = settings.EMAIL_HOST_USER  # Replace with your email address
            recipient_list = ['yash.goodluck4@gmail.com']  # Replace with the recipient's email address
            email = EmailMessage(subject, message, from_email, recipient_list)
            backup_filename = f'db_backup_{datetime.datetime.now().strftime("%Y-%m-%d")}.json'
            email.attach(backup_filename, in_memory_file.getvalue(), 'application/json')
            
            email_sent = email.send()
            if email_sent:
                print("Email sent successfully.")
            else:
                print("Email sending failed.")
        except:
            print(traceback.print_exc())    

# python manage.py loaddata /path/to/db_backup_YYYY-MM-DD.json


# python3 /path/to/your/manage.py your_custom_command
# python3 manage.py_path file_to_run