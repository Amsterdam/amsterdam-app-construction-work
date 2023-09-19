""" unit_tests """
import json

from django.db import DEFAULT_DB_ALIAS, connections
from django.test import Client, TestCase

from construction_work.api_messages import Messages
from construction_work.models import Project
from construction_work.unit_tests.mock_data import TestData
from construction_work.generic_functions.generic_logger import Logger

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
