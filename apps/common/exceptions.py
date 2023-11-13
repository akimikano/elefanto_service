from rest_framework import exceptions
from rest_framework import status


class UserException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class AuthException(exceptions.APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
