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

        project_foreign_id = 1337

        # Set initial title, to be updated later
        first_project = self.test_data.projects[0]
        initial_title = "initial title"
        first_project["foreign_id"] = project_foreign_id
        first_project["title"] = initial_title
        Project.objects.create(**first_project)

        # Update title, keep subtitle the same
        ingest_data = self.test_data.ingest_projects[0]
        ingest_data["foreign_id"] = project_foreign_id
        title_and_subtitle = ingest_data["title"].split(": ")
        new_title = "updated title"
        ingest_data["title"] = f"{new_title}: {title_and_subtitle[1]}"

        result = self.client.post(
            self.api_url,
            data=ingest_data,
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
        self.api_url = "/api/v1/ingest/article"

    def test_add_new_article_success(self):
        """Test add new article via ingest API"""
        article = self.test_data.ingest_articles[0]

        result = self.client.post(
            self.api_url,
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

        article_foreign_id = 1337

        # Setup article with initial title
        article_data = self.test_data.articles[0]
        initial_title = "initial data"
        article_data["foreign_id"] = article_foreign_id
        article_data["title"] = initial_title
        Article.objects.create(**article_data)

        # Update first article with updated title
        ingest_data = self.test_data.ingest_articles[0]
        new_title = "updated title"
        ingest_data["foreign_id"] = article_foreign_id
        ingest_data["title"] = new_title

        result = self.client.post(
            self.api_url,
            data=ingest_data,
            headers=self.header,
            content_type="application/json",
        )

        # Test for correct status code
        self.assertEqual(result.status_code, 200)

        # Test if no new object was created
        db_objects = list(Article.objects.all())
        self.assertEqual(len(db_objects), 1)

        # Test if objects was actually updated
        updated_article = Article.objects.filter(foreign_id=article_foreign_id).first()
        self.assertEqual(updated_article.title, new_title)
        self.assertNotEqual(updated_article.title, initial_title)

    def test_article_invalid(self):
        data = self.test_data.ingest_articles[1]
        # Empty required project id list
        data["projectIds"] = []

        result = self.client.post(
            self.api_url,
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

        # Create articles from mock data
        [Article.objects.create(**x) for x in self.test_data.articles]

        result = self.client.get(
            self.api_url,
            headers=self.header,
            content_type="application/json",
        )

        self.assertEqual(result.status_code, 200)

        # Check if len result equals the amount of objects in the database
        db_objects = list(Article.objects.all())
        self.assertEqual(len(db_objects), 2)

        # Check for expected output
        first_article = self.test_data.articles[0]
        second_article = self.test_data.articles[1]

        expected_result = {
            str(first_article["foreign_id"]): {
                "modification_date": str(first_article["modification_date"]).replace(
                    "T", " "
                )
            },
            str(second_article["foreign_id"]): {
                "modification_date": str(second_article["modification_date"]).replace(
                    "T", " "
                )
            },
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
