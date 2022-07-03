import time
import smtplib

from celery import shared_task

SMTP_PORT = 1025
SMTP_SERVER = "localhost"
SENDER_EMAIL = "my@mail.com"


@shared_task
def send_mails(message: str, emails: list):
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        time.sleep(1)
        for receiver_email in emails:
            message += f'\nSent at {time.asctime()}'
            server.sendmail(SENDER_EMAIL, receiver_email, message)
    return f"Emails sent to {', '.join(emails)}"
