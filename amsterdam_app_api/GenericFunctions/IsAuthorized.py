import os
import functools
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from amsterdam_app_backend.settings import SECRET_KEY
from amsterdam_app_api.GenericFunctions.AESCipher import AESCipher
from django.http.response import HttpResponseForbidden
from amsterdam_app_api.models import ProjectManager


class IsAuthorized:
    """ This class is a decorator for APIs specific for project managers. It will check if a correct HTTP_TOKEN is set.
        If the token is valid, the calling function will be executed. If the token is invalid, the HTTP request will
        be aborted with a 401 response

        Usage:

        @isAuthorized
        def example(request):
            <method body>
    """

    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func

    def __call__(self, *args, **kwargs):
        try:
            request = args[0]
            http_userauthorization = request.META.get('HTTP_USERAUTHORIZATION', None)
            header_userauthorization = request.META.get('headers', {}).get('UserAuthorization', None)
            jwt_token = request.META.get('HTTP_AUTHORIZATION', None)
            header_jwt_token = str(request.META.get('headers', {}).get('HTTP_AUTHORIZATION', None)).encode('utf-8')

            encrypted_token = http_userauthorization if http_userauthorization is not None else header_userauthorization
            jwt_encrypted_token = jwt_token if jwt_token is not None else header_jwt_token

            if encrypted_token is not None:
                if self.is_valid_AES_token(encrypted_token=encrypted_token):
                    return self.func(*args, **kwargs)
            elif jwt_encrypted_token is not None:
                if self.is_valid_JWT_token(jwt_encrypted_token=jwt_encrypted_token):
                    return self.func(*args, **kwargs)
        except Exception as error:  # pragma: no cover
            pass

        # Access is not allowed, abort with 401
        return HttpResponseForbidden()

    @staticmethod
    def is_valid_AES_token(encrypted_token=None):
        token = AESCipher(encrypted_token, os.getenv('AES_SECRET')).decrypt()
        project_manager = ProjectManager.objects.filter(pk=token).first()
        if project_manager is None:
            return False
        return True

    @staticmethod
    def is_valid_JWT_token(jwt_encrypted_token=None):
        try:
            token_dict = jwt.decode(jwt_encrypted_token, SECRET_KEY, algorithms=["HS256"])
            return isinstance(token_dict, dict)
        except (InvalidSignatureError, ExpiredSignatureError, Exception) as error:
            return False
