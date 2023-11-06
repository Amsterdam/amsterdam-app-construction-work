""" unit_tests """

import json
import os

from django.test import Client, TestCase

from construction_work.generic_functions.aes_cipher import AESCipher
from construction_work.models import Article, Project, ProjectManager, WarningMessage
from construction_work.unit_tests.mock_data import TestData
from construction_work.views.views_messages import Messages

message = Messages()


class TestArticlesBase(TestCase):
    def setUp(self) -> None:
        self.data = TestData()
        self.identifiers = []

        for project in self.data.projects:
            Project.objects.create(**project)

        for news in self.data.articles:
            news["project_id"] = Project.objects.filter(pk=news["project_id"]).first()
            news_item = Article.objects.create(**news)
            news_item.save()
            self.identifiers.append(news_item.foreign_id)

        for project_manager in self.data.project_managers:
            ProjectManager.objects.create(**project_manager)

        self.url = "/api/v1/project/warning"
        self.client = Client()
        self.token = AESCipher(
            "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", os.getenv("AES_SECRET")
        ).encrypt()
        self.headers = {"UserAuthorization": self.token}
        self.content_type = "application/json"
        for title in ["title0", "title1"]:
            data = {
                "title": title,
                "project_identifier": "0000000000",
                "project_manager_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                "body": "Body text",
            }
        self.client.post(
            self.url,
            json.dumps(data),
            headers=self.headers,
            content_type=self.content_type,
        )

    def tearDown(self) -> None:
        Project.objects.all().delete()
        WarningMessage.objects.all().delete()
        ProjectManager.objects.all().delete()


class TestArticles(TestArticlesBase):
    """unit_tests"""

    def setUp(self):
        """Setup test db"""
        self.api_url = "/api/v1/articles"

    def test_get_all(self):
        """Test get all articles"""
        result = self.client.get(self.api_url)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.data["result"]), 3)

    def test_get_limit_one(self):
        """Test limiting the result to one article"""
        result = self.client.get(self.api_url, {"limit": 1})
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.data["result"]), 1)

    def test_get_limit_project_ids(self):
        """Test limiting amount of projects"""
        result = self.client.get(
            self.api_url,
            {"project-ids": "0000000000,0000000001", "sort-order": "asc", "limit": 4},
        )

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.data["result"]), 3)

    def test_get_limit_error(self):
        """Test false limit query"""
        result = self.client.get(
            self.api_url,
            {
                "project-ids": "0000000000,0000000001",
                "sort-order": "asc",
                "limit": "error",
            },
        )

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.data["result"]), 3)


class TestNews(TestArticlesBase):
    """UNITTEST"""

    def setUp(self):
        """Setup test db"""
        self.api_url = "/api/v1/project/news"

    def test_get_news(self):
        """Test get news"""
        c = Client()
        for i in range(0, len(self.setup.identifiers)):
            response = c.get(
                "/api/v1/project/news?id={identifier}".format(
                    identifier=self.setup.identifiers[i]
                )
            )
            result = json.loads(response.content)
            self.data.articles[i]["last_seen"] = result["result"]["last_seen"]
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(
                result, {"status": True, "result": self.data.articles[i]}
            )

    def test_invalid_query(self):
        """Test invalid news query"""
        c = Client()
        response = c.get("/api/v1/project/news")
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(result, {"status": False, "result": message.invalid_query})

    def test_no_record(self):
        """Test for 404 result"""
        c = Client()
        response = c.get("/api/v1/project/news?id=unknown")
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertDictEqual(
            result, {"status": False, "result": message.no_record_found}
        )

    def test_method_not_allowed(self):
        """Test invalid http method"""
        c = Client()
        response = c.post("/api/v1/project/news")
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertDictEqual(result, {"detail": 'Method "POST" not allowed.'})
