""" unit_tests """
import json
import os

from django.db import DEFAULT_DB_ALIAS, connections
from django.test import Client, TestCase

from construction_work.api_messages import Messages
from construction_work.generic_functions.aes_cipher import AESCipher
from construction_work.generic_functions.generic_logger import Logger
from construction_work.models import Project
from construction_work.models.device import Device
from construction_work.unit_tests.mock_data import TestData

messages = Messages()
logger = Logger()


class BaseTestApi(TestCase):
    """Abstract base class for API tests"""

    def __init__(self, methodName) -> None:
        self.data = TestData()
        self.maxDiff = None
        super().__init__(methodName)

    def setUp(self):
        # Create needed database extensions
        connection = connections[DEFAULT_DB_ALIAS]
        cursor = connection.cursor()
        cursor.execute("CREATE EXTENSION pg_trgm")
        cursor.execute("CREATE EXTENSION unaccent")

        for project in self.data.projects:
            Project.objects.create(**project)


class TestApiProjects(BaseTestApi):
    """unit_tests"""

    def test_method_not_allowed(self):
        """Http method not allowed"""
        c = Client()
        headers = {"HTTP_DEVICEID": "1"}
        response = c.post("/api/v1/projects", **headers)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertDictEqual(result, {"detail": 'Method "POST" not allowed.'})

    def test_projects_all(self):
        """Get all projects"""
        c = Client()
        headers = {"HTTP_DEVICEID": "6"}
        response = c.get("/api/v1/projects", **headers)
        results = json.loads(response.content)
        for result in results["result"]:
            for i in range(0, len(self.data.projects), 1):
                if result["project_id"] == self.data.projects[i]["project_id"]:
                    self.data.projects[i]["followed"] = False
        print(json.dumps(results, indent=4))

        expected_result = {
            "status": True,
            "result": [
                {
                    "project_id": "0000000000",
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
                    "publication_date": "1970-01-01",
                    "subtitle": "subtitle",
                    "title": "title",
                    "followed": False,
                    "coordinates": {"lat": 0.0, "lon": 0.0},
                    "recent_articles": [],
                },
                {
                    "project_id": "0000000001",
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
                    "publication_date": "1970-01-02",
                    "subtitle": "subtitle",
                    "title": "title",
                    "followed": False,
                    "coordinates": {"lat": 1.0, "lon": 1.0},
                    "recent_articles": [],
                },
            ],
            "page": {"number": 1, "size": 10, "totalElements": 2, "totalPages": 1},
            "_links": {"self": {"href": "http://localhost/api/v1/projects"}},
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(results, expected_result)


class TestApiProjectsSearch(BaseTestApi):
    """unit_tests"""

    def test_search(self):
        """Test search in projects"""
        c = Client()
        query = {
            "text": "title",
            "query_fields": "title,subtitle",
            "fields": "title,subtitle",
            "page_size": 1,
            "page": 1,
        }
        response = c.get("/api/v1/projects/search", query)
        result = json.loads(response.content)
        expected_result = {
            "status": True,
            "result": [{"title": "title", "subtitle": "subtitle", "score": 1.333}],
            "page": {"number": 1, "size": 1, "totalElements": 2, "totalPages": 2},
            "_links": {
                "self": {"href": "http://localhost/api/v1/projects/search"},
                "next": {"href": "http://localhost/api/v1/projects/search?page=2"},
            },
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, expected_result)

    def test_no_text(self):
        """Test search without a string"""
        c = Client()
        query = {
            "query_fields": "title,subtitle",
            "fields": "title,subtitle",
            "page_size": 1,
            "page": 1,
        }
        response = c.get("/api/v1/projects/search", query)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(
            result, {"status": False, "result": messages.invalid_query}
        )

    def test_invalid_model_field(self):
        """Test search on invalid model fields"""
        c = Client()
        query = {
            "text": "mock",
            "query_fields": "mock",
            "fields": "title,subtitle",
            "page_size": 1,
            "page": 1,
        }
        response = c.get("/api/v1/projects/search", query)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(
            result, {"status": False, "result": messages.no_such_field_in_model}
        )

    def test_invalid_model_return_field(self):
        """Test search on invalid return fields"""
        c = Client()
        query = {
            "text": "mock",
            "query_fields": "title,subtitle",
            "fields": "mock",
            "page_size": 1,
            "page": 1,
        }
        response = c.get("/api/v1/projects/search", query)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(
            result, {"status": False, "result": messages.no_such_field_in_model}
        )


class TestApiProjectDetails(BaseTestApi):
    """unit_tests"""

    def test_method_not_allowed(self):
        """Test http method not allowed"""
        c = Client()
        response = c.post("/api/v1/project/details")
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertDictEqual(result, {"detail": 'Method "POST" not allowed.'})

    def test_invalid_query(self):
        """Invalid query parameters"""
        c = Client()
        headers = {"HTTP_DEVICEID": "0"}
        response = c.get("/api/v1/project/details", **headers)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.data, {"status": False, "result": messages.invalid_query}
        )

    def test_identifier_does_exist(self):
        """Invalid identifier"""
        c = Client()
        headers = {"HTTP_DEVICEID": "0"}
        response = c.get("/api/v1/project/details", {"id": "0000000000"}, **headers)
        result = json.loads(response.content)

        expected_result = {
            "status": True,
            "result": {
                "project_id": "0000000000",
                "identifier": "0000000000",
                "district_name": "Centrum",
                "source_url": "https://amsterdam.nl/@0000000000/page/?AppIdt=app-pagetype&reload=true",
                "active": True,
                "last_seen": result.get("last_seen"),
                "publication_date": "1970-01-01",
                "modification_date": "1970-01-01",
                "title": "title",
                "subtitle": "subtitle",
                "body": {
                    "what": [{"html": "html content", "title": "title"}],
                    "when": [{"html": "html content", "title": "title"}],
                    "work": [{"html": "html content", "title": "title"}],
                    "where": [{"html": "html content", "title": "title"}],
                    "contact": [{"html": "html content", "title": "title"}],
                    "timeline": {},
                    "more-info": [{"html": "html content", "title": "title"}],
                },
                "content_html": "html content",
                "district_id": 5398,
                "coordinates": {"lat": 0.0, "lon": 0.0},
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
                "contacts": [],
                "news": [
                    {
                        "url": "https://localhost/news/0",
                        "identifier": "00000000000",
                        "project_identifier": "00000000000",
                    }
                ],
                "followers": 0,
                "followed": False,
                "meter": None,
                "strides": None,
            },
        }

        logger.debug(response.data)
        self.assertEqual(response.status_code, 200)

        expected_result["result"]["last_seen"] = result["result"]["last_seen"]
        self.assertDictEqual(result, expected_result)

    def test_identifier_does_not_exist(self):
        """Invalid identifier (ii)"""
        c = Client()
        headers = {"HTTP_DEVICEID": "0"}
        response = c.get("/api/v1/project/details", {"id": "does not exist"}, **headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data, {"status": False, "result": messages.no_record_found}
        )


