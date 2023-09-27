""" unit_tests """

import os

from django.test import Client, TestCase

from construction_work.api_messages import Messages
from construction_work.generic_functions.aes_cipher import AESCipher
from construction_work.models import FirebaseToken, Project, firebase_token
from construction_work.models.device import Device
from construction_work.unit_tests.mock_data import TestData

messages = Messages()


class TestApiDeviceRegistration(TestCase):
    """Test device registration"""

    def setUp(self):
        """Setup test db"""
        self.data = TestData()
        for project in self.data.projects:
            Project.objects.create(**project)

        self.url = "/api/v1/device/register"
        app_token = os.getenv("APP_TOKEN")
        aes_secret = os.getenv("AES_SECRET")
        self.token = AESCipher(app_token, aes_secret).encrypt()

    def tearDown(self) -> None:
        FirebaseToken.objects.all().delete()
        return super().tearDown()

    def test_registration_ok(self):
        """Test registering a new device"""
        c = Client()
        data = {"firebase_token": "foobar_token", "os": "ios"}
        headers = {"HTTP_DEVICEAUTHORIZATION": self.token, "HTTP_DEVICEID": "0"}
        first_result = c.post(self.url, data, **headers)

        self.assertEqual(first_result.status_code, 200)
        self.assertEqual(
            first_result.data.get("firebase_token"), data.get("firebase_token")
        )
        self.assertEqual(first_result.data.get("os"), data.get("os"))

        # Silent discard second call
        second_result = c.post(self.url, data, **headers)

        self.assertEqual(second_result.status_code, 409)
        self.assertEqual(
            second_result.data.get("firebase_token"), data.get("firebase_token")
        )
        self.assertEqual(second_result.data.get("os"), data.get("os"))

        # Assert only one record in db
        devices = list(FirebaseToken.objects.all())
        self.assertEqual(len(devices), 1)

    def test_delete_registration(self):
        """Test removing a device registration"""
        new_device = Device(device_id="foobar_device")
        new_device.save()
        new_token = FirebaseToken(
            firebase_token="foobar_token", os="ios", device=new_device
        )
        new_token.save()

        # Delete registration
        c = Client()
        headers = {
            "HTTP_DEVICEAUTHORIZATION": self.token,
            "HTTP_DEVICEID": "foobar_device",
        }
        first_result = c.delete(self.url, **headers)

        self.assertEqual(first_result.status_code, 200)
        self.assertDictEqual(
            first_result.data, {"status": False, "result": "Registration removed"}
        )

        # Expect no records in db
        devices = list(FirebaseToken.objects.all())
        self.assertEqual(len(devices), 0)

        # Silently discard not existing registration delete
        second_result = c.delete(self.url, **headers)

        self.assertEqual(second_result.status_code, 200)
        self.assertDictEqual(
            second_result.data, {"status": False, "result": "Registration removed"}
        )

    def test_missing_os_missing(self):
        """Test if missing OS is detected"""
        c = Client()
        data = {"firebase_token": "0"}
        headers = {"HTTP_DEVICEAUTHORIZATION": self.token, "HTTP_DEVICEID": "0"}
        result = c.post(self.url, data, **headers)

        self.assertEqual(result.status_code, 400)
        self.assertDictEqual(
            result.data, {"status": False, "result": messages.invalid_query}
        )

    def test_missing_firebase_token(self):
        """Test is missing token is detected"""
        c = Client()
        data = {"os": "ios"}
        headers = {"HTTP_DEVICEAUTHORIZATION": self.token, "HTTP_DEVICEID": "0"}
        result = c.post(self.url, data, **headers)

        self.assertEqual(result.status_code, 400)
        self.assertDictEqual(
            result.data, {"status": False, "result": messages.invalid_query}
        )

    def test_missing_identifier(self):
        """Test if missing identifier is detected"""
        c = Client()
        headers = {"HTTP_DEVICEAUTHORIZATION": self.token}
        result = c.post(self.url, **headers)

        self.assertEqual(result.status_code, 400)
        self.assertDictEqual(
            result.data, {"status": False, "result": messages.invalid_headers}
        )

    def test_invalid_authorization(self):
        """Test if device authorization went well"""
        c = Client()
        headers = {"HTTP_DEVICEAUTHORIZATION": "foobar", "HTTP_DEVICEID": "0"}
        result = c.post(self.url, **headers)

        self.assertEqual(result.status_code, 403)
        self.assertEqual(result.reason_phrase, "Forbidden")
