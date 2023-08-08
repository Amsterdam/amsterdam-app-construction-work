""" unit_tests """
import json

from django.db import DEFAULT_DB_ALIAS, connections
from django.test import Client, TestCase

from construction_work.api_messages import Messages
from construction_work.models import Project, ProjectDetail
from construction_work.unit_tests.mock_data import TestData

messages = Messages()


class SetUp:
    """Setup test db"""

    def __init__(self):
        # Create needed database extensions
        connection = connections[DEFAULT_DB_ALIAS]
        cursor = connection.cursor()
        cursor.execute("CREATE EXTENSION pg_trgm")
        cursor.execute("CREATE EXTENSION unaccent")

        self.data = TestData()
        for project in self.data.projects:
            Project.objects.create(**project)

        for project_detail in self.data.project_details:
            project_detail["identifier"] = Project.objects.filter(pk=project_detail["identifier"]).first()
            ProjectDetail.objects.create(**project_detail)


class TestApiProjects(TestCase):
    """unit_tests"""

    def __init__(self, *args, **kwargs):
        super(TestApiProjects, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        """Setup test db"""
        SetUp()

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
                if result["identifier"] == self.data.projects[i]["identifier"]:
                    self.data.projects[i]["followed"] = False

        expected_result = {
            "status": True,
            "result": [
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
                    "publication_date": "1970-01-01",
                    "subtitle": "subtitle",
                    "title": "title",
                    "followed": False,
                    "coordinates": {"lat": 0.0, "lon": 0.0},
                    "recent_articles": [],
                },
                {
                    "identifier": "0000000001",
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


class TestApiProjectsSearch(TestCase):
    """unit_tests"""

    def __init__(self, *args, **kwargs):
        super(TestApiProjectsSearch, self).__init__(*args, **kwargs)

    def setUp(self):
        """Setup test db"""
        SetUp()

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
            "result": [{"title": "title", "subtitle": "subtitle", "score": 1.3333333432674408}],
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
        query = {"query_fields": "title,subtitle", "fields": "title,subtitle", "page_size": 1, "page": 1}
        response = c.get("/api/v1/projects/search", query)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(result, {"status": False, "result": messages.invalid_query})

    def test_invalid_model_field(self):
        """Test search on invalid model fields"""
        c = Client()
        query = {"text": "mock", "query_fields": "mock", "fields": "title,subtitle", "page_size": 1, "page": 1}
        response = c.get("/api/v1/projects/search", query)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(result, {"status": False, "result": messages.no_such_field_in_model})

    def test_invalid_model_return_field(self):
        """Test search on invalid return fields"""
        c = Client()
        query = {"text": "mock", "query_fields": "title,subtitle", "fields": "mock", "page_size": 1, "page": 1}
        response = c.get("/api/v1/projects/search", query)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(result, {"status": False, "result": messages.no_such_field_in_model})


class TestApiProjectDetails(TestCase):
    """unit_tests"""

    def __init__(self, *args, **kwargs):
        super(TestApiProjectDetails, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        """Setup test db"""
        SetUp()

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
        self.assertEqual(response.data, {"status": False, "result": messages.invalid_query})

    def test_identifier_does_exist(self):
        """Invalid identifier"""
        c = Client()
        headers = {"HTTP_DEVICEID": "0"}
        response = c.get("/api/v1/project/details", {"id": "0000000000"}, **headers)
        result = json.loads(response.content)
        expected_result = {
            "status": True,
            "result": {
                "identifier": "0000000000",
                "project_type": "brug",
                "body": {
                    "what": [{"html": "html content", "text": "text content", "title": "title"}],
                    "when": [{"html": "html content", "text": "text content", "title": "title"}],
                    "work": [{"html": "html content", "text": "text content", "title": "title"}],
                    "where": [{"html": "html content", "text": "text content", "title": "title"}],
                    "contact": [{"html": "html content", "text": "text content", "title": "title"}],
                    "timeline": {},
                    "more-info": [{"html": "html content", "text": "text content", "title": "title"}],
                },
                "coordinates": {"lat": 0.0, "lon": 0.0},
                "district_id": 0,
                "district_name": "West",
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
                "news": [
                    {
                        "url": "https://localhost/news/0",
                        "identifier": "00000000000",
                        "project_identifier": "00000000000",
                    }
                ],
                "page_id": 0,
                "title": "test0",
                "subtitle": "subtitle",
                "rel_url": "project/0",
                "url": "https://localhost/project/0",
                "last_seen": "2022-07-05T13:02:29.030663",
                "active": True,
                "contacts": [],
                "followers": 0,
                "followed": False,
                "meter": None,
                "strides": None,
            },
        }
        expected_result["result"]["last_seen"] = result["result"]["last_seen"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expected_result)

    def test_identifier_does_not_exist(self):
        """Invalid identifier (ii)"""
        c = Client()
        headers = {"HTTP_DEVICEID": "0"}
        response = c.get("/api/v1/project/details", {"id": "does not exist"}, **headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {"status": False, "result": messages.no_record_found})


class TestApiProjectDetailsSearch(TestCase):
    """unit_tests"""

    def __init__(self, *args, **kwargs):
        super(TestApiProjectDetailsSearch, self).__init__(*args, **kwargs)

    def setUp(self):
        """Setup test db"""
        SetUp()

    def test_search(self):
        """Search with a string"""
        c = Client()
        query = {
            "text": "test0",
            "query_fields": "title,subtitle",
            "fields": "title,subtitle",
            "page_size": 1,
            "page": 1,
        }
        response = c.get("/api/v1/project/details/search", query)
        result = json.loads(response.content)
        expected_result = {
            "status": True,
            "result": [{"title": "test0", "subtitle": "subtitle", "score": 1.0}],
            "page": {"number": 1, "size": 1, "totalElements": 2, "totalPages": 2},
            "_links": {
                "self": {"href": "http://localhost/api/v1/project/details/search"},
                "next": {"href": "http://localhost/api/v1/project/details/search?page=2"},
            },
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, expected_result)

    def test_no_text(self):
        """Search without a string"""
        c = Client()
        query = {"query_fields": "title,subtitle", "fields": "title,subtitle", "page_size": 1, "page": 1}
        response = c.get("/api/v1/project/details/search", query)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(result, {"status": False, "result": messages.invalid_query})

    def test_invalid_model_field(self):
        """Search on invalid model field"""
        c = Client()
        query = {"text": "mock", "query_fields": "mock", "fields": "title,subtitle", "page_size": 1, "page": 1}
        response = c.get("/api/v1/project/details/search", query)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(result, {"status": False, "result": messages.no_such_field_in_model})

    def test_invalid_model_return_field(self):
        """Request invalid return field"""
        c = Client()
        query = {"text": "mock", "query_fields": "title,subtitle", "fields": "mock", "page_size": 1, "page": 1}
        response = c.get("/api/v1/project/details/search", query)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(result, {"status": False, "result": messages.no_such_field_in_model})
