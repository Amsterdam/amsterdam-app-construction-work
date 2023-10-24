""" unit_tests """
import json
import os
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.test import Client, RequestFactory, TestCase

from construction_work.api_messages import Messages
from construction_work.generic_functions.aes_cipher import AESCipher
from construction_work.models import Project, ProjectManager
from construction_work.serializers import ProjectManagerSerializer
from construction_work.unit_tests.mock_data import TestData
from construction_work.views.views_project_manager import get as get_project_manager

messages = Messages()

username = "mock"
password = "mock"
email = "mock@localhost"


class TestApiProjectManager(TestCase):
    """unit_tests"""

    def __init__(self, *args, **kwargs):
        super(TestApiProjectManager, self).__init__(*args, **kwargs)
        self.data = TestData()
        self.url = "/api/v1/project/manager"
        self.client = Client()

    def setUp(self):
        """Setup test db"""
        # Create user for token
        self.user = get_user_model().objects.create_user(username=username, password=password, email=email)
        self.user.save()
        response = self.client.post("/api/v1/get-token/", {"username": username, "password": password})
        self.headers_jwt = {"HTTP_AUTHORIZATION": response.data["access"]}

        app_token = os.getenv("APP_TOKEN")
        aes_secret = os.getenv("AES_SECRET")
        self.token = AESCipher(app_token, aes_secret).encrypt()
        self.headers_aes = {"HTTP_USERAUTHORIZATION": self.token, "HTTP_DEVICEID": "0"}

        Project.objects.all().delete()
        project_objs = [Project.objects.create(**x) for x in self.data.projects]

        ProjectManager.objects.all().delete()

        for i, project_manager_data in enumerate(self.data.project_managers):
            serializer = ProjectManagerSerializer(data=project_manager_data)
            if not serializer.is_valid():
                assert False

            project_manager = serializer.save()

            # Update mock data for test
            self.data.project_managers[i]["projects"] = [x.id for x in project_objs]
            self.data.project_managers[i]["manager_key"] = str(project_manager.manager_key)

            # Add related projects to the ProjectManager instance
            project_manager.projects.add(*project_objs)
            project_manager.save()

        self.factory = RequestFactory()

    def test_get_all_project_managers(self):
        """Get all project managers"""
        response = self.client.get(self.url, **self.headers_jwt)
        response_data = response.json()
        # remove db id's from response
        [x.pop("id") for x in response_data]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 2)
        self.assertListEqual(response_data, self.data.project_managers)

    def test_get_single_project_managers(self):
        """Get a single project manager"""
        manager_key = self.data.project_managers[0]["manager_key"]
        response = self.client.get(
            f"{self.url}?manager_key={manager_key}",
            **self.headers_aes,
        )

        expected_result = {
            "projects": [
                {
                    "foreign_id": 2048,
                    "images": [],
                    "subtitle": "subtitle first project",
                    "title": "title first project",
                },
                {
                    "foreign_id": 4096,
                    "images": [],
                    "subtitle": "subtitle second project",
                    "title": "title second project",
                },
            ],
            "manager_key": manager_key,
            "email": "mock0@amsterdam.nl",
        }

        response_data = response.json()
        response_data.pop("id")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response_data, expected_result)

    def test_get_single_project_managers_with_inactive_project(self):
        """Get a single project manager"""
        project = Project.objects.filter(foreign_id=4096).first()
        project.active = False
        project.save()

        manager_key = self.data.project_managers[0]["manager_key"]
        response = self.client.get(f"{self.url}?manager_key={manager_key}", **self.headers_aes)

        expected_result = {
            "projects": [
                {
                    "foreign_id": 2048,
                    "images": [],
                    "subtitle": "subtitle first project",
                    "title": "title first project",
                }
            ],
            "manager_key": manager_key,
            "email": "mock0@amsterdam.nl",
        }

        response_data = response.json()
        response_data.pop("id")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response_data, expected_result)

    def test_get_single_non_existing_project_managers(self):
        response = self.client.get(f"{self.url}?manager_key=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", **self.headers_aes)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, messages.no_record_found)

    def test_get_non_authorized_1(self):
        response = self.client.get(f"{self.url}", **self.headers_aes)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.reason_phrase, "Forbidden")

    def test_get_non_authorized_2(self):
        response = self.client.get(f"{self.url}")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.reason_phrase, "Forbidden")

    def test_delete_project_manager(self):
        manager_key = self.data.project_managers[0]["manager_key"]
        response = self.client.delete(f"{self.url}?manager_key={manager_key}", **self.headers_jwt)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, "Project manager removed")

    def test_delete_project_manager_no_identifier(self):
        response = self.client.delete(self.url, **self.headers_jwt)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, messages.invalid_query)

    def test_delete_non_authorized_1(self):
        response = self.client.delete(self.url, **self.headers_aes)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.reason_phrase, "Forbidden")

    def test_delete_non_authorized_2(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.reason_phrase, "Forbidden")

    # def test_post_project_manager_valid(self):
    #    """Create a new project manager account"""
    #    json_data = '{"email": "mock3@amsterdam.nl", "projects": ["0000000000"]}'
    #
    #    c = Client()
    #    response = c.post(self.url, json_data, content_type="application/json", **self.headers)
    #
    #    self.assertEqual(response.status_code, 200)
    #    self.assertEqual(len(str(response.data["identifier"])), 36)
    #
    # def test_post_project_manager_invalid_email(self):
    #    """Create a new project manager with an invalid email address"""
    #    json_data = '{"email": "mock@example.com", "projects": ["0000000000"]}'
    #
    #    c = Client()
    #    response = c.post(self.url, json_data, content_type="application/json", **self.headers)
    #
    #    self.assertEqual(response.status_code, 422)
    #    self.assertDictEqual(
    #        response.data,
    #        {
    #            "status": False,
    #            "result": "Invalid email, should be <username>@amsterdam.nl",
    #        },
    #    )
    #
    # def test_post_project_manager_no_email(self):
    #    """Create a new project manager without an email address"""
    #    json_data = '{"projects": ["0000000000"]}'
    #
    #    c = Client()
    #    response = c.post(self.url, json_data, content_type="application/json", **self.headers)
    #
    #    self.assertEqual(response.status_code, 422)
    #    self.assertDictEqual(response.data, {"status": False, "result": messages.invalid_query})
    #
    # def test_post_project_manager_invalid_project(self):
    #    """Create a new project manager with an invalid project"""
    #    json_data = '{"email": "mock3@amsterdam.nl", "projects": ["AAAAAAAAAA"]}'
    #
    #    c = Client()
    #    response = c.post(self.url, json_data, content_type="application/json", **self.headers)
    #
    #    self.assertEqual(response.status_code, 404)
    #    self.assertDictEqual(response.data, {"status": False, "result": messages.no_record_found})
    #
    # def test_post_project_manager_update(self):
    #    """Update an existing project manager"""
    #    json_data0 = '{"email": "mock3@amsterdam.nl", "projects": []}'
    #
    #    c = Client()
    #    response = c.post(self.url, json_data0, content_type="application/json", **self.headers)
    #
    #    self.assertEqual(response.status_code, 200)
    #    self.assertEqual(len(str(response.data["identifier"])), 36)
    #
    #    json_data1 = '{"email": "mock3@amsterdam.nl", "projects": ["0000000000"]}'
    #    response = c.post(self.url, json_data1, content_type="application/json", **self.headers)
    #
    #    self.assertEqual(response.status_code, 200)
    #    self.assertDictEqual(response.data, {"status": True, "result": "Project manager updated"})
    #
    # def test_invalid_token(self):
    #    """Test with a invalid JWT token"""
    #
    #    headers = {"Accept": "application/json", "Authorization": "invalid"}
    #    request = self.factory.post("/", headers=headers)
    #    result = get_project_manager(request)
    #    expected_result = {
    #        "result": {"status": True, "result": messages.access_denied},
    #        "status": 403,
    #    }
    #    self.assertDictEqual(result, expected_result)
