from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                str(user.is_active) + str(user.pk) + str(timestamp)
        )


email_verification_token_generator = EmailVerificationTokenGenerator()


def send_email(email, title, body):
    send_mail(
        title,
        body,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    return True


# def encode_user(user, valid_till: datetime.datetime):
#     # encoded_data = jwt.encode(payload={"name": "Dinesh",
#     #                                    'valid_till': str(valid_till)},
#     #                           key='secret',
#     #                           algorithm="HS256")
#
#     generator = PasswordResetTokenGenerator()
#     return generator.make_token(user)
#
#
# def decode_user(user, token: str):
#     """
#     :param token: jwt token
#     :return:
#     """
#     # decoded_data = jwt.decode(jwt=token,
#     #                           key='secret',
#     #                           algorithms=["HS256"])
#     generator = PasswordResetTokenGenerator()
#     print(generator.check_token(user, token))
