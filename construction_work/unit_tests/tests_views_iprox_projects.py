""" unit_tests """
import json
import os
from datetime import datetime

from django.db import DEFAULT_DB_ALIAS, connections
from django.test import Client, TestCase
from freezegun import freeze_time

from construction_work.api_messages import Messages
from construction_work.generic_functions.aes_cipher import AESCipher
from construction_work.generic_functions.date_translation import (
    translate_timezone as tt,
)
from construction_work.generic_functions.generic_logger import Logger
from construction_work.generic_functions.text_search import MIN_QUERY_LENGTH
from construction_work.models import Project
from construction_work.models.article import Article
from construction_work.models.device import Device
from construction_work.models.warning_and_notification import WarningMessage
from construction_work.unit_tests.mock_data import TestData
from construction_work.views.views_iprox_projects import memoize

messages = Messages()
logger = Logger()


class BaseTestApi(TestCase):
    """Abstract base class for API tests"""

    def setUp(self):
        self.data = TestData()
        self.maxDiff = None

        # Create needed database extensions
        connection = connections[DEFAULT_DB_ALIAS]
        cursor = connection.cursor()
        cursor.execute("CREATE EXTENSION pg_trgm")
        cursor.execute("CREATE EXTENSION unaccent")

        # Create device header
        app_token = os.getenv("APP_TOKEN")
        aes_secret = os.getenv("AES_SECRET")
        token = AESCipher(app_token, aes_secret).encrypt()
        self.headers = {"HTTP_DEVICEAUTHORIZATION": token}

        # Create request client
        self.client = Client()

    def tearDown(self) -> None:
        memoize.clear_all_cache()

    def create_project_and_article(self, project_foreign_id, article_pub_date):
        """Create project and article"""
        project_data = self.data.projects[0]
        project_data["foreign_id"] = project_foreign_id
        project = Project.objects.create(**project_data)

        article_data = self.data.articles[0]
        article_data["foreign_id"] = project_foreign_id + 1
        article_data["publication_date"] = article_pub_date
        article = Article.objects.create(**article_data)
        article.projects.add(project)

        return project, article

    def add_article_to_project(self, project: Project, foreign_id, pub_date):
        """Add article to projects"""
        article_data = self.data.articles[0]
        article_data["foreign_id"] = foreign_id
        article_data["publication_date"] = pub_date
        article = Article.objects.create(**article_data)
        article.projects.add(project)
        return article

    def add_warning_to_project(self, project: Project, pub_date):
        """Add warning to project"""
        warning_data = self.data.warning_message
        warning_data["publication_date"] = pub_date
        warning_data["project_id"] = project.pk
        warning = WarningMessage.objects.create(**warning_data)
        warning.save()
        return warning


