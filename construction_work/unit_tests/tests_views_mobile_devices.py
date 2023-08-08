""" unit_tests """

import os

from django.test import Client, TestCase

from construction_work.api_messages import Messages
from construction_work.generic_functions.aes_cipher import AESCipher
from construction_work.models import DeviceAccessLog, FirebaseToken, Project
from construction_work.unit_tests.mock_data import TestData

messages = Messages()


class SetUp:
    """Setup test db"""

    def __init__(self):
        self.data = TestData()
        for project in self.data.projects:
            Project.objects.create(**project)


class TestDeviceAccessLog(TestCase):
    """unit_tests"""

    def __init__(self, *args, **kwargs):
        super(TestDeviceAccessLog, self).__init__(*args, **kwargs)
        self.url = "/api/v1/device/register"
        app_token = os.getenv("APP_TOKEN")
        aes_secret = os.getenv("AES_SECRET")
        self.token = AESCipher(app_token, aes_secret).encrypt()

    def setUp(self):
        """Setup test db"""
        SetUp()
        FirebaseToken.objects.all().delete()

    def test_registration_ok(self):
        """Test registration went well"""
        c = Client()
        data = {"firebase_token": "0", "os": "ios"}
        headers = {"HTTP_DEVICEAUTHORIZATION": self.token, "HTTP_DEVICEID": "0"}
        result = c.post(self.url, data, **headers)

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {"status": False, "result": "Registration added"})

        DeviceAccessLog.prune()
        devices = list(FirebaseToken.objects.all())
        self.assertEqual(len(devices), 1)


class TestApiDeviceRegistration(TestCase):
    """unit_tests"""

    def __init__(self, *args, **kwargs):
        super(TestApiDeviceRegistration, self).__init__(*args, **kwargs)
        self.url = "/api/v1/device/register"
        app_token = os.getenv("APP_TOKEN")
        aes_secret = os.getenv("AES_SECRET")
        self.token = AESCipher(app_token, aes_secret).encrypt()

    def setUp(self):
        """Setup test db"""
        SetUp()
        FirebaseToken.objects.all().delete()

    def test_delete_registration(self):
        """Test removing a device registration"""
        c = Client()
        data = {"firebase_token": "0", "os": "ios"}
        headers = {"HTTP_DEVICEAUTHORIZATION": self.token, "HTTP_DEVICEID": "0"}
        result = c.post(self.url, data, **headers)

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {"status": False, "result": "Registration added"})

        # Delete registration
        result = c.delete(self.url, **headers)

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {"status": False, "result": "Registration removed"})

        # Assert only one record in db
        devices = list(FirebaseToken.objects.all())
        self.assertEqual(len(devices), 0)

        # Silently discard not existing registration delete
        result = c.delete(self.url, **headers)

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {"status": False, "result": "Registration removed"})

    def test_registration_ok(self):
        """Test registering a new device"""
        c = Client()
        data = {"firebase_token": "0", "os": "ios"}
        headers = {"HTTP_DEVICEAUTHORIZATION": self.token, "HTTP_DEVICEID": "0"}
        result = c.post(self.url, data, **headers)

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {"status": False, "result": "Registration added"})

        # Silent discard second call
        result = c.post(self.url, data, **headers)

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {"status": False, "result": "Registration added"})

        # Assert only one record in db
        devices = list(FirebaseToken.objects.all())
        self.assertEqual(len(devices), 1)

    def test_missing_os_missing(self):
        """Test if missing OS is detected"""
        c = Client()
        data = {"firebase_token": "0"}
        headers = {"HTTP_DEVICEAUTHORIZATION": self.token, "HTTP_DEVICEID": "0"}
        result = c.post(self.url, data, **headers)

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {"status": False, "result": messages.invalid_query})

    def test_missing_firebase_token(self):
        """Test is missing token is detected"""
        c = Client()
        data = {"os": "ios"}
        headers = {"HTTP_DEVICEAUTHORIZATION": self.token, "HTTP_DEVICEID": "0"}
        result = c.post(self.url, data, **headers)

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {"status": False, "result": messages.invalid_query})

    def test_missing_identifier(self):
        """Test if missing identifier is detected"""
        c = Client()
        headers = {"HTTP_DEVICEAUTHORIZATION": self.token}
        result = c.post(self.url, **headers)

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {"status": False, "result": messages.invalid_headers})

    def test_invalid_authorization(self):
        """Test if device authorization went well"""
        c = Client()
        headers = {"HTTP_DEVICEAUTHORIZATION": "invalid", "HTTP_DEVICEID": "0"}
        result = c.post(self.url, **headers)

        self.assertEqual(result.status_code, 403)
        self.assertEqual(result.reason_phrase, "Forbidden")
