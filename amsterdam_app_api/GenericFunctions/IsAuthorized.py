import functools
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
        request = args[0]
        http_userauthorization = request.META.get('HTTP_USERAUTHORIZATION', None)
        header_userauthorization = request.META.get('headers', {}).get('UserAuthorization', None)
        encrypted_token = http_userauthorization if http_userauthorization is not None else header_userauthorization

        if self.is_valid_token(encrypted_token=encrypted_token):
            return self.func(*args, **kwargs)

        # Access is not allowed, abort with 401
        return {'result': 'ACCESS DENIED', 'status_code': 403}

    @staticmethod
    def is_valid_token(encrypted_token=None):
        if encrypted_token is None:
            return False
        token = AESCipher(encrypted_token, '6886b31dfe27e9306c3d2b553345d9e5').decrypt()
        project_manager = ProjectManager.objects.filter(pk=token).first()
        if project_manager is None:
            return False
        return True
