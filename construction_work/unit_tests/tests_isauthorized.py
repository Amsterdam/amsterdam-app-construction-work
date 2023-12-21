""" unit_tests """

import os

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase

from construction_work.generic_functions.aes_cipher import AESCipher
from construction_work.generic_functions.is_authorized import (
    IsAuthorized,
    JWTAuthorized,
    ManagerAuthorized,
)
from construction_work.models import ProjectManager
from construction_work.unit_tests.mock_data import TestData

username = "mock"
password = "unsave"
email = "mock@localhost"


class TestIsAuthorized(TestCase):
    """Unittest for IsAuthorized decorator"""

    def __init__(self, *args, **kwargs):
        super(TestIsAuthorized, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        """Setup test db"""
        # Create user for token
        self.user = get_user_model().objects.create_user(
            username=username, password=password, email=email
        )
        self.user.save()
        response = self.client.post(
            "/api/v1/get-token/", {"username": username, "password": password}
        )
        self.jwt_token = response.data["access"]

        self.factory = RequestFactory()
        ProjectManager.objects.all().delete()
        for project_manager in self.data.project_managers:
            ProjectManager.objects.create(**project_manager)

    def test_valid_token(self):
        """Test with valid app token"""

        project_manager = ProjectManager.objects.first()

        @ManagerAuthorized
        def a_view(request):
            return "success"

        aes_secret = os.getenv("AES_SECRET")
        token = AESCipher(str(project_manager.manager_key), aes_secret).encrypt()

        headers = {"Accept": "application/json", "UserAuthorization": token}
        request = self.factory.post("/", headers=headers)
        resp = a_view(request)
        self.assertEqual(resp, "success")

    def test_valid_token_ingest(self):
        """Test with valid ingestion token"""

        @IsAuthorized
        def a_view(request):
            return "success"

        app_token = os.getenv("APP_TOKEN")
        aes_secret = os.getenv("AES_SECRET")
        token = AESCipher(app_token, aes_secret).encrypt()

        headers = {"Accept": "application/json", "INGESTAUTHORIZATION": token}
        request = self.factory.post("/", headers=headers)
        resp = a_view(request)
        self.assertEqual(resp, "success")

    def test_invalid_token_ingest(self):
        """Test with invalid ingestion token"""

        @IsAuthorized
        def a_view(request):  # pragma: no cover
            return "success"

        headers = {"Accept": "application/json", "INGESTAUTHORIZATION": "bogus"}
        request = self.factory.post("/", headers=headers)
        result = a_view(request)
        self.assertEqual(result.reason_phrase, "Forbidden")

    def test_invalid_token(self):
        """Test with a invalid JWT token"""

        @IsAuthorized
        def a_view(request):  # pragma: no cover
            return "success"

        headers = {"Accept": "application/json", "UserAuthorization": "invalid"}
        request = self.factory.post("/", headers=headers)
        result = a_view(request)
        self.assertEqual(result.status_code, 403)

    def test_no_token(self):
        """Test missing JWT token"""

        @IsAuthorized
        def a_view(request):  # pragma: no cover
            return "success"

        headers = {"Accept": "application/json"}
        request = self.factory.post("/", headers=headers)
        result = a_view(request)
        self.assertEqual(result.reason_phrase, "Forbidden")

    def test_jwt_token_valid(self):
        """Test if JWT token is valid"""

        @JWTAuthorized
        def a_view(request):  # pragma: no cover
            return "success"

        headers = {"Accept": "application/json", "AUTHORIZATION": self.jwt_token}
        request = self.factory.post("/", headers=headers)
        result = a_view(request)
        self.assertEqual(result, "success")

    def test_jwt_token_invalid(self):
        """Test if JWT token is in-valid"""

        @JWTAuthorized
        def a_view(request):  # pragma: no cover
            return "success"

        headers = {"Accept": "application/json", "AUTHORIZATION": "bogus"}
        request = self.factory.post("/", headers=headers)
        result = a_view(request)
        self.assertEqual(result.reason_phrase, "Forbidden")