class TestApiProjectFollow(BaseTestApi):
    """Test follow project endpoint"""

    def setUp(self):
        super().setUp()

        self.api_url = "/api/v1/projects/follow"
        app_token = os.getenv("APP_TOKEN")
        aes_secret = os.getenv("AES_SECRET")
        self.token = AESCipher(app_token, aes_secret).encrypt()

    def test_missing_device_id(self):
        """Test missing device id"""
        c = Client()
        project = Project.objects.first()
        project_id = project.project_id

        headers = {
            "HTTP_DEVICEAUTHORIZATION": self.token,
        }
        data = {"project_id": project_id}
        response = c.post(self.api_url, data, **headers)
        self.assertEqual(response.status_code, 400)

    def test_missing_project_id(self):
        """Test missing project id"""
        c = Client()

        headers = {
            "HTTP_DEVICEAUTHORIZATION": self.token,
            "HTTP_DEVICEID": "foobar",
        }
        data = {}
        response = c.post(self.api_url, data, **headers)
        self.assertEqual(response.status_code, 400)

    def test_project_does_not_exist(self):
        """Test call but project does not exist"""
        c = Client()

        headers = {
            "HTTP_DEVICEAUTHORIZATION": self.token,
            "HTTP_DEVICEID": "foobar",
        }
        data = {"project_id": 9999}
        response = c.post(self.api_url, data, **headers)
        self.assertEqual(response.status_code, 404)

    def test_new_device_follows_existing_project(self):
        """Test new device follows existing project"""
        c = Client()
        project = Project.objects.first()
        project_id = project.project_id

        # Test if device did not yet exist
        new_device_id = "foobar"
        device: Device = Device.objects.filter(device_id=new_device_id).first()
        self.assertIsNone(device)

        # Perform API call and check status
        headers = {
            "HTTP_DEVICEAUTHORIZATION": self.token,
            "HTTP_DEVICEID": new_device_id,
        }
        data = {"project_id": project_id}
        response = c.post(self.api_url, data, **headers)
        self.assertEqual(response.status_code, 200)

        # Device should now exist with followed project
        device: Device = Device.objects.filter(device_id=new_device_id).first()
        self.assertIsNotNone(device)
        self.assertIn(project, device.followed_projects.all())

    def test_existing_device_unfollows_existing_project(self):
        """Test unfollow existing project with existing device"""
        # Setup device and follow project
        device_id = "foobar"
        project = Project.objects.first()
        project_id = project.project_id
        device = Device(device_id=device_id)
        device.save()
        device.followed_projects.add(project)

        # Perform API call and check status
        c = Client()
        headers = {
            "HTTP_DEVICEAUTHORIZATION": self.token,
            "HTTP_DEVICEID": device_id,
        }
        data = {"project_id": project_id}
        response = c.delete(
            self.api_url, data=data, content_type="application/json", **headers
        )
        self.assertEqual(response.status_code, 200)

        # Project should not be part of device followed projects
        self.assertNotIn(project, device.followed_projects.all())

    def test_unfollow_not_existing_project(self):
        """Test unfollowing not existing project"""
        # Setup device and follow project
        device_id = "foobar"
        device = Device(device_id=device_id)
        device.save()

        # Perform API call and check status
        c = Client()
        headers = {
            "HTTP_DEVICEAUTHORIZATION": self.token,
            "HTTP_DEVICEID": device_id,
        }
        data = {"project_id": 9999}
        response = c.delete(
            self.api_url, data=data, content_type="application/json", **headers
        )
        self.assertEqual(response.status_code, 404)

    def test_unfollow_project_that_device_is_not_following(self):
        """Test unfollow existing project with existing device"""
        # Setup device and follow project
        project = Project.objects.first()
        project_id = project.project_id

        device_id = "foobar"
        device = Device(device_id=device_id)
        device.save()

        # Perform API call and check status
        c = Client()
        headers = {
            "HTTP_DEVICEAUTHORIZATION": self.token,
            "HTTP_DEVICEID": device_id,
        }
        data = {"project_id": project_id}
        response = c.delete(
            self.api_url, data=data, content_type="application/json", **headers
        )
        self.assertEqual(response.status_code, 200)

        # Device should have no followed projects
        self.assertEqual(0, len(device.followed_projects.all()))
