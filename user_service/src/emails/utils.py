import smtplib
from email.message import EmailMessage

from src.celery import celery
from src.config import settings
from src.emails.templates import RESET_PASS_TEMPLATE, VERIFY_EMAIL_TEMPLATE
from src.exceptions import SMTPServerNotAllowedError
from src.messages import (
    EMAIL_RESET_PASSWORD_SUBJECT,
    EMAIL_VERIFICATION_SUBJECT
)


EMAIL_VERIFY_URL = f'{settings.FRONT_URL}/email_verification/'
PASSWORD_RESET_URL = f'{settings.FRONT_URL}/reset_password/'


def get_email(
    subject: str,
    email_address: str,
    template: str,
    link: str
) -> dict:
    return {
        'Subject': subject,
        'From': settings.SMTP_USER,
        'To': email_address,
        'Content': template.format(subject=subject, link=link)
    }


def dict_to_email(email_data: dict) -> EmailMessage:
    email = EmailMessage()
    email['Subject'] = email_data['Subject']
    email['From'] = email_data['From']
    email['To'] = email_data['To']
    email.set_content(email_data['Content'], subtype='html')
    return email


@celery.task
def send_mail(email_data: dict):
    email = dict_to_email(email_data)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        try:
            server.login(settings.SMTP_USER, settings.SMTP_PASS)
            server.send_message(email)
        except smtplib.SMTPAuthenticationError:
            raise SMTPServerNotAllowedError


def send_verify_email(email_address: str, token: str):
    confirmation_link: str = EMAIL_VERIFY_URL + token
    email = get_email(
        subject=EMAIL_VERIFICATION_SUBJECT,
        email_address=email_address,
        template=VERIFY_EMAIL_TEMPLATE,
        link=confirmation_link
    )
    send_mail.delay(email)


def send_reset_email(email_address: str, token: str):
    reset_link: str = PASSWORD_RESET_URL + token
    email = get_email(
        subject=EMAIL_RESET_PASSWORD_SUBJECT,
        email_address=email_address,
        template=RESET_PASS_TEMPLATE,
        link=reset_link
    )
    send_mail.delay(email)
