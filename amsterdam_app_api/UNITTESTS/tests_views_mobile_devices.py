import json
import os
from django.test import Client
from django.test import TestCase
from amsterdam_app_api.UNITTESTS.mock_data import TestData
from amsterdam_app_api.GenericFunctions.AESCipher import AESCipher
from amsterdam_app_api.models import FirebaseTokens
from amsterdam_app_api.api_messages import Messages
from amsterdam_app_api.models import Projects

messages = Messages()


class SetUp:
    def __init__(self):
        self.data = TestData()
        for project in self.data.projects:
            Projects.objects.create(**project)


class TestApiDeviceRegistration(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestApiDeviceRegistration, self).__init__(*args, **kwargs)
        self.url = '/api/v1/device/register'
        app_token = os.getenv('APP_TOKEN')
        aes_secret = os.getenv('AES_SECRET')
        self.token = AESCipher(app_token, aes_secret).encrypt()

    def setUp(self):
        SetUp()
        FirebaseTokens.objects.all().delete()

    def test_delete_registration(self):
        c = Client()
        data = {'firebase_token': '0', 'os': 'ios'}
        headers = {"HTTP_DEVICEAUTHORIZATION": self.token, 'HTTP_DEVICEID': '0'}
        result = c.post(self.url, data, **headers)

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': False, 'result': 'Registration added'})

        # Delete registration
        result = c.delete(self.url, **headers)

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': False, 'result': 'Registration removed'})

        # Assert only one record in db
        devices = list(FirebaseTokens.objects.all())
        self.assertEqual(len(devices), 0)

        # Silently discard not existing registration delete
        result = c.delete(self.url, **headers)

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': False, 'result': 'Registration removed'})

    def test_registration_ok(self):
        c = Client()
        data = {'firebase_token': '0', 'os': 'ios'}
        headers = {"HTTP_DEVICEAUTHORIZATION": self.token, 'HTTP_DEVICEID': '0'}
        result = c.post(self.url, data, **headers)

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': False, 'result': 'Registration added'})

        # Silent discard second call
        result = c.post(self.url, data, **headers)

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': False, 'result': 'Registration added'})

        # Assert only one record in db
        devices = list(FirebaseTokens.objects.all())
        self.assertEqual(len(devices), 1)

    def test_missing_os_missing(self):
        c = Client()
        data = {'firebase_token': '0'}
        headers = {"HTTP_DEVICEAUTHORIZATION": self.token, 'HTTP_DEVICEID': '0'}
        result = c.post(self.url, data, **headers)

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.invalid_query})

    def test_missing_firebase_token(self):
        c = Client()
        data = {'os': 'ios'}
        headers = {"HTTP_DEVICEAUTHORIZATION": self.token, 'HTTP_DEVICEID': '0'}
        result = c.post(self.url, data, **headers)

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.invalid_query})

    def test_missing_identifier(self):
        c = Client()
        headers = {"HTTP_DEVICEAUTHORIZATION": self.token}
        result = c.post(self.url, **headers)

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.invalid_headers})

    def test_invalid_authorization(self):
        c = Client()
        headers = {"HTTP_DEVICEAUTHORIZATION": 'invalid', 'HTTP_DEVICEID': '0'}
        result = c.post(self.url, **headers)

        self.assertEqual(result.status_code, 403)
        self.assertEqual(result.reason_phrase, 'Forbidden')
