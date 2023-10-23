""" unit_tests """
import json
import os

from django.db import DEFAULT_DB_ALIAS, connections
from django.test import Client, TestCase

from construction_work.api_messages import Messages
from construction_work.generic_functions.aes_cipher import AESCipher
from construction_work.generic_functions.generic_logger import Logger
from construction_work.models import Project
from construction_work.models.article import Article
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
    """Tests for getting all projects via API"""

    def tearDown(self) -> None:
        Project.objects.all().delete()
        Article.objects.all().delete()
        Device.objects.all().delete()

    def test_method_not_allowed(self):
        """Http method not allowed"""
        c = Client()
        headers = {"HTTP_DEVICEID": "1"}
        response = c.post("/api/v1/projects", **headers)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertDictEqual(result, {"detail": 'Method "POST" not allowed.'})

    def create_project_and_article(self, project_foreign_id, article_pub_date):
        project_data = self.data.projects[0]
        project_data["foreign_id"] = project_foreign_id
        project = Project.objects.create(**project_data)

        article_data = self.data.articles[0]
        article_data["foreign_id"] = project_foreign_id + 1
        article_data["publication_date"] = article_pub_date
        article = Article.objects.create(**article_data)
        article.projects.add(project)

        return project
    
    def add_article_to_project(self, project: Project, foreign_id, pub_date):
        article_data = self.data.articles[0]
        article_data["foreign_id"] = foreign_id
        article_data["publication_date"] = pub_date
        article = Article.objects.create(**article_data)
        article.projects.add(project)
        return article

    def test_new_device_should_be_created(self):
        c = Client()

        new_device_id = "test_new_device_should_be_created"
        headers = {"HTTP_DEVICEID": new_device_id}
        c.get("/api/v1/projects", **headers)

        new_device = Device.objects.filter(device_id=new_device_id).first()
        self.assertIsNotNone(new_device)

    def assert_projects_sorted_descending_by_recent_article_date(self, device_follows_projects: bool):
        # Reset projects
        Project.objects.all().delete()

        # Create projects with articles at different times
        project_1 = self.create_project_and_article(10, "2023-01-01T12:00:00+00:00")
        self.add_article_to_project(project_1, 12, "2023-01-01T12:20:00+00:00")
        project_2 = self.create_project_and_article(20, "2023-01-01T12:35:00+00:00")
        self.add_article_to_project(project_2, 22, "2023-01-01T12:45:00+00:00")
        project_3 = self.create_project_and_article(30, "2023-01-01T12:15:00+00:00")
        self.add_article_to_project(project_3, 32, "2023-01-01T12:16:00+00:00")
        project_4 = self.create_project_and_article(40, "2023-01-01T12:35:00+00:00")
        self.add_article_to_project(project_4, 42, "2023-01-01T12:30:00+00:00")

        # Create device and follow all projects
        device = Device.objects.create(**self.data.devices[0])
        if device_follows_projects:
            device.followed_projects.set([project_1, project_2, project_3, project_4])

        # Perform request
        c = Client()
        headers = {"HTTP_DEVICEID": device.device_id}
        response = c.get("/api/v1/projects", {"page_size": 4}, **headers)

        # Default order will be by objects internal pk
        expected_default_foreign_id_order = [10, 20, 30, 40]
        default_foreign_id_order = list(
            Project.objects.values_list("foreign_id", flat=True)
        )
        self.assertEqual(default_foreign_id_order, expected_default_foreign_id_order)

        # Expected projects to be ordered descending by publication date
        expected_foreign_id_order = [20, 40, 10, 30]
        response_foreign_id_order = [x["foreign_id"] for x in response.data["result"]]
        self.assertEqual(response_foreign_id_order, expected_foreign_id_order)

    def test_followed_projects_sorted_descending_by_recent_article_date(self):
        self.assert_projects_sorted_descending_by_recent_article_date(device_follows_projects=True)

    def test_other_projects_sorted_descending_by_recent_article_date(self):
        self.assert_projects_sorted_descending_by_recent_article_date(device_follows_projects=False)

    def test_other_projects_sorted_by_distance_with_lat_lon(self):
        # Reset projects
        Project.objects.all().delete()

        # Setup location
        # - Base location is Amsterdam Central Station
        adam_central_station = (52.379158791458494, 4.899904339167326)
        # - The closest location to the base location
        royal_palace_adam = (52.3731077480929, 4.891371824969558)
        # - The second closest location to the base location
        rijks_museam_adam = (52.36002292836369, 4.8852016757845345)
        # - The furthest location to the base location
        van_gogh_museum_adam = (52.358155575937595, 4.8811891932042055)

        project_1 = self.create_project_and_article(10, "2023-01-01T12:00:00+00:00")
        project_1.coordinates = {
            "lat": van_gogh_museum_adam[0],
            "lon": van_gogh_museum_adam[1],
        }
        project_1.save()

        project_2 = self.create_project_and_article(20, "2023-01-01T12:15:00+00:00")
        project_2.coordinates = {
            "lat": royal_palace_adam[0],
            "lon": royal_palace_adam[1],
        }
        project_2.save()

        project_3 = self.create_project_and_article(30, "2023-01-01T12:30:00+00:00")
        project_3.coordinates = {
            "lat": rijks_museam_adam[0],
            "lon": rijks_museam_adam[1],
        }
        project_3.save()

        # Create device, but don't follow any projects
        device = Device.objects.create(**self.data.devices[0])

        # Perform request
        c = Client()
        headers = {"HTTP_DEVICEID": device.device_id}
        response = c.get(
            f"/api/v1/projects",
            {"lat": adam_central_station[0], "lon": adam_central_station[1], "page_size": 3},
            **headers,
        )

        # Expected projects to be ordered from closest to furthest from the base location
        expected_foreign_id_order = [20, 30, 10]
        response_foreign_id_order = [x["foreign_id"] for x in response.data["result"]]
        self.assertEqual(response_foreign_id_order, expected_foreign_id_order)
    
    def test_pagination(self):
        # Reset projects
        Project.objects.all().delete()

        # Create a total of 10 projects
        for i in range(1, 10+1):
            project_data = self.data.projects[0]
            project_data["foreign_id"] = i*10
            Project.objects.create(**project_data)
        self.assertEqual(len(Project.objects.all()), 10)

        device = Device.objects.create(**self.data.devices[0])
        c = Client()
        headers = {"HTTP_DEVICEID": device.device_id}
        
        # With page size of 4, 4 projects should be returned
        response = c.get("/api/v1/projects", {"page_size": 4}, **headers)
        self.assertEqual(response.data["page"]["number"], 1)
        self.assertEqual(response.data["page"]["size"], 4)
        self.assertEqual(response.data["page"]["totalElements"], 10)
        self.assertEqual(response.data["page"]["totalPages"], 3)
        self.assertEqual(len(response.data["result"]), 4)

        # The next URL should be available with the same pagination settings
        next_url = response.data["_links"]["next"]["href"]

        # With page size of 4, the next 4 projects should be returned
        response = c.get(next_url, **headers)
        self.assertEqual(response.data["page"]["number"], 2)
        self.assertEqual(response.data["page"]["size"], 4)
        self.assertEqual(response.data["page"]["totalElements"], 10)
        self.assertEqual(response.data["page"]["totalPages"], 3)
        self.assertEqual(len(response.data["result"]), 4)

        next_url = response.data["_links"]["next"]["href"]

        # With page size of 4, the last 2 projects should be returned
        response = c.get(next_url, **headers)
        self.assertEqual(response.data["page"]["number"], 3)
        self.assertEqual(response.data["page"]["size"], 4)
        self.assertEqual(response.data["page"]["totalElements"], 10)
        self.assertEqual(response.data["page"]["totalPages"], 3)
        self.assertEqual(len(response.data["result"]), 2)


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
    """Tests for getting all project details"""
    
    def setUp(self):
        self.data = TestData()

    def test_method_not_allowed(self):
        """Test http method not allowed"""
        c = Client()
        response = c.post("/api/v1/project/details")
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertDictEqual(result, {"detail": 'Method "POST" not allowed.'})

    def test_missing_device_id(self):
        """Test call without device id"""
        c = Client()
        headers = {}
        response = c.get("/api/v1/project/details", **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, messages.invalid_headers)

    def test_missing_project_foreign_id(self):
        """Test call without project foreign id"""
        c = Client()
        headers = {"HTTP_DEVICEID": "foobar"}
        params = {
            "lat": 52.379158791458494,
            "lon": 4.899904339167326,
            "article_max_age": 10,
        }
        response = c.get("/api/v1/project/details", params, **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, messages.invalid_query)

    def test_create_device_when_it_does_not_exist(self):
        """Test call with device id that does not exist"""
        project = Project.objects.create(**self.data.projects[0])
        
        c = Client()
        new_device_id = "new_foobar_device"
        headers = {"HTTP_DEVICEID": new_device_id}
        params = {
            "foreign_id": project.foreign_id,
            "lat": 52.379158791458494,
            "lon": 4.899904339167326,
            "article_max_age": 10,
        }
        response = c.get("/api/v1/project/details", params, **headers)

        self.assertEqual(response.status_code, 200)

        new_device = Device.objects.filter(device_id=new_device_id).first()
        self.assertIsNotNone(new_device)

    def test_project_does_not_exists(self):
        """Test call when project does not exist"""        
        c = Client()
        new_device_id = "new_foobar_device"
        headers = {"HTTP_DEVICEID": new_device_id}
        params = {
            "foreign_id": 9999,
            "lat": 52.379158791458494,
            "lon": 4.899904339167326,
            "article_max_age": 10,
        }
        response = c.get("/api/v1/project/details", params, **headers)

        self.assertEqual(response.status_code, 404)

    def test_get_project_details(self):
        """Test getting project details"""
        project = Project.objects.create(**self.data.projects[0])
        
        c = Client()
        new_device_id = "new_foobar_device"
        headers = {"HTTP_DEVICEID": new_device_id}
        params = {
            "foreign_id": project.foreign_id,
            "lat": 52.379158791458494,
            "lon": 4.899904339167326,
            "article_max_age": 10,
        }
        response = c.get("/api/v1/project/details", params, **headers)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data["foreign_id"], project.foreign_id)


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
        foreign_id = project.foreign_id

        headers = {
            "HTTP_DEVICEAUTHORIZATION": self.token,
        }
        data = {"foreign_id": foreign_id}
        response = c.post(self.api_url, data, **headers)
        self.assertEqual(response.status_code, 400)

    def test_missing_foreign_id(self):
        """Test missing foreign id"""
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
        data = {"foreign_id": 9999}
        response = c.post(self.api_url, data, **headers)
        self.assertEqual(response.status_code, 404)

    def test_new_device_follows_existing_project(self):
        """Test new device follows existing project"""
        c = Client()
        project = Project.objects.first()
        foreign_id = project.foreign_id

        # Test if device did not yet exist
        new_device_id = "foobar"
        device: Device = Device.objects.filter(device_id=new_device_id).first()
        self.assertIsNone(device)

        # Perform API call and check status
        headers = {
            "HTTP_DEVICEAUTHORIZATION": self.token,
            "HTTP_DEVICEID": new_device_id,
        }
        data = {"foreign_id": foreign_id}
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
        foreign_id = project.foreign_id
        device = Device(device_id=device_id)
        device.save()
        device.followed_projects.add(project)

        # Perform API call and check status
        c = Client()
        headers = {
            "HTTP_DEVICEAUTHORIZATION": self.token,
            "HTTP_DEVICEID": device_id,
        }
        data = {"foreign_id": foreign_id}
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
        data = {"foreign_id": 9999}
        response = c.delete(
            self.api_url, data=data, content_type="application/json", **headers
        )
        self.assertEqual(response.status_code, 404)

    def test_unfollow_project_that_device_is_not_following(self):
        """Test unfollow existing project with existing device"""
        # Setup device and follow project
        project = Project.objects.first()
        foreign_id = project.foreign_id

        device_id = "foobar"
        device = Device(device_id=device_id)
        device.save()

        # Perform API call and check status
        c = Client()
        headers = {
            "HTTP_DEVICEAUTHORIZATION": self.token,
            "HTTP_DEVICEID": device_id,
        }
        data = {"foreign_id": foreign_id}
        response = c.delete(
            self.api_url, data=data, content_type="application/json", **headers
        )
        self.assertEqual(response.status_code, 200)

        # Device should have no followed projects
        self.assertEqual(0, len(device.followed_projects.all()))
