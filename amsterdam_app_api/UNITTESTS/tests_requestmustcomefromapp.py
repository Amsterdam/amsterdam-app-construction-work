from django.test import RequestFactory
from django.test import TestCase
from amsterdam_app_api.GenericFunctions.RequestMustComeFromApp import RequestMustComeFromApp
from amsterdam_app_api.GenericFunctions.AESCipher import AESCipher


class TestRequestMustComeFromApp(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestRequestMustComeFromApp, self).__init__(*args, **kwargs)

    def setUp(self):
        self.factory = RequestFactory()

    def test_valid_token(self):
        @RequestMustComeFromApp
        def a_view(request):
            return 'success'

        token = AESCipher('44755871-9ea6-4018-b1df-e4f00466c723', '6886b31dfe27e9306c3d2b553345d9e5').encrypt()
        headers = {'Accept': 'application/json', 'DeviceAuthorization': token}
        request = self.factory.post('/', headers=headers)
        resp = a_view(request)
        self.assertEqual(resp, 'success')

    def test_invalid_token(self):
        @RequestMustComeFromApp
        def a_view(request):  # pragma: no cover
            return 'success'

        headers = {'Accept': 'application/json', 'DeviceAuthorization': 'invalid'}
        request = self.factory.post('/', headers=headers)
        resp = a_view(request)
        self.assertEqual(resp.status_code, 403)

    def test_no_token(self):
        @RequestMustComeFromApp
        def a_view(request):  # pragma: no cover
            return 'success'

        headers = {'Accept': 'application/json'}
        request = self.factory.post('/', headers=headers)
        resp = a_view(request)
        self.assertEqual(resp.status_code, 403)
