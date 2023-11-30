""" This class is a decorator for APIs specific for project managers. It will check if a correct HTTP_TOKEN is set.
    If the token is valid, the calling function will be executed. If the token is invalid, the HTTP request will
    be aborted with a 401 response

    Usage:

    @isAuthorized
    def example(request):
        <method body>
"""

import functools
import os
from uuid import UUID

import jwt
from django.http import HttpRequest
from django.http.response import HttpResponseForbidden
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from construction_work.generic_functions.aes_cipher import AESCipher, AESException
from construction_work.generic_functions.generic_logger import Logger
from construction_work.models.project_manager import ProjectManager
from main_application.settings import SECRET_KEY

logger = Logger()

AES_SECRET = os.getenv("AES_SECRET")


def get_token_from_request(request: HttpRequest, auth_headers=[]):
    """Get the AES encrypted token from the request"""

    auth_token = None
    for k, v in request.META.items():
        if k in [f"HTTP_{x.upper()}" for x in auth_headers]:
            auth_token = v
            break

    if auth_token is None:
        for k, v in request.META.get("headers", {}).items():
            if k in auth_headers:
                auth_token = v

    return auth_token


class IsAuthorized:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func

    @staticmethod
    def is_valid_auth_token(encrypted_token):
        """Test is ingest token is valid"""
        try:
            decrypted_token = AESCipher(encrypted_token, AES_SECRET).decrypt()
            # Check if token is valid UUID, if not ValueError will be thrown
            UUID(decrypted_token, version=4)
            return True
        except AESException as e:
            logger.error(e)
            return False
        except ValueError as e:
            logger.error(e)
            return False

    def __call__(self, *args, **kwargs):
        request = args[0]

        auth_headers = [
            "IngestAuthorization",
            "DeviceAuthorization",
        ]
        auth_token = get_token_from_request(request, auth_headers)

        if auth_token is None or self.is_valid_auth_token(auth_token) is False:
            return HttpResponseForbidden()

        return self.func(*args, **kwargs)


class ManagerAuthorized:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func

    @staticmethod
    def is_valid_manager_key(encrypted_token):
        """Test is ingest token is valid"""
        try:
            decrypted_token = AESCipher(encrypted_token, AES_SECRET).decrypt()
            # Check if token is valid UUID, if not ValueError will be thrown
            UUID(decrypted_token, version=4)
            # Decrypted token is project manager key, check if it exists
            project_manager = ProjectManager.objects.filter(
                manager_key=decrypted_token
            ).first()
            if project_manager is None:
                return False
            return True
        except AESException as e:
            logger.error(e)
            return False
        except ValueError as e:
            logger.error(e)
            return False

    def __call__(self, *args, **kwargs):
        request = args[0]
        auth_headers = ["UserAuthorization"]
        auth_token = get_token_from_request(request, auth_headers)

        if auth_token is None or self.is_valid_manager_key(auth_token) is False:
            return HttpResponseForbidden()

        return self.func(*args, **kwargs)


class JWTAuthorized:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func

    @staticmethod
    def get_jwt_auth_token(request: HttpRequest):
        """Get the JWT token from the request"""

        jwt_header = "Authorization"

        auth_token = None
        http_token = request.META.get(f"HTTP_{jwt_header.upper()}")
        header_token = request.META.get("headers", {}).get(jwt_header)

        if http_token:
            auth_token = http_token
        elif header_token:
            auth_token = http_token

        if auth_token:
            auth_token = auth_token.encode("utf-8")

        return auth_token

    def __call__(self, *args, **kwargs):
        request = args[0]
        jwt_auth_token = self.get_jwt_auth_token(request)

        if jwt_auth_token is None:
            return HttpResponseForbidden()

        try:
            jwt.decode(jwt_auth_token, SECRET_KEY, algorithms=["HS256"])
        except (InvalidSignatureError, ExpiredSignatureError, Exception) as e:
            logger.error(e)
            return HttpResponseForbidden()

        return self.func(*args, **kwargs)
