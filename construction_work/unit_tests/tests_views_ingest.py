""" Test ingest views """
import datetime
import os

import pytz
from django.test import Client, TestCase
from django.utils import timezone
from rest_framework.exceptions import ErrorDetail

from construction_work.generic_functions.aes_cipher import AESCipher
from construction_work.models import Article, Project, project
from construction_work.unit_tests.mock_data import TestData


class BaseTestIngestViews(TestCase):
    """Base for ingest view tests"""

    def setUp(self):
        """Setup for all ingest view tests"""
        token = AESCipher(
            "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", os.getenv("AES_SECRET")
        ).encrypt()
        self.header = {"INGESTAUTHORIZATION": token}
        self.content_type = "application/json"
        self.client = Client()
        self.api_url = "/api/v1/ingest/project"


class TestProjectIngestViews(BaseTestIngestViews):
    """Test project ingest views"""

    def setUp(self):
        """Setup test data"""
        self.test_data = TestData()
        super().setUp()

    def test_add_new_project_success(self):
        """Test add new project via ingest API"""
        project = self.test_data.ingest_projects[0]

        result = self.client.post(
            self.api_url,
            data=project,
            headers=self.header,
            content_type="application/json",
        )
        # Test for correct status code
        self.assertEqual(result.status_code, 200)

        # Test if a new object was created
        db_objects = list(Project.objects.all())
        self.assertEqual(len(db_objects), 1)

    def test_update_project_success(self):
        """Test update existing project via ingest API"""
        first_project = self.test_data.projects[0]
        # Set initial title, to be updated later
        initial_title = "initial title"
        first_project["title"] = initial_title
        Project.objects.create(**first_project)

        data = self.test_data.ingest_projects[0]
        title_and_subtitle = data["title"].split(": ")
        # Update title, keep subtitle the same
        new_title = "updated title"
        data["title"] = f"{new_title}: {title_and_subtitle[1]}"

        result = self.client.post(
            self.api_url,
            data=data,
            headers=self.header,
            content_type="application/json",
        )

        # Test for correct status code
        self.assertEqual(result.status_code, 200)

        # Test if no new object was created
        db_objects = list(Project.objects.all())
        self.assertEqual(len(db_objects), 1)

        # Test if objects was actually updated
        updated_project = db_objects[0]
        self.assertEqual(updated_project.title, new_title)
        self.assertNotEqual(updated_project.title, initial_title)

    def test_project_invalid(self):
        """test invalid project"""
        data = {"bogus": "bogus"}

        result = self.client.post(
            self.api_url,
            data=data,
            headers=self.header,
            content_type="application/json",
        )
        db_objects = list(Project.objects.all())

        self.assertEqual(result.status_code, 400)
        self.assertEqual(len(db_objects), 0)

    def test_get_projects(self):
        """test get project modification dates"""

        # Create projects from mock data
        [Project.objects.create(**x) for x in self.test_data.projects]

        result = self.client.get(
            self.api_url,
            headers=self.header,
            content_type="application/json",
        )

        self.assertEqual(result.status_code, 200)

        # Check if len result equals the amount of objects in the database
        db_objects = list(Project.objects.all())
        self.assertEqual(len(db_objects), 2)

        # Check for expected output
        first_project = self.test_data.projects[0]
        second_project = self.test_data.projects[1]

        expected_result = {
            str(first_project["foreign_id"]): {
                "modification_date": str(first_project["modification_date"]).replace(
                    "T", " "
                )
            },
            str(second_project["foreign_id"]): {
                "modification_date": str(second_project["modification_date"]).replace(
                    "T", " "
                )
            },
        }
        self.assertDictEqual(result.data, expected_result)


