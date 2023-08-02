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
from django.http.response import HttpResponse, HttpResponseForbidden
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from amsterdam_app_api.GenericFunctions.AESCipher import AESCipher, AESException
from main_application.settings import SECRET_KEY


def get_jwtauthorization(request):
    """Get the JWT token from the request"""
    http_jwt_token = request.META.get("HTTP_AUTHORIZATION", None)
    header_jwt_token = request.META.get("headers", {}).get("AUTHORIZATION", None)
    return header_jwt_token.encode("utf-8") if header_jwt_token is not None else http_jwt_token


def get_userauthorization(request):
    """Get the AES encrypted token from the request"""
    http_userauthorization = request.META.get("HTTP_USERAUTHORIZATION", None)
    header_uauth = request.META.get("headers", {}).get("UserAuthorization", None)
    return http_userauthorization if http_userauthorization is not None else header_uauth


def get_ingestauthorization(request):
    """Get the AES encrypted token from the request"""
    http_ingestauthorization = request.META.get("HTTP_INGESTAUTHORIZATION", None)
    header_iauth = request.META.get("headers", {}).get("INGESTAUTHORIZATION", None)
    return http_ingestauthorization if http_ingestauthorization is not None else header_iauth


def is_valid_AES_token(encrypted_token=None):
    """Test if aes token is valid"""
    token = AESCipher(encrypted_token, os.getenv("AES_SECRET")).decrypt()
    if token is None:
        raise AESException("Invalid encrypted token")
    return True


def is_valid_JWT_token(jwt_encrypted_token=None):
    """Test if jwt token is valid"""
    try:
        token_dict = jwt.decode(jwt_encrypted_token, SECRET_KEY, algorithms=["HS256"])
        return isinstance(token_dict, dict)
    except (InvalidSignatureError, ExpiredSignatureError, Exception):
        return False


def is_valid_INGEST_token(encrypted_token=None):
    """Test is ingest token is valid"""
    try:
        token = UUID(AESCipher(encrypted_token, os.getenv("AES_SECRET")).decrypt(), version=4)
        return isinstance(token, UUID)
    except (InvalidSignatureError, ExpiredSignatureError, Exception):
        return False


class IsAuthorized:
    """This class is a decorator for APIs specific for project managers. It will check if a correct HTTP_TOKEN is set.
    If the token is valid, the calling function will be executed. If the token is invalid, the HTTP request will
    be aborted with a 403 response

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

            userauthorization = get_userauthorization(request)
            ingestauthorization = get_ingestauthorization(request)
            jwtauthorization = get_jwtauthorization(request)

            if userauthorization is not None:
                if is_valid_AES_token(encrypted_token=userauthorization):
                    return self.func(*args, **kwargs)
            elif jwtauthorization is not None:
                if is_valid_JWT_token(jwt_encrypted_token=jwtauthorization):
                    return self.func(*args, **kwargs)
            elif ingestauthorization is not None:
                if is_valid_INGEST_token(encrypted_token=ingestauthorization):
                    return self.func(*args, **kwargs)
        except Exception as error:  # pragma: no cover
            return HttpResponse(f"Server error: {error}", status=500)

        # Access is not allowed, abort with 403
        return HttpResponseForbidden()
