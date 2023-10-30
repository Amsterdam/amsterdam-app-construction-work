""" unit_tests for project manager CRUD APIs """
import os
import uuid

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from construction_work.api_messages import Messages
from construction_work.generic_functions.aes_cipher import AESCipher
from construction_work.models import Project, ProjectManager
from construction_work.serializers import ProjectManagerSerializer
from construction_work.unit_tests.mock_data import TestData

messages = Messages()

username = "mock"
password = "mock"
email = "mock@localhost"


class TestApiProjectManager(TestCase):
    """unit_tests"""

    def __init__(self, *args, **kwargs):
        super(TestApiProjectManager, self).__init__(*args, **kwargs)
        self.data = TestData()
        self.api_url = "/api/v1/project/manager"
        self.client = Client()

    def setUp(self):
        """Setup test data"""

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
        self.project_objs = [Project.objects.create(**x) for x in self.data.projects]

        ProjectManager.objects.all().delete()

        for i, project_manager_data in enumerate(self.data.project_managers):
            serializer = ProjectManagerSerializer(data=project_manager_data)
            if not serializer.is_valid():
                assert False

            project_manager = serializer.save()

            # Update mock data for test
            self.data.project_managers[i]["projects"] = [x.id for x in self.project_objs]
            self.data.project_managers[i]["manager_key"] = str(project_manager.manager_key)

            # Add related projects to the ProjectManager instance
            project_manager.projects.add(*self.project_objs)
            project_manager.save()

    def test_get_all_project_managers(self):
        """Get all project managers"""
        response = self.client.get(self.api_url, **self.headers_jwt)
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
            f"{self.api_url}?manager_key={manager_key}",
            **self.headers_aes,
        )

        expected_result = {
            "projects": [
                {
                    "foreign_id": self.data.projects[0]["foreign_id"],
                    "images": self.data.projects[0]["images"],
                    "subtitle": self.data.projects[0]["subtitle"],
                    "title": self.data.projects[0]["title"],
                },
                {
                    "foreign_id": self.data.projects[1]["foreign_id"],
                    "images": self.data.projects[1]["images"],
                    "subtitle": self.data.projects[1]["subtitle"],
                    "title": self.data.projects[1]["title"],
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
        """Test if inactive projects are omitted from result"""
        project = Project.objects.filter(foreign_id=4096).first()
        project.deactivate()

        manager_key = self.data.project_managers[0]["manager_key"]
        response = self.client.get(f"{self.api_url}?manager_key={manager_key}", **self.headers_aes)

        expected_result = {
            "projects": [
                {
                    "foreign_id": self.data.projects[0]["foreign_id"],
                    "images": self.data.projects[0]["images"],
                    "subtitle": self.data.projects[0]["subtitle"],
                    "title": self.data.projects[0]["title"],
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
        """Test if guard clause 'manager_key' works"""
        response = self.client.get(f"{self.api_url}?manager_key=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", **self.headers_aes)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, messages.no_record_found)

    def test_get_non_authorized_1(self):
        """Test if authorization is done with JWT token"""
        response = self.client.get(f"{self.api_url}", **self.headers_aes)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.reason_phrase, "Forbidden")

    def test_get_non_authorized_2(self):
        """Test if AES/JWT authorization is required"""
        response = self.client.get(f"{self.api_url}")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.reason_phrase, "Forbidden")

    def test_delete_project_manager(self):
        """Delete a project manager account. It should succeed"""
        manager_key = self.data.project_managers[0]["manager_key"]
        response = self.client.delete(f"{self.api_url}?manager_key={manager_key}", **self.headers_jwt)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, "Project manager removed")

    def test_delete_project_manager_no_identifier(self):
        """Test if guard clause 'manager_key' works"""
        response = self.client.delete(self.api_url, **self.headers_jwt)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, messages.invalid_query)

    def test_delete_non_authorized_1(self):
        """Test if authorization is done with JWT token"""
        response = self.client.delete(self.api_url, **self.headers_aes)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.reason_phrase, "Forbidden")

    def test_delete_non_authorized_2(self):
        """Test if AES/JWT authorization is required"""
        response = self.client.delete(self.api_url)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.reason_phrase, "Forbidden")

    def test_post_project_manager_valid(self):
        """Create a new project manager account. It should succeed"""
        data = {"email": "mock@amsterdam.nl", "projects": [x.id for x in self.project_objs]}
        response = self.client.post(self.api_url, data=data, content_type="application/json", **self.headers_jwt)
        response_data = response.json()

        response_data.pop("id")
        data["manager_key"] = response_data["manager_key"]

        self.assertEqual(response.status_code, 200)
        self.assertTrue(uuid.UUID(response_data["manager_key"], version=4))
        self.assertDictEqual(response_data, data)

    def test_post_non_amsterdam_email(self):
        """Test if it's possible to create a project manager without an amsterdam.nl email address. It should fail!"""
        data = {"email": "mock@dummy.nl"}
        response = self.client.post(self.api_url, data=data, content_type="application/json", **self.headers_jwt)
        response_data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response_data, {"email": ["Email must belong to 'amsterdam.nl'"]})

    def test_post_no_email(self):
        """Test if it's possible to create a project manager without an email address. It should fail!"""
        data = {"projects": [x.id for x in self.project_objs]}
        response = self.client.post(self.api_url, data=data, content_type="application/json", **self.headers_jwt)
        response_data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data, messages.invalid_query)

    def test_post_invalid_project(self):
        """Test if it's possible to create a project manager with not existing projects. It should fail!"""
        data = {"email": "mock@amsterdam.nl", "projects": [0]}
        response = self.client.post(self.api_url, data=data, content_type="application/json", **self.headers_jwt)
        response_data = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data, messages.no_record_found)

    def test_post_no_projects(self):
        """Test if it's possible to create a new project manager without any projects"""
        data = {"email": "mock@amsterdam.nl", "projects": []}
        response = self.client.post(self.api_url, data=data, content_type="application/json", **self.headers_jwt)
        response_data = response.json()

        response_data.pop("id")
        data["manager_key"] = response_data["manager_key"]

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response_data, data)

    def test_post_non_authorized_1(self):
        """Test if authorization is done with JWT token"""
        response = self.client.post(self.api_url, **self.headers_aes)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.reason_phrase, "Forbidden")

    def test_post_patch_non_authorized_2(self):
        """Test if AES/JWT authorization is required"""
        response = self.client.post(self.api_url)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.reason_phrase, "Forbidden")

    def test_patch_project_manager(self):
        """Update an existing project manager: remove projects"""
        project_manager = ProjectManager.objects.filter(email="mock0@amsterdam.nl").first()
        projects = list(project_manager.projects.all())
        self.assertEqual(len(projects), 2)

        data = {"manager_key": str(project_manager.manager_key), "email": "mock0@amsterdam.nl", "projects": []}
        response = self.client.patch(self.api_url, data=data, content_type="application/json", **self.headers_jwt)
        response_data = response.json()

        response_data.pop("id")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data["projects"]), 0)

    def test_patch_no_manager_key(self):
        """Test if guard clause 'manager_key' works"""
        data = {}
        response = self.client.patch(self.api_url, data=data, content_type="application/json", **self.headers_jwt)
        response_data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data, messages.invalid_query)

    def test_patch_not_found(self):
        """Test that the to be patch project manager exists"""
        data = {"manager_key": str(uuid.uuid4())}
        response = self.client.patch(self.api_url, data=data, content_type="application/json", **self.headers_jwt)
        response_data = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data, messages.no_record_found)

    def test_patch_non_authorized_1(self):
        """Test if authorization is done with JWT token"""
        project_manager = ProjectManager.objects.filter(email="mock0@amsterdam.nl").first()
        data = {"manager_key": str(project_manager.manager_key)}
        response = self.client.patch(self.api_url, data=data, content_type="application/json", **self.headers_aes)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.reason_phrase, "Forbidden")

    def test_patch_non_authorized_2(self):
        """Test if AES/JWT authorization is required"""
        response = self.client.post(self.api_url)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.reason_phrase, "Forbidden")
