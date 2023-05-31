""" UNITTESTS """
from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase
from amsterdam_app_api.models import ProjectManager
from amsterdam_app_api.models import Projects
from amsterdam_app_api.UNITTESTS.mock_data import TestData
from amsterdam_app_api.api_messages import Messages

messages = Messages()

username = "mock"
password = "unsave"
email = "mock@localhost"


class TestApiProjectManager(TestCase):
    """UNITTESTS"""

    def __init__(self, *args, **kwargs):
        super(TestApiProjectManager, self).__init__(*args, **kwargs)
        self.data = TestData()
        self.url = "/api/v1/project/manager"

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
        self.headers = {"HTTP_AUTHORIZATION": response.data["access"]}

        ProjectManager.objects.all().delete()
        for project_manager in self.data.project_manager:
            ProjectManager.objects.create(**project_manager)

        Projects.objects.all().delete()
        for project in self.data.projects:
            Projects.objects.create(**project)

    def test_get_all_project_managers(self):
        """Get all project managers"""
        c = Client()
        response = c.get(self.url, **self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.data, {"status": True, "result": self.data.project_manager}
        )

    def test_get_single_project_managers(self):
        """Get a single project manager"""
        c = Client()
        response = c.get(
            "{url}?id=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa".format(url=self.url),
            **self.headers
        )

        expected_result = [
            {
                "identifier": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                "email": "mock0@amsterdam.nl",
                "projects": [
                    {
                        "identifier": "0000000000",
                        "images": [
                            {
                                "type": "banner",
                                "sources": {
                                    "orig": {
                                        "url": "https://localhost/image.jpg",
                                        "size": "orig",
                                        "filename": "image.jpg",
                                        "image_id": "0000000000",
                                        "description": "",
                                    }
                                },
                            },
                            {
                                "type": "additional",
                                "sources": {
                                    "orig": {
                                        "url": "https://localhost/image.jpg",
                                        "size": "orig",
                                        "filename": "image.jpg",
                                        "image_id": "0000000001",
                                        "description": "",
                                    }
                                },
                            },
                        ],
                        "subtitle": "subtitle",
                        "title": "title",
                    }
                ],
            }
        ]
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, {"status": True, "result": expected_result})

    def test_get_single_project_managers_inactive_project(self):
        """Get a single project manager with an inactive project"""
        project = Projects.objects.filter(pk="0000000000").first()
        project.active = False
        project.save()

        c = Client()
        response = c.get(
            "{url}?id=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa".format(url=self.url),
            **self.headers
        )

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.data,
            {
                "status": True,
                "result": [
                    {
                        "identifier": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                        "email": "mock0@amsterdam.nl",
                        "projects": [],
                    }
                ],
            },
        )

    def test_delete_project_manager_no_identifier(self):
        """Test deleting a project manager without an identifier"""
        c = Client()
        response = c.delete(self.url, **self.headers)

        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(
            response.data, {"status": False, "result": messages.invalid_query}
        )

    def test_delete_project_manager(self):
        """Delete a project manager"""
        c = Client()
        response = c.delete(
            "{url}?id=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa".format(url=self.url),
            **self.headers
        )

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.data, {"status": True, "result": "Project manager removed"}
        )

    def test_post_project_manager_valid(self):
        """Create a new project manager account"""
        json_data = '{"email": "mock3@amsterdam.nl", "projects": ["0000000000"]}'

        c = Client()
        response = c.post(
            self.url, json_data, content_type="application/json", **self.headers
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(str(response.data["identifier"])), 36)

    def test_post_project_manager_invalid_email(self):
        """Create a new project manager with an invalid email address"""
        json_data = '{"email": "mock@example.com", "projects": ["0000000000"]}'

        c = Client()
        response = c.post(
            self.url, json_data, content_type="application/json", **self.headers
        )

        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(
            response.data,
            {
                "status": False,
                "result": "Invalid email, should be <username>@amsterdam.nl",
            },
        )

    def test_post_project_manager_no_email(self):
        """Create a new project manager without an email address"""
        json_data = '{"projects": ["0000000000"]}'

        c = Client()
        response = c.post(
            self.url, json_data, content_type="application/json", **self.headers
        )

        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(
            response.data, {"status": False, "result": messages.invalid_query}
        )

    def test_post_project_manager_invalid_project(self):
        """Create a new project manager with an invalid project"""
        json_data = '{"email": "mock3@amsterdam.nl", "projects": ["AAAAAAAAAA"]}'

        c = Client()
        response = c.post(
            self.url, json_data, content_type="application/json", **self.headers
        )

        self.assertEqual(response.status_code, 404)
        self.assertDictEqual(
            response.data, {"status": False, "result": messages.no_record_found}
        )

    def test_post_project_manager_update(self):
        """Update an existing project manager"""
        json_data0 = '{"email": "mock3@amsterdam.nl", "projects": []}'

        c = Client()
        response = c.post(
            self.url, json_data0, content_type="application/json", **self.headers
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(str(response.data["identifier"])), 36)

        json_data1 = '{"email": "mock3@amsterdam.nl", "projects": ["0000000000"]}'
        response = c.post(
            self.url, json_data1, content_type="application/json", **self.headers
        )

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.data, {"status": True, "result": "Project manager updated"}
        )
