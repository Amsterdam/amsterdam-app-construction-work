""" Test ingest views """

import os
from unittest.mock import patch

from django.test import Client, TestCase
from rest_framework import status

from construction_work.api_messages import Messages
from construction_work.garbage_collector.garbage_collector import GarbageCollector
from construction_work.generic_functions.aes_cipher import AESCipher
from construction_work.models import Article, Asset, Image, Project
from construction_work.unit_tests.mock_data import TestData
from construction_work.generic_functions.generic_logger import Logger

messages = Messages()
logger = Logger()


class BaseTestIngestViews(TestCase):
    def setUp(self):
        """Setup for all ingest view tests"""
        token = AESCipher(
            "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", os.getenv("AES_SECRET")
        ).encrypt()
        self.header = {"INGESTAUTHORIZATION": token}
        self.content_type = "application/json"
        self.client = Client()


class TestProjectIngestViews(BaseTestIngestViews):
    """Test project ingest views"""

    def setUp(self):
        """Setup test data"""
        self.test_data = TestData()
        super().setUp()

    def test_add_new_project_success(self):
        """Test add new project via ingest API"""
        first_project = self.test_data.projects[0]

        result = self.client.post(
            "/api/v1/ingest/project",
            data=first_project,
            headers=self.header,
            content_type="application/json",
        )
        # Test for correct status code
        logger.debug(result.data)
        self.assertEqual(result.status_code, 200)

        # Test if a new object was created
        db_objects = list(Project.objects.all())
        self.assertEqual(len(db_objects), 1)

    def test_update_project_success(self):
        """Test update existing project via ingest API"""
        first_project = self.test_data.projects[0]
        Project.objects.create(**first_project)

        new_date = "2023-10-01"
        data = {
            "project_id": "0000000000",
            "modification_date": new_date,
            "content_html": "<html />",
        }

        result = self.client.post(
            "/api/v1/ingest/project",
            data=data,
            headers=self.header,
            content_type="application/json",
        )
        # Test for correct status code
        logger.debug(result.data)
        self.assertEqual(result.status_code, 200)

        # Test if no new object was created
        db_objects = list(Project.objects.all())
        self.assertEqual(len(db_objects), 1)

        # Test if objects was actually updated
        updated_project = db_objects[0]
        self.assertEqual(str(updated_project.modification_date), new_date)

    def test_project_invalid(self):
        """test invalid project"""
        data = {"bogus": "bogus"}

        result = self.client.post(
            "/api/v1/ingest/project",
            data=data,
            headers=self.header,
            content_type="application/json",
        )
        db_objects = list(Project.objects.all())

        self.assertEqual(result.status_code, 400)
        self.assertEqual(len(db_objects), 0)


class TestNewsIngestViews(BaseTestIngestViews):
    """Test news ingest views"""

    def setUp(self):
        """Setup test data"""
        self.test_data = TestData()
        super().setUp()

    def test_news_valid(self):
        """test ingesting valid news"""
        Project.objects.all().delete()
        for project in self.test_data.projects:
            Project.objects.create(**project)

        result = self.client.post(
            "/api/v1/ingest/article",
            data=self.test_data.article[0],
            headers=self.header,
            content_type="application/json",
        )
        news_objects = list(Article.objects.all())

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, {"status": True, "result": "work item saved"})
        self.assertEqual(len(news_objects), 1)

        # Update existing record
        result = self.client.post(
            "/api/v1/ingest/article",
            data=self.test_data.article[0],
            headers=self.header,
            content_type="application/json",
        )
        news_objects = list(Article.objects.all())

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, {"status": True, "result": "work item updated"})
        self.assertEqual(len(news_objects), 1)

    def test_news_invalid(self):
        """test ingesting invalid news"""
        data = "bogus"

        result = self.client.post(
            "/api/v1/ingest/article",
            data=data,
            headers=self.header,
            content_type="application/json",
        )
        news_objects = list(Article.objects.all())

        self.assertEqual(result.status_code, 500)
        self.assertEqual(
            result.data,
            {
                "status": False,
                "result": "JSON parse error - Expecting value: line 1 column 1 (char 0)",
            },
        )
        self.assertEqual(len(news_objects), 0)


class TestGarbageCollectionView(BaseTestIngestViews):
    def test_garbage_collection(self):
        """test garbage collector"""

        def mock(*args, **kwargs):
            """dummy func"""
            pass  # pylint: disable=unnecessary-pass

        with patch.object(GarbageCollector, "collect_iprox", side_effect=mock):
            result = self.client.get(
                "/api/v1/ingest/garbagecollector?project_type=kade",
                headers=self.header,
                content_type="application/json",
            )

            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.data, {"status": True, "result": None})
