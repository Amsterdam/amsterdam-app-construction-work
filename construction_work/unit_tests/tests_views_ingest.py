""" unit_tests """

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


class TestApiImage(TestCase):
    """test image api"""

    def setUp(self):
        """setup test db"""
        self.test_data = TestData()
        for asset in self.test_data.assets:
            Asset.objects.create(**asset)

        for image in self.test_data.images:
            Image.objects.create(**image)

        token = AESCipher(
            "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", os.getenv("AES_SECRET")
        ).encrypt()
        self.header = {"INGESTAUTHORIZATION": token}
        self.content_type = "application/json"
        self.client = Client()

    def tearDown(self):
        Project.objects.all().delete()
        Asset.objects.all().delete()
        Image.objects.all().delete()

        return super().tearDown()

    def test_image_exist(self):
        """test image exist"""
        c = Client()
        response = c.get(
            "/api/v1/ingest/image?identifier=0000000000", headers=self.header
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data, {"status": True, "result": {"identifier": "0000000000"}}
        )

    def test_image_not_exist(self):
        """test image does not exist"""
        c = Client()
        response = c.get("/api/v1/ingest/image?identifier=bogus", headers=self.header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"status": False, "result": None})

    def test_image_ingest_valid(self):
        """test ingesting valid image"""
        data = {
            "identifier": "0000000000",
            "size": "orig",
            "url": "mock",
            "filename": "mock",
            "description": "mock",
            "mime_type": "mock",
            "data": "MHgwMA==",
        }

        result = self.client.post(
            "/api/v1/ingest/image",
            data=data,
            headers=self.header,
            content_type="application/json",
        )

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, {"status": True, "result": True})

    def test_image_ingest_invalid(self):
        """test ingesting invalid image"""
        data = {
            "identifier": "0000000000",
            "size": "orig",
            "url": "mock",
            "filename": "mock",
            "description": "mock",
            "mime_type": "mock",
            "data": "BOGUS",
        }

        result = self.client.post(
            "/api/v1/ingest/image",
            data=data,
            headers=self.header,
            content_type="application/json",
        )

        self.assertEqual(result.status_code, 500)
        self.assertEqual(
            result.data,
            {
                "status": False,
                "result": "Invalid base64-encoded string: number of data characters (5) "
                "cannot be 1 more than a multiple of 4",
            },
        )

    def test_asset_exist(self):
        """test existing asset"""
        c = Client()
        response = c.get(
            "/api/v1/ingest/asset?identifier=0000000000", headers=self.header
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data, {"status": True, "result": {"identifier": "0000000000"}}
        )

    def test_asset_not_exist(self):
        """test not existing asset"""
        c = Client()
        response = c.get("/api/v1/ingest/asset?identifier=bogus", headers=self.header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"status": False, "result": None})

    def test_asset_ingest_valid(self):
        """test ingesting valid asset"""
        data = {
            "identifier": "0000000000",
            "url": "mock",
            "mime_type": "mock",
            "data": "MHgwMA==",
        }

        result = self.client.post(
            "/api/v1/ingest/asset",
            data=data,
            headers=self.header,
            content_type="application/json",
        )

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, {"status": True, "result": True})

    def test_asset_ingest_invalid(self):
        """test ingesting invalid asset"""
        data = {
            "identifier": "0000000000",
            "url": "mock",
            "mime_type": "mock",
            "data": "BOGUS",
        }

        result = self.client.post(
            "/api/v1/ingest/asset",
            data=data,
            headers=self.header,
            content_type="application/json",
        )

        self.assertEqual(result.status_code, 500)
        self.assertEqual(
            result.data,
            {
                "status": False,
                "result": "Invalid base64-encoded string: number of data characters (5) "
                "cannot be 1 more than a multiple of 4",
            },
        )

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

    def test_projects_get(self):
        """test get project data"""
        project_object = Project(**self.test_data.projects[0])
        project_object.save()

        result = self.client.get(
            "/api/v1/ingest/projects?identifier=0000000000",
            headers=self.header,
            content_type="application/json",
        )
        self.assertEqual(result.status_code, 200)
        assert isinstance(result.data["result"], dict)

        result = self.client.get(
            "/api/v1/ingest/projects?identifier=0000000001",
            headers=self.header,
            content_type="application/json",
        )
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, {"status": True, "result": None})

    def test_projects_post_valid(self):
        """test posting valid project data"""
        result = self.client.post(
            "/api/v1/ingest/projects",
            data=self.test_data.projects[0],
            headers=self.header,
            content_type="application/json",
        )
        project_objects = list(Project.objects.all())

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, {"status": True, "result": True})
        self.assertEqual(len(project_objects), 1)

        # Update record
        result = self.client.post(
            "/api/v1/ingest/projects",
            data=self.test_data.projects[0],
            headers=self.header,
            content_type="application/json",
        )
        project_objects = list(Project.objects.all())

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, {"status": True, "result": True})
        self.assertEqual(len(project_objects), 1)

    def test_projects_post_invalid(self):
        """test posting invalid project data"""
        data = {"bogus": "bogus"}

        result = self.client.post(
            "/api/v1/ingest/projects",
            data=data,
            headers=self.header,
            content_type="application/json",
        )
        project_objects = list(Project.objects.all())

        self.assertEqual(result.status_code, 500)
        self.assertEqual(len(project_objects), 0)

    def test_projects_delete_valid(self):
        """test deleting valid project"""
        project_object = Project(**self.test_data.projects[0])
        project_object.save()

        data = {"identifier": "0000000000"}
        result = self.client.delete(
            "/api/v1/ingest/projects",
            data=data,
            headers=self.header,
            content_type="application/json",
        )
        project_objects = list(Project.objects.all())

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, {"status": True, "result": True})
        self.assertEqual(len(project_objects), 0)

        data = "bogus"
        result = self.client.delete(
            "/api/v1/ingest/projects",
            data=data,
            headers=self.header,
            content_type="application/json",
        )

        self.assertEqual(result.status_code, 500)
        self.assertEqual(
            result.data,
            {
                "status": False,
                "result": "JSON parse error - Expecting value: line 1 column 1 (char 0)",
            },
        )

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
