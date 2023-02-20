""" UNITTESTS """
import os
from django.test import RequestFactory
from django.test import TestCase
from amsterdam_app_api.GenericFunctions.RequestMustComeFromApp import RequestMustComeFromApp
from amsterdam_app_api.GenericFunctions.AESCipher import AESCipher


class TestRequestMustComeFromApp(TestCase):
    """ UNITTESTS """
    def __init__(self, *args, **kwargs):
        super(TestRequestMustComeFromApp, self).__init__(*args, **kwargs)

    def setUp(self):
        """ Setup test db """
        self.factory = RequestFactory()

    def test_valid_token(self):
        """ Test if token is valid """
        @RequestMustComeFromApp
        def a_view(request):
            return 'success'

        token = AESCipher(os.getenv('APP_TOKEN'), os.getenv('AES_SECRET')).encrypt()
        headers = {'Accept': 'application/json', 'DeviceAuthorization': token}
        request = self.factory.post('/', headers=headers)
        resp = a_view(request)
        self.assertEqual(resp, 'success')

    def test_invalid_token(self):
        """ Test with invalid token """
        @RequestMustComeFromApp
        def a_view(request):  # pragma: no cover
            return 'success'

        headers = {'Accept': 'application/json', 'DeviceAuthorization': 'invalid'}
        request = self.factory.post('/', headers=headers)
        resp = a_view(request)
        self.assertEqual(resp.status_code, 403)

    def test_no_token(self):
        """ Test without a token """
        @RequestMustComeFromApp
        def a_view(request):  # pragma: no cover
            return 'success'

        headers = {'Accept': 'application/json'}
        request = self.factory.post('/', headers=headers)
        resp = a_view(request)
        self.assertEqual(resp.status_code, 403)
