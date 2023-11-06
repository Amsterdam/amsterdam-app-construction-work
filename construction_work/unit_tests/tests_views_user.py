""" unit_tests """
from django.contrib.auth import get_user_model
from django.test import TestCase

from construction_work.api_messages import Messages

messages = Messages()


class SignInTest(TestCase):
    """Test django jwt signin"""

    def setUp(self):
        """Setup test db"""
        self.username = "mock"
        self.password = "unsave"
        self.email = "mock@localhost"

        self.user = get_user_model().objects.create_user(
            username=self.username, password=self.password, email=self.email
        )
        self.user.save()
        response = self.client.post("/api/v1/get-token/", {"username": self.username, "password": self.password})
        self.headers = {"Accept": "application/json", "AUTHORIZATION": response.data["access"]}

        self.api_url = "/api/v1/user/password"

    def tearDown(self):
        """Run teardown setup"""
        self.user = get_user_model().objects.filter(username=self.username).first()
        self.user.delete()

    def test_change_password_valid(self):
        """Test valid password"""
        payload = {
            "username": self.username,
            "old_password": self.password,
            "password": "012345678",
            "password_verify": "012345678",
        }

        response = self.client.post(self.api_url, payload, headers=self.headers)
        self.assertEqual(response.data, "password updated")
        self.assertEqual(response.status_code, 200)

    def test_missing_parameter(self):
        """test missing parameter"""
        payload = {"old_password": self.password, "password": "012345678", "password_verify": "012345678"}

        response = self.client.post(self.api_url, payload, headers=self.headers)
        self.assertEqual(response.data, messages.invalid_query)
        self.assertEqual(response.status_code, 400)

    def test_password_do_not_match(self):
        """Test non-matching passwords"""
        payload = {
            "username": self.username,
            "old_password": self.password,
            "password": "012345678",
            "password_verify": "87654321",
        }

        response = self.client.post(self.api_url, payload, headers=self.headers)
        self.assertEqual(response.data, messages.do_not_match)
        self.assertEqual(response.status_code, 400)

    def test_password_invalid_username(self):
        """test invalid username"""
        payload = {
            "username": "does_not_exist",
            "old_password": self.password,
            "password": "012345678",
            "password_verify": "012345678",
        }

        response = self.client.post(self.api_url, payload, headers=self.headers)
        self.assertEqual(response.data, messages.invalid_username_or_password)
        self.assertEqual(response.status_code, 400)

    def test_password_invalid_password(self):
        """test invalid password"""
        payload = {
            "username": self.username,
            "old_password": "invalid_password",
            "password": "012345678",
            "password_verify": "012345678",
        }

        response = self.client.post(self.api_url, payload, headers=self.headers)
        self.assertEqual(response.data, messages.invalid_username_or_password)
        self.assertEqual(response.status_code, 400)
