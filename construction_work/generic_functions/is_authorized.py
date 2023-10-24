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
from django.http.response import HttpResponse, HttpResponseForbidden
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from construction_work.generic_functions.aes_cipher import AESCipher, AESException
from construction_work.generic_functions.generic_logger import Logger
from main_application.settings import SECRET_KEY

logger = Logger()

AES_SECRET = os.getenv("AES_SECRET")


def get_token_from_request(request: HttpRequest, http_key: str, header_key: str, encode_header: bool = False):
    """Get the AES encrypted token from the request"""
    http_token = request.META.get(http_key, None)
    header_token = request.META.get("headers", {}).get(header_key, None)

    return_token = None
    if http_token:
        return_token = http_token
    elif header_token:
        return_token = header_token
        if encode_header:
            return_token = header_token.encode("utf-8")

    return return_token


# NOTE: Check headers, they don't seem to match their functions...
def get_jwt_auth_token(request: HttpRequest):
    """Get the JWT token from the request"""
    return get_token_from_request(request, "HTTP_AUTHORIZATION", "AUTHORIZATION", encode_header=True)


def get_user_auth_token(request: HttpRequest):
    """Get the AES encrypted UserAuthorization token from the request"""
    return get_token_from_request(request, "HTTP_USERAUTHORIZATION", "UserAuthorization")


def get_ingest_auth_token(request: HttpRequest):
    """Get the AES encrypted INGEST token from the request"""
    return get_token_from_request(request, "HTTP_INGESTAUTHORIZATION", "INGESTAUTHORIZATION")


def is_valid_jwt_token(jwt_encrypted_token):
    """Test if jwt token is valid"""
    try:
        token_dict = jwt.decode(jwt_encrypted_token, SECRET_KEY, algorithms=["HS256"])
        return isinstance(token_dict, dict)
    except (InvalidSignatureError, ExpiredSignatureError, Exception) as e:
        logger.error(e)
        return False


def is_valid_aes_token(encrypted_token):
    """Test if aes token is valid"""
    try:
        AESCipher(encrypted_token, AES_SECRET).decrypt()
        return True
    except AESException as e:
        logger.error(e)
        raise AESException("Invalid encrypted token") from e


def is_valid_ingest_token(encrypted_token):
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

            user_auth_token = get_user_auth_token(request)
            ingest_auth_token = get_ingest_auth_token(request)
            jwt_auth_token = get_jwt_auth_token(request)

            if user_auth_token is not None:
                if is_valid_aes_token(user_auth_token):
                    return self.func(*args, **kwargs)
            elif jwt_auth_token is not None:
                if is_valid_jwt_token(jwt_auth_token):
                    return self.func(*args, **kwargs)
            elif ingest_auth_token is not None:
                if is_valid_ingest_token(ingest_auth_token):
                    return self.func(*args, **kwargs)
        except Exception as error:  # pragma: no cover
            return HttpResponse(f"Server error: {error}", status=500)

        # Access is not allowed, abort with 403
        return HttpResponseForbidden()
