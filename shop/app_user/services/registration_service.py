import os
import sendgrid
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from python_http_client import exceptions, HTTPError
from six import text_type

SENDGRID_API_KEY = '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'
ADMIN_EMAIL = 'karlvonkrause@protonmail.com'
SUBJECT = 'Активируйте Ваш аккаунт '
SUBJECT_ERROR = 'Ошибка активации аккаунта'


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                text_type(user.pk) + text_type(timestamp) +
                text_type(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()


def _get_token(user):
    return account_activation_token.make_token(user)


def _get_current_site(request):
    return get_current_site(request).domain


def _get_uid(user):
    return urlsafe_base64_encode(force_bytes(user.pk))


def _get_message(request, user):
    message = render_to_string(
        'users/account_activation_email.html', {
            'user': user,
            'domain': _get_current_site(request),
            'uid': _get_uid(user),
            'token': _get_token(user),
        })
    return message


def _get_error_message(user, error_text):
    return f"""
            Ошибка активации аккаунта {user}.\n
            Ошибка ({error_text}) 
            """


def _error_description_message(user, error_text):
    message = Mail(
        from_email=ADMIN_EMAIL,
        to_emails=ADMIN_EMAIL,
        subject=SUBJECT_ERROR,
        html_content=_get_error_message(user, error_text)
    )
    return message


def send_mail_to_verify_account(request, user):
    message = Mail(
        from_email=ADMIN_EMAIL,
        to_emails=user.email,
        subject=SUBJECT,
        html_content=_get_message(request, user)
    )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
    except HTTPError as error_text:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(_error_description_message(user, error_text))
