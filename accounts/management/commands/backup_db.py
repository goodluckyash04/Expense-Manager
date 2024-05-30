import traceback

from cryptography.fernet import Fernet
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from django.conf import settings
import base64
import datetime
import os

from django.db.models import Q

from accounts.models import Task, Transaction, LedgerTransaction, FinancialProduct


# from decouple import config

class Command(BaseCommand):
    help = 'Backup and send the encrypted database via email'

    def handle(self, *args, **options):
        try:
            print("Starting the backup and encryption process...")
            today = datetime.datetime.now(datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=5, minutes=30)))
            models_to_check = [
                (Transaction, Q(updated_at__date=today)),
                (LedgerTransaction, Q(updated_at__date=today)),
                (FinancialProduct, Q(updated_at__date=today)),
                (Task, Q(updated_at__date=today))
            ]

            changes_detected = False

            for model, query in models_to_check:
                if model.objects.filter(query).exists():
                    changes_detected = True
                    break
            print("changes_detected",changes_detected)
            due_tasks = Task.objects.filter(complete_by_date__lte=today.date(),status = 'Pending')

            task_list = []
            for task in due_tasks:
                task_list.append(task.name+'-'+task.description)
            list_string = "\n".join(task_list)
            task_email = EmailMessage(
                'Task Reminder',
                f'Reminder for task:\n {list_string}',
                settings.EMAIL_HOST_USER,
                [settings.RECIEPINT_EMAIL]
            )
            print(today.date())
            if task_list:
                task_email.send()
            # Perform a database backup
            db_file_path = settings.DATABASES['default']['NAME']  # Assuming the default database settings
            with open(db_file_path, 'rb') as f:
                database_data = f.read()

            print("Backup data generated successfully.")

            # Generate a symmetric encryption key
            encryption_key = base64.b64decode(settings.ENCRYPTION_KEY.encode('utf-8'))
            cipher_suite = Fernet(encryption_key)
            # Encrypt the database data
            encrypted_data = cipher_suite.encrypt(database_data)

            print("Data encrypted successfully.")

            # Sending email with the encrypted data as an attachment
            subject = 'Daily Backup'
            message = 'Please find the attached encrypted database backup.'
            from_email = settings.EMAIL_HOST_USER  # Replace with your email address
            recipient_list = [settings.RECIEPINT_EMAIL]  # Replace with the recipient's email address
            email = EmailMessage(subject, message, from_email, recipient_list)
            today = datetime.datetime.today().strftime("%Y%m%d%H%M")
            email.attach(f'{today}.bin', encrypted_data, 'application/octet-stream')
            if changes_detected:
                email_sent = email.send()
                if email_sent:
                    print("Email sent successfully.")
                else:
                    print("Email sending failed.")
            else:
                print("No changes Made Today")
        except Exception as e:
            print(traceback.print_exc())
            print(f"An error occurred: {e}")

























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
# from django.core.management.base import BaseCommand
# from django.core.management import call_command
# from django.core.mail import EmailMessage,send_mail
# import io
# import traceback;
# import datetime
# from django.conf import settings


# class Command(BaseCommand):
#     help = 'Backup the database and send as an email attachment'
#     def handle(self, *args, **options):
#         try:
#             print("Starting the backup process...")
#             in_memory_file = io.BytesIO()  # Use io.StringIO() for text-based data

#             call_command('dumpdata', stdout=in_memory_file)
#             print("Backup data generated successfully.")
#             # Sending email with the backup data as an attachment
#             subject = 'Daily Database Backup'
#             message = 'Please find the attached database backup file.'
#             from_email = settings.EMAIL_HOST_USER  # Replace with your email address
#             recipient_list = ['yash.goodluck4@gmail.com']  # Replace with the recipient's email address
#             email = EmailMessage(subject, message, from_email, recipient_list)
#             backup_filename = f'db_backup_{datetime.datetime.now().strftime("%Y-%m-%d")}.json'
#             email.attach(backup_filename, in_memory_file.getvalue(), 'application/json')

#             email_sent = email.send()
#             if email_sent:
#                 print("Email sent successfully.")
#             else:
#                 print("Email sending failed.")
#         except:
#             print(traceback.print_exc())






# import io
# import os
# from django.core.management import call_command
# from django.core.mail import EmailMessage
# from django.core.management.base import BaseCommand
# from django.conf import settings

# class Command(BaseCommand):
#     help = 'Backup the database and send as an email attachment'

#     def handle(self, *args, **options):
#         try:
#             print("Starting the backup process...")
#             in_memory_file = io.BytesIO()

#             # Perform a database backup
#             db_file_path = settings.DATABASES['default']['NAME']  # Assuming the default database settings
#             with open(db_file_path, 'rb') as f:
#                 in_memory_file.write(f.read())

#             print("Backup data generated successfully.")

#             # Sending email with the database backup file as an attachment
#             subject = 'Daily Database Backup'
#             message = 'Please find the attached database backup file.'
#             from_email = settings.EMAIL_HOST_USER  # Replace with your email address
#             recipient_list = ['yash.goodluck4@gmail.com']  # Replace with the recipient's email address
#             email = EmailMessage(subject, message, from_email, recipient_list)

#             backup_filename = os.path.basename(db_file_path)
#             email.attach(backup_filename, in_memory_file.getvalue(), 'application/octet-stream')

#             email_sent = email.send()
#             if email_sent:
#                 print("Email sent successfully.")
#             else:
#                 print("Email sending failed.")
#         except Exception as e:
#             print(f"An error occurred: {e}")













# python manage.py loaddata /path/to/db_backup_YYYY-MM-DD.json


# python3 /path/to/your/manage.py your_custom_command
# python3 manage.py_path file_to_run