class TestApiProjects(BaseTestApi):
    """Tests for getting all projects via API"""

    def setUp(self):
        super().setUp()

        self.api_url = "/api/v1/projects"

    def tearDown(self) -> None:
        Project.objects.all().delete()
        Article.objects.all().delete()
        Device.objects.all().delete()
        super().tearDown()

    def test_method_not_allowed(self):
        """Http method not allowed"""
        self.headers["HTTP_DEVICEID"] = 1
        response = self.client.post(self.api_url, **self.headers)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertDictEqual(result, {"detail": 'Method "POST" not allowed.'})

    def test_new_device_should_be_created(self):
        """Test new device should be created"""
        new_device_id = "test_new_device_should_be_created"
        self.headers["HTTP_DEVICEID"] = new_device_id
        self.client.get(self.api_url, **self.headers)

        new_device = Device.objects.filter(device_id=new_device_id).first()
        self.assertIsNotNone(new_device)

    @freeze_time("2023-01-02")
    def assert_projects_sorted_descending_by_recent_article_date(
        self, device_follows_projects: bool
    ):
        """Assert projects sorted descending by recent article date"""
        # Create projects with articles at different times
        project_1, _ = self.create_project_and_article(10, "2023-01-01T12:00:00+00:00")
        self.add_article_to_project(project_1, 12, "2023-01-01T12:20:00+00:00")
        project_2, _ = self.create_project_and_article(20, "2023-01-01T12:35:00+00:00")
        self.add_article_to_project(project_2, 22, "2023-01-01T12:45:00+00:00")
        project_3, _ = self.create_project_and_article(30, "2023-01-01T12:15:00+00:00")
        self.add_article_to_project(project_3, 32, "2023-01-01T12:16:00+00:00")
        project_4, _ = self.create_project_and_article(40, "2023-01-01T12:35:00+00:00")
        self.add_article_to_project(project_4, 42, "2023-01-01T12:30:00+00:00")

        # Create device and follow all projects
        device = Device.objects.create(**self.data.devices[0])
        if device_follows_projects:
            device.followed_projects.set([project_1, project_2, project_3, project_4])

        # Perform request
        self.headers["HTTP_DEVICEID"] = device.device_id
        response = self.client.get(self.api_url, {"page_size": 4}, **self.headers)

        # Default order will be by objects internal pk
        expected_default_foreign_id_order = [
            project_1.pk,
            project_2.pk,
            project_3.pk,
            project_4.pk,
        ]
        default_foreign_id_order = list(Project.objects.values_list("pk", flat=True))
        self.assertEqual(default_foreign_id_order, expected_default_foreign_id_order)

        # Expected projects to be ordered descending by publication date
        expected_foreign_id_order = [
            project_2.pk,
            project_4.pk,
            project_1.pk,
            project_3.pk,
        ]
        response_foreign_id_order = [x["id"] for x in response.data["result"]]
        self.assertEqual(response_foreign_id_order, expected_foreign_id_order)

    def test_followed_projects_sorted_descending_by_recent_article_date(self):
        """Test followed projects sorted descending by recent article date"""
        self.assert_projects_sorted_descending_by_recent_article_date(
            device_follows_projects=True
        )

    def test_not_followed_projects_sorted_descending_by_recent_article_date(self):
        """Test other projects sorted descending by recent article date"""
        self.assert_projects_sorted_descending_by_recent_article_date(
            device_follows_projects=False
        )

    @freeze_time("2023-01-02")
    def assert_project_without_articles_sorted_below_project_with_articles(
        self, device_follows_projects: bool
    ):
        """Assert project without articles sorted below project with articles"""
        # Create project with articles
        project_1, _ = self.create_project_and_article(10, "2023-01-01T12:00:00+00:00")
        self.add_article_to_project(project_1, 12, "2023-01-01T12:20:00+00:00")

        # Create project without articles
        project_data = self.data.projects[0]
        project_data["foreign_id"] = 20
        project_2 = Project.objects.create(**project_data)

        # Create device and follow all projects (if requested)
        device = Device.objects.create(**self.data.devices[0])
        if device_follows_projects:
            device.followed_projects.set([project_1, project_2])

        # Perform request
        self.headers["HTTP_DEVICEID"] = device.device_id
        response = self.client.get(self.api_url, {"page_size": 4}, **self.headers)

        # Expected project without articles on the bottom
        expected_foreign_id_order = [
            project_1.pk,
            project_2.pk,
        ]
        response_foreign_id_order = [x["id"] for x in response.data["result"]]
        self.assertEqual(response_foreign_id_order, expected_foreign_id_order)

    def test_sort_followed_project_without_articles_below_project_with_articles(self):
        """
        Given a list of followed projects:
        When articles are sorted by recent article date,
        and there is a project without articles,
        it should appear on the bottom of the list
        """
        self.assert_project_without_articles_sorted_below_project_with_articles(
            device_follows_projects=True
        )

    def test_sort_not_followed_project_without_articles_below_project_with_articles(
        self,
    ):
        """
        Given a list of not followed projects:
        When articles are sorted by recent article date,
        and there is a project without articles,
        it should appear on the bottom of the list
        """
        self.assert_project_without_articles_sorted_below_project_with_articles(
            device_follows_projects=False
        )

    def test_other_projects_sorted_by_distance_with_lat_lon(self):
        """Test other projects sorted by distance with lat lon"""
        # Setup location
        # - Base location is Amsterdam Central Station
        adam_central_station = (52.379158791458494, 4.899904339167326)
        # - The closest location to the base location
        royal_palace_adam = (52.3731077480929, 4.891371824969558)
        # - The second closest location to the base location
        rijks_museam_adam = (52.36002292836369, 4.8852016757845345)
        # - The furthest location to the base location
        van_gogh_museum_adam = (52.358155575937595, 4.8811891932042055)

        project_1, _ = self.create_project_and_article(10, "2023-01-01T12:00:00+00:00")
        project_1.coordinates = {
            "lat": van_gogh_museum_adam[0],
            "lon": van_gogh_museum_adam[1],
        }
        project_1.save()

        project_2, _ = self.create_project_and_article(20, "2023-01-01T12:15:00+00:00")
        project_2.coordinates = {
            "lat": royal_palace_adam[0],
            "lon": royal_palace_adam[1],
        }
        project_2.save()

        project_3, _ = self.create_project_and_article(30, "2023-01-01T12:30:00+00:00")
        project_3.coordinates = {
            "lat": rijks_museam_adam[0],
            "lon": rijks_museam_adam[1],
        }
        project_3.save()

        # Create device, but don't follow any projects
        device = Device.objects.create(**self.data.devices[0])

        # Perform request
        self.headers["HTTP_DEVICEID"] = device.device_id
        response = self.client.get(
            self.api_url,
            {
                "lat": adam_central_station[0],
                "lon": adam_central_station[1],
                "page_size": 3,
            },
            **self.headers,
        )

        # Expected projects to be ordered from closest to furthest from the base location
        expected_foreign_id_order = [project_2.pk, project_3.pk, project_1.pk]
        response_foreign_id_order = [x["id"] for x in response.data["result"]]
        self.assertEqual(response_foreign_id_order, expected_foreign_id_order)

    def test_pagination(self):
        """Test pagination"""
        # Create a total of 10 projects
        for i in range(1, 10 + 1):
            project_data = self.data.projects[0]
            project_data["foreign_id"] = i * 10
            Project.objects.create(**project_data)
        self.assertEqual(len(Project.objects.all()), 10)

        device = Device.objects.create(**self.data.devices[0])
        self.headers["HTTP_DEVICEID"] = device.device_id

        # With page size of 4, 4 projects should be returned
        response = self.client.get(self.api_url, {"page_size": 4}, **self.headers)
        self.assertEqual(response.data["page"]["number"], 1)
        self.assertEqual(response.data["page"]["size"], 4)
        self.assertEqual(response.data["page"]["totalElements"], 10)
        self.assertEqual(response.data["page"]["totalPages"], 3)
        self.assertEqual(len(response.data["result"]), 4)

        # The next URL should be available with the same pagination settings
        next_url = response.data["_links"]["next"]["href"]

        # With page size of 4, the next 4 projects should be returned
        response = self.client.get(next_url, **self.headers)
        self.assertEqual(response.data["page"]["number"], 2)
        self.assertEqual(response.data["page"]["size"], 4)
        self.assertEqual(response.data["page"]["totalElements"], 10)
        self.assertEqual(response.data["page"]["totalPages"], 3)
        self.assertEqual(len(response.data["result"]), 4)

        next_url = response.data["_links"]["next"]["href"]

        # With page size of 4, the last 2 projects should be returned
        response = self.client.get(next_url, **self.headers)
        self.assertEqual(response.data["page"]["number"], 3)
        self.assertEqual(response.data["page"]["size"], 4)
        self.assertEqual(response.data["page"]["totalElements"], 10)
        self.assertEqual(response.data["page"]["totalPages"], 3)
        self.assertEqual(len(response.data["result"]), 2)


