""" unit_tests """

import json

from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase


class BaseTokenTest(TestCase):
    """Base token test"""

    def setUp(self) -> None:
        """Setup test db"""
        self.username = "mock"
        self.password = "unsave"
        self.email = "mock@localhost"

        self.user = get_user_model().objects.create_user(
            username=self.username, password=self.password, email=self.email
        )
        self.user.save()


class SignInTest(BaseTokenTest):
    """Test django signin"""

    def tearDown(self):
        """tear down test db"""
        self.user.delete()

    def test_correct(self):
        """test successful signin"""
        user = authenticate(username=self.username, password=self.password)
        self.assertEqual(user.email, self.email)
        self.assertTrue(user.is_authenticated)

    def test_wrong_username(self):
        """test wrong username"""
        user = authenticate(username="wrong", password=self.password)
        self.assertEqual(user, None)

    def test_wrong_password(self):
        """test wrong password"""
        user = authenticate(username=self.username, password="wrong")
        self.assertEqual(user, None)


class SignInViewTest(BaseTokenTest):
    """Test signin view"""

    def tearDown(self):
        """tear down test db"""
        self.user.delete()

    def test_correct(self):
        """test correct signin"""
        response = self.client.post(
            "/api/v1/get-token/", {"username": self.username, "password": self.password}
        )
        self.assertTrue(len(str(response.data["access"]).split(".")) == 3)
        self.assertTrue(len(str(response.data["refresh"]).split(".")) == 3)

    def test_wrong_username(self):
        """test wrong username"""
        response = self.client.post(
            "/api/v1/get-token/", {"username": "wrong", "password": self.password}
        )
        result = json.loads(response.content.decode("utf-8"))
        expected_result = {
            "detail": "No active account found with the given credentials"
        }
        self.assertDictEqual(result, expected_result)

    def test_wrong_password(self):
        """test wrong password"""
        response = self.client.post(
            "/api/v1/get-token/", {"username": self.username, "password": "wrong"}
        )
        result = json.loads(response.content.decode("utf-8"))
        expected_result = {
            "detail": "No active account found with the given credentials"
        }
        self.assertDictEqual(result, expected_result)


class RefreshTokenViewTest(BaseTokenTest):
    """Test refresh token view"""

    def tearDown(self):
        """tear down test db"""
        self.user.delete()

    def test_correct(self):
        """test correct refresh token"""
        credentials = self.client.post(
            "/api/v1/get-token/", {"username": self.username, "password": self.password}
        )
        self.assertTrue(len(str(credentials.data["access"]).split(".")) == 3)
        self.assertTrue(len(str(credentials.data["refresh"]).split(".")) == 3)

        response = self.client.post(
            "/api/v1/refresh-token/", {"refresh": credentials.data["refresh"]}
        )
        self.assertNotEqual(response.data["access"], credentials.data["access"])
        self.assertTrue(len(str(response.data["access"]).split(".")) == 3)

    def test_incorrect(self):
        """test failed refresh token"""
        response = self.client.post("/api/v1/refresh-token/", {"refresh": "invalid"})
        result = json.loads(response.content.decode("utf-8"))
        expected_result = {
            "detail": "Token is invalid or expired",
            "code": "token_not_valid",
        }
        self.assertDictEqual(result, expected_result)
