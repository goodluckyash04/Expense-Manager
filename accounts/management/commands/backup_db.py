from cryptography.fernet import Fernet
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from django.conf import settings
import base64
from decouple import config
import datetime

class Command(BaseCommand):
    help = 'Backup and send the encrypted database via email'

    def handle(self, *args, **options):
        try:
            print("Starting the backup and encryption process...")
            
            # Perform a database backup
            db_file_path = settings.DATABASES['default']['NAME']  # Assuming the default database settings
            with open(db_file_path, 'rb') as f:
                database_data = f.read()

            print("Backup data generated successfully.")

            # Generate a symmetric encryption key
            encryption_key = base64.b64decode(config('ENCRYPTION_KEY').encode('utf-8'))
            cipher_suite = Fernet(encryption_key)
            # Encrypt the database data
            encrypted_data = cipher_suite.encrypt(database_data)

            print("Data encrypted successfully.")

            # Sending email with the encrypted data as an attachment
            subject = 'Daily Backup'
            message = 'Please find the attached encrypted database backup.'
            from_email = settings.EMAIL_HOST_USER  # Replace with your email address
            recipient_list = [config('RECIEPINT_EMAIL')]  # Replace with the recipient's email address
            email = EmailMessage(subject, message, from_email, recipient_list)
            today = datetime.datetime.today().strftime("%Y%m%d%H%M")
            email.attach(f'{today}.bin', encrypted_data, 'application/octet-stream')
            
            email_sent = email.send()
            if email_sent:
                print("Email sent successfully.")
            else:
                print("Email sending failed.")
        except Exception as e:
            print(f"An error occurred: {e}")