class TestApiProjectsSearch(BaseTestApi):
    """Test searching text in project model"""

    def setUp(self):
        super().setUp()
        self.api_url = "/api/v1/projects/search"
        for project in self.data.projects:
            Project.objects.create(**project)

    def test_no_text(self):
        """Test search without a string"""
        query = {
            "query_fields": "title,subtitle",
            "fields": "title,subtitle",
            "page_size": 1,
            "page": 1,
        }
        response = self.client.get(self.api_url, query, **self.headers)

        self.assertEqual(response.status_code, 400)

    def test_text_to_short(self):
        """Test for text lower than minimal length"""
        query = {
            "text": "x" * (MIN_QUERY_LENGTH - 1),
            "query_fields": "title,subtitle",
            "fields": "title,subtitle",
            "page_size": 1,
            "page": 1,
        }
        response = self.client.get(self.api_url, query, **self.headers)

        self.assertEqual(response.status_code, 400)

    def test_search_in_field_not_part_of_model(self):
        """Test search in field that is not part of the project model"""
        query = {
            "text": "title",
            "query_fields": "foobar",
            "fields": "title,subtitle",
            "page_size": 1,
            "page": 1,
        }
        response = self.client.get(self.api_url, query, **self.headers)

        self.assertEqual(response.status_code, 400)

    def test_invalid_model_return_field(self):
        """Test request return fields that are not part of the model"""
        query = {
            "text": "title",
            "query_fields": "title,subtitle",
            "fields": "foobar",
            "page_size": 1,
            "page": 1,
        }
        response = self.client.get(self.api_url, query, **self.headers)

        self.assertEqual(response.status_code, 400)

    def test_search_project_and_follow_links(self):
        """Test search for projects"""
        search_text = "title"
        query = {
            "text": search_text,
            "query_fields": "title,subtitle",
            "fields": "title,subtitle",
            "page_size": 1,
            "page": 1,
        }
        response = self.client.get(self.api_url, query, **self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["result"]), 1)

        project_data = response.data["result"][0]
        self.assertTrue(search_text in project_data["title"])

        next_page = response.data["_links"]["next"]["href"]

        # Go to next page, and check results
        response = self.client.get(next_page, **self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["result"]), 1)

        project_data = response.data["result"][0]
        self.assertTrue(search_text in project_data["title"])