class TestArticleIngestViews(BaseTestIngestViews):
    """Test project ingest views"""

    def setUp(self):
        """Setup test data"""
        self.test_data = TestData()
        [Project.objects.create(**x) for x in self.test_data.projects]
        super().setUp()

    def test_add_new_article_success(self):
        """Test add new article via ingest API"""
        article = self.test_data.ingest_articles[0]

        result = self.client.post(
            "/api/v1/ingest/article",
            data=article,
            headers=self.header,
            content_type="application/json",
        )
        # Test for correct status code
        self.assertEqual(result.status_code, 200)

        # Test if a new object was created
        db_objects = list(Article.objects.all())
        self.assertEqual(len(db_objects), 1)

    def test_update_article_success(self):
        """Test update existing project via ingest API"""

        [Article.objects.create(**x) for x in self.test_data.articles]

        data = self.test_data.ingest_articles[0]
        result = self.client.post(
            "/api/v1/ingest/article",
            data=data,
            headers=self.header,
            content_type="application/json",
        )

        # Test for correct status code
        self.assertEqual(result.status_code, 200)

        # Test if no new object was created
        db_objects = list(Article.objects.all())
        self.assertEqual(len(db_objects), 2)

        # Test if objects was actually updated
        updated_article = Article.objects.filter(foreign_id=128).first()
        self.assertEqual(updated_article.title, data["title"])
        self.assertEqual(updated_article.intro, result.data["intro"])
        self.assertEqual(updated_article.body, result.data["body"])

    def test_article_invalid(self):
        data = self.test_data.ingest_articles[1]
        result = self.client.post(
            "/api/v1/ingest/article",
            data=data,
            headers=self.header,
            content_type="application/json",
        )

        # Test for correct status code
        self.assertEqual(result.status_code, 400)
        self.assertDictEqual(
            result.data,
            {
                "projects": [
                    ErrorDetail(string="This list may not be empty.", code="empty")
                ]
            },
        )

    def test_get_articles(self):
        """test get article modification dates"""

        # Create projects from mock data
        [Article.objects.create(**x) for x in self.test_data.articles]

        result = self.client.get(
            "/api/v1/ingest/article",
            headers=self.header,
            content_type="application/json",
        )

        self.assertEqual(result.status_code, 200)

        # Check if len result equals the amount of objects in the database
        db_objects = list(Article.objects.all())
        self.assertEqual(len(db_objects), 2)

        # Check for expected output
        expected_result = {
            "128": {"modification_date": "2023-01-20 00:00:00+00:00"},
            "256": {"modification_date": "2023-01-20 00:00:00+00:00"},
        }
        self.assertDictEqual(result.data, expected_result)


class TestGarbageCollectionView(BaseTestIngestViews):
    def setUp(self):
        """Setup test data"""
        self.test_data = TestData()
        [Project.objects.create(**x) for x in self.test_data.projects]
        [Article.objects.create(**x) for x in self.test_data.articles]
        super().setUp()

    def test_garbage_collector_one(self):
        """One project is active, one project is inactive, one article is removed"""
        etl_epoch = timezone.now() - timezone.timedelta(days=6)
        etl_epoch_string = etl_epoch.strftime("%Y-%m-%d %H:%M:%S.%f")
        project_ids = [2048]
        article_ids = [128]
        data = {
            "etl_epoch_string": etl_epoch_string,
            "project_ids": project_ids,
            "article_ids": article_ids,
        }

        result = self.client.post(
            "/api/v1/ingest/garbagecollector",
            data=data,
            headers=self.header,
            content_type="application/json",
        )

        self.assertEqual(result.status_code, 200)

        project_db_objects = list(Project.objects.all())
        self.assertEqual(project_db_objects[0].active, False)
        self.assertEqual(project_db_objects[1].active, True)

        article_db_objects = list(Article.objects.all())
        self.assertEqual(len(article_db_objects), 1)

        self.assertDictEqual(
            result.data,
            {
                "projects": {"active": 1, "inactive": 1, "deleted": 0, "count": 2},
                "articles": {"deleted": 1, "count": 1},
            },
        )

    def test_garbage_collector_two(self):
        """One project is active, one project is removed, one article is removed"""
        etl_epoch = timezone.now() + timezone.timedelta(days=6)
        unix_epoch = datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
        etl_epoch_string = etl_epoch.strftime("%Y-%m-%d %H:%M:%S.%f")
        project_ids = [2048]
        article_ids = [128]
        data = {
            "etl_epoch_string": etl_epoch_string,
            "project_ids": project_ids,
            "article_ids": article_ids,
        }

        first_project = Project.objects.filter(foreign_id=2048).first()
        first_project.last_seen = unix_epoch
        first_project.deactivate()

        result = self.client.post(
            "/api/v1/ingest/garbagecollector",
            data=data,
            headers=self.header,
            content_type="application/json",
        )

        self.assertEqual(result.status_code, 200)

        project_db_objects = list(Project.objects.all())
        self.assertEqual(len(project_db_objects), 1)
        self.assertEqual(project_db_objects[0].active, True)

        article_db_objects = list(Article.objects.all())
        self.assertEqual(len(article_db_objects), 1)

        self.assertDictEqual(
            result.data,
            {
                "projects": {"active": 1, "inactive": 0, "deleted": 1, "count": 1},
                "articles": {"deleted": 1, "count": 1},
            },
        )
