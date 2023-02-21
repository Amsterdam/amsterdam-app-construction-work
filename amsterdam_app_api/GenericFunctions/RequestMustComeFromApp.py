""" This class is a decorator for APIs specific for devices."""

import os
import functools
from django.http.response import HttpResponseForbidden
from amsterdam_app_api.GenericFunctions.AESCipher import AESCipher

valid_app_token = os.getenv('APP_TOKEN')


class RequestMustComeFromApp:
    """ This class is a decorator for APIs specific for devices. It will check if a correct HTTP_TOKEN is set.
        If the token is valid, the calling function will be executed. If the token is invalid, the HTTP request will
        be aborted with a 401 response

        Usage:

        @RequestMustComeFromApp
        def example(request):
            <method body>
    """

    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func

    def __call__(self, *args, **kwargs):
        request = args[0]

        http_userauthorization = request.META.get('HTTP_DEVICEAUTHORIZATION', None)
        header_userauthorization = request.META.get('headers', {}).get('DeviceAuthorization', None)
        encrypted_token = http_userauthorization if http_userauthorization is not None else header_userauthorization

        if self.is_valid_token(encrypted_token=encrypted_token):
            return self.func(*args, **kwargs)

        # Access is not allowed, abort with 403
        return HttpResponseForbidden()

    @staticmethod
    def is_valid_token(encrypted_token=None):
        """ Check if token is valid """
        if encrypted_token is None:
            return False
        aes_secret = os.getenv('AES_SECRET')
        token = AESCipher(encrypted_token, aes_secret).decrypt()
        if valid_app_token != token:
            return False
        return True