class TestApiProjectDetails(BaseTestApi):
    """Tests for getting all project details"""

    def setUp(self):
        super().setUp()

        self.api_url = "/api/v1/project/details"

    def test_method_not_allowed(self):
        """Test http method not allowed"""
        response = self.client.post(self.api_url)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertDictEqual(result, {"detail": 'Method "POST" not allowed.'})

    def test_missing_device_id(self):
        """Test call without device id"""
        response = self.client.get(self.api_url, **self.headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, messages.invalid_headers)

    def test_missing_project_id(self):
        """Test call without project id"""
        self.headers["HTTP_DEVICEID"] = "foobar"
        params = {
            "lat": 52.379158791458494,
            "lon": 4.899904339167326,
            "article_max_age": 10,
        }
        response = self.client.get(self.api_url, params, **self.headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, messages.invalid_query)

    def test_create_device_when_it_does_not_exist(self):
        """Test call with device id that does not exist"""
        project = Project.objects.create(**self.data.projects[0])

        new_device_id = "new_foobar_device"
        self.headers["HTTP_DEVICEID"] = new_device_id
        params = {
            "id": project.pk,
            "lat": 52.379158791458494,
            "lon": 4.899904339167326,
            "article_max_age": 10,
        }
        response = self.client.get(self.api_url, params, **self.headers)

        self.assertEqual(response.status_code, 200)

        new_device = Device.objects.filter(device_id=new_device_id).first()
        self.assertIsNotNone(new_device)

    def test_project_does_not_exists(self):
        """Test call when project does not exist"""
        new_device_id = "new_foobar_device"
        self.headers["HTTP_DEVICEID"] = new_device_id
        params = {
            "id": 9999,
            "lat": 52.379158791458494,
            "lon": 4.899904339167326,
            "article_max_age": 10,
        }
        response = self.client.get(self.api_url, params, **self.headers)

        self.assertEqual(response.status_code, 404)

    def test_get_project_details(self):
        """Test getting project details"""
        project = Project.objects.create(**self.data.projects[0])

        new_device_id = "new_foobar_device"
        self.headers["HTTP_DEVICEID"] = new_device_id
        params = {
            "id": project.pk,
            "lat": 52.379158791458494,
            "lon": 4.899904339167326,
            "article_max_age": 10,
        }
        response = self.client.get(self.api_url, params, **self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data["id"], project.pk)


