from apps.common.constants import EmailText
from apps.common.exceptions import UserException
from apps.user.utils import email_verification_token_generator
from apps.user.utils import send_email
from apps.user.models import User
from django.conf import settings


def send_activation_email(user: User):
    token = email_verification_token_generator.make_token(user)
    activation_url = settings.ACTIVATION_URL.format(user.pk, token)
    send_email(user.email,
               EmailText.ACTIVATION_TITLE,
               EmailText.ACTIVATION_BODY.format(activation_url))


def activate_user(user: User, token: str):
    if email_verification_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return True
    return False