class TestApiProjectFollow(BaseTestApi):
    """Test follow project endpoint"""

    def setUp(self):
        super().setUp()

        self.api_url = "/api/v1/projects/follow"

        for project in self.data.projects:
            Project.objects.create(**project)

    def test_missing_device_id(self):
        """Test missing device id"""
        project = Project.objects.first()
        foreign_id = project.foreign_id

        data = {"foreign_id": foreign_id}
        response = self.client.post(self.api_url, data, **self.headers)
        self.assertEqual(response.status_code, 400)

    def test_missing_foreign_id(self):
        """Test missing foreign id"""
        self.headers["HTTP_DEVICEID"] = "foobar"
        data = {}
        response = self.client.post(self.api_url, data, **self.headers)
        self.assertEqual(response.status_code, 400)

    def test_project_does_not_exist(self):
        """Test call but project does not exist"""
        self.headers["HTTP_DEVICEID"] = "foobar"
        data = {"id": 9999}
        response = self.client.post(self.api_url, data, **self.headers)
        self.assertEqual(response.status_code, 404)

    def test_existing_device_follows_existing_project(self):
        """Test new device follows existing project"""
        project = Project.objects.first()
        project_id = project.pk

        # Setup device and follow project
        device_id = "foobar"
        device = Device(device_id=device_id)
        device.save()

        # Perform API call and check status
        self.headers["HTTP_DEVICEID"] = device_id
        data = {"id": project_id}
        response = self.client.post(self.api_url, data, **self.headers)
        self.assertEqual(response.status_code, 200)

        # Device should now exist with followed project
        device: Device = Device.objects.filter(device_id=device_id).first()
        self.assertIsNotNone(device)
        self.assertIn(project, device.followed_projects.all())

    def test_new_device_follows_existing_project(self):
        """Test new device follows existing project"""
        project = Project.objects.first()
        project_id = project.pk

        # Test if device did not yet exist
        new_device_id = "foobar"
        device: Device = Device.objects.filter(device_id=new_device_id).first()
        self.assertIsNone(device)

        # Perform API call and check status
        self.headers["HTTP_DEVICEID"] = new_device_id
        data = {"id": project_id}
        response = self.client.post(self.api_url, data, **self.headers)
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
        project_id = project.pk
        device = Device(device_id=device_id)
        device.save()
        device.followed_projects.add(project)

        # Perform API call and check status
        self.headers["HTTP_DEVICEID"] = device_id
        data = {"id": project_id}
        response = self.client.delete(
            self.api_url, data=data, content_type="application/json", **self.headers
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
        self.headers["HTTP_DEVICEID"] = device_id
        data = {"id": 9999}
        response = self.client.delete(
            self.api_url, data=data, content_type="application/json", **self.headers
        )
        self.assertEqual(response.status_code, 404)

    def test_unfollow_project_that_device_is_not_following(self):
        """Test unfollow existing project with existing device"""
        # Setup device and follow project
        project = Project.objects.first()
        project_id = project.pk

        device_id = "foobar"
        device = Device(device_id=device_id)
        device.save()

        # Perform API call and check status
        self.headers["HTTP_DEVICEID"] = device_id
        data = {"id": project_id}
        response = self.client.delete(
            self.api_url, data=data, content_type="application/json", **self.headers
        )
        self.assertEqual(response.status_code, 200)

        # Device should have no followed projects
        self.assertEqual(0, len(device.followed_projects.all()))


class TestFollowedProjectArticles(BaseTestApi):
    """Test followed projects articles"""

    def setUp(self):
        super().setUp()

        self.api_url = "/api/v1/projects/followed/articles"

    def test_missing_device_id(self):
        """Test missing device id"""
        self.headers["HTTP_DEVICEID"] = None
        response = self.client.get(self.api_url, **self.headers)
        self.assertEqual(response.status_code, 400)

    def test_device_does_not_exist(self):
        """Test device does not exist"""
        self.headers["HTTP_DEVICEID"] = "foobar"
        response = self.client.get(self.api_url, **self.headers)
        self.assertEqual(response.status_code, 404)

    @freeze_time("2023-01-10")
    def test_get_recent_articles(self):
        """Test get recent articles"""
        # Project with TWO recent articles
        project_1, article_1 = self.create_project_and_article(
            10, "2023-01-08T12:00:00+00:00"
        )
        warning_1 = self.add_warning_to_project(project_1, "2023-01-08T12:00:00+00:00")
        article_2 = self.add_article_to_project(
            project_1, 12, "2023-01-08T12:00:00+00:00"
        )

        # Project with ONE recent article
        project_2, article_3 = self.create_project_and_article(
            20, "2023-01-05T12:00:00+00:00"
        )
        article_4 = self.add_article_to_project(
            project_2, 22, "2023-01-07T12:00:00+00:00"
        )

        # Project with NO recent articles
        project_3, article_5 = self.create_project_and_article(
            30, "2023-01-01T12:00:00+00:00"
        )
        article_6 = self.add_article_to_project(
            project_3, 32, "2023-01-01T12:00:00+00:00"
        )

        # Create device and follow all projects
        device = Device.objects.create(**self.data.devices[0])
        device.followed_projects.set([project_1, project_2, project_3])

        self.headers["HTTP_DEVICEID"] = device.device_id

        def assert_total_returned_articles(max_age=0):
            params = {"article_max_age": max_age}
            _response = self.client.get(self.api_url, params, **self.headers).json()

            _total_returned_articles = 0
            for key in _response:
                article_count = len(_response[key])
                _total_returned_articles += article_count

            return _total_returned_articles, _response

        total_returned_articles, response = assert_total_returned_articles(max_age=3)
        self.assertEqual(total_returned_articles, 4)

        target_tzinfo = datetime.fromisoformat(
            response[str(project_1.pk)][0]["modification_date"]
        ).tzinfo

        expected_result = {
            str(project_1.pk): [
                {
                    "meta_id": {"type": "article", "id": article_1.pk},
                    "modification_date": tt(
                        str(article_1.modification_date), target_tzinfo
                    ),
                },
                {
                    "meta_id": {"type": "article", "id": article_2.pk},
                    "modification_date": tt(
                        str(article_2.modification_date), target_tzinfo
                    ),
                },
                {
                    "meta_id": {"type": "warning", "id": warning_1.pk},
                    "modification_date": tt(
                        str(warning_1.modification_date), target_tzinfo
                    ),
                },
            ],
            str(project_2.pk): [
                {
                    "meta_id": {"type": "article", "id": article_4.pk},
                    "modification_date": tt(
                        str(article_4.modification_date), target_tzinfo
                    ),
                }
            ],
            str(project_3.pk): [],
        }
        self.assertDictEqual(response, expected_result)

        total_returned_articles, response = assert_total_returned_articles(max_age=10)
        self.assertEqual(total_returned_articles, 7)
        expected_result = {
            str(project_1.pk): [
                {
                    "meta_id": {"type": "article", "id": article_1.pk},
                    "modification_date": tt(
                        str(article_1.modification_date), target_tzinfo
                    ),
                },
                {
                    "meta_id": {"type": "article", "id": article_2.pk},
                    "modification_date": tt(
                        str(article_2.modification_date), target_tzinfo
                    ),
                },
                {
                    "meta_id": {"type": "warning", "id": warning_1.pk},
                    "modification_date": tt(
                        str(warning_1.modification_date), target_tzinfo
                    ),
                },
            ],
            str(project_2.pk): [
                {
                    "meta_id": {"type": "article", "id": article_3.pk},
                    "modification_date": tt(
                        str(article_3.modification_date), target_tzinfo
                    ),
                },
                {
                    "meta_id": {"type": "article", "id": article_4.pk},
                    "modification_date": tt(
                        str(article_4.modification_date), target_tzinfo
                    ),
                },
            ],
            str(project_3.pk): [
                {
                    "meta_id": {"type": "article", "id": article_5.pk},
                    "modification_date": tt(
                        str(article_5.modification_date), target_tzinfo
                    ),
                },
                {
                    "meta_id": {"type": "article", "id": article_6.pk},
                    "modification_date": tt(
                        str(article_6.modification_date), target_tzinfo
                    ),
                },
            ],
        }
        self.assertDictEqual(response, expected_result)
