""" unit_tests """

import json
import os
from datetime import datetime

from django.test import Client, TestCase

from construction_work.generic_functions.aes_cipher import AESCipher
from construction_work.generic_functions.date_translation import (
    translate_timezone as tt,
)
from construction_work.models import Article, Project, ProjectManager, WarningMessage
from construction_work.models.image import Image
from construction_work.models.warning_and_notification import WarningImage
from construction_work.unit_tests.mock_data import TestData
from construction_work.views.views_messages import Messages

message = Messages()


class TestArticlesBase(TestCase):
    """Test articles base"""

    def setUp(self) -> None:
        self.data = TestData()
        self.maxDiff = None

        # Create device header
        app_token = os.getenv("APP_TOKEN")
        aes_secret = os.getenv("AES_SECRET")
        token = AESCipher(app_token, aes_secret).encrypt()
        self.headers = {"HTTP_DEVICEAUTHORIZATION": token}

        # Create request client
        self.client = Client()

    def tearDown(self) -> None:
        Project.objects.all().delete()
        Article.objects.all().delete()
        WarningMessage.objects.all().delete()
        ProjectManager.objects.all().delete()


class TestArticles(TestArticlesBase):
    """Test multiple articles view"""

    def setUp(self):
        """Setup test db"""
        super().setUp()
        self.api_url = "/api/v1/articles"

        projects = []
        for project_data in self.data.projects:
            project = Project.objects.create(**project_data)
            projects.append(project)

        articles = []
        for article_data in self.data.articles:
            article = Article.objects.create(**article_data)
            articles.append(article)

        articles[0].projects.add(projects[0])
        articles[0].publication_date = "2023-01-01T12:00:00+00:00"
        articles[0].save()

        articles[1].projects.add(projects[1])
        articles[1].publication_date = "2023-01-01T11:00:00+00:00"
        articles[1].save()

        warning_data = self.data.warning_message
        # warning_data["publication_date"] = "2023-01-01T10:00:00+00:00"
        warning_data["project_id"] = projects[0].pk
        warning = WarningMessage.objects.create(**warning_data)
        warning.publication_date = "2023-01-01T10:00:00+00:00"
        warning.save()

    def test_get_all(self):
        """Test get all news"""
        result = self.client.get(self.api_url, **self.headers)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.data), 3)

    def test_get_limit_one(self):
        """Test limiting the result to one article"""
        result = self.client.get(self.api_url, {"limit": 1}, **self.headers)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.data), 1)

    def test_invalid_limit(self):
        """Test passing invalid limit char"""
        result = self.client.get(self.api_url, {"limit": "1.1"}, **self.headers)
        self.assertEqual(result.status_code, 400)

    def test_get_articles_of_single_project(self):
        """Test get news from a single project"""
        first_project = Project.objects.first()

        result = self.client.get(
            self.api_url, {"project_ids": first_project.pk}, **self.headers
        )
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.data), 2)

    def test_get_articles_of_multiple_projects(self):
        """Test get news from multiple projects"""
        first_project = Project.objects.first()
        last_project = Project.objects.last()

        result = self.client.get(
            self.api_url,
            {"project_ids": f"{first_project.pk},{last_project.pk}"},
            **self.headers,
        )
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.data), 3)

    def test_invalid_project_id(self):
        """Test passing invalid project id in comma seperated list"""
        result = self.client.get(
            self.api_url, {"project_ids": "1,foobar"}, **self.headers
        )
        self.assertEqual(result.status_code, 400)

    def test_article_content(self):
        """Test if content of article is as expected"""
        result = self.client.get(
            self.api_url,
            {"sort_by": "publication_date", "sort_order": "desc"},
            **self.headers,
        )
        self.assertEqual(result.status_code, 200)
        article = Article.objects.order_by("-publication_date").first()

        expected_data = {
            "title": article.title,
            "publication_date": article.publication_date,
            "meta_id": {
                "type": "article",
                "id": article.pk,
            },
            "images": [],
        }
        self.assertDictEqual(result.data[0], expected_data)

    def test_article_content_with_image(self):
        """Test if content of article with image is as expected"""
        image_data = {
            "id": 123,
            "sources": [
                {
                    "url": "/foo/bar.png",
                    "width": 100,
                    "height": 50,
                },
            ],
            "aspectRatio": 2,
            "alternativeText": None,
        }

        article_data = self.data.articles[0]
        article_data["foreign_id"] = 9999
        article_data["image"] = image_data
        article: Article = Article.objects.create(**article_data)
        # Refresh from db to create datetime objects from datetime strings
        article.refresh_from_db()

        project_data = self.data.projects[0]
        project_data["foreign_id"] = 9999
        project = Project.objects.create(**project_data)

        article.projects.add(project)

        result = self.client.get(
            self.api_url, {"project_ids": [project.pk]}, **self.headers
        )
        self.assertEqual(result.status_code, 200)

        expected_data = {
            # "type": "news",
            "title": article.title,
            "publication_date": article.publication_date,
            "meta_id": {
                "type": "article",
                "id": article.pk,
            },
            "images": [image_data],
        }
        self.assertDictEqual(result.data[0], expected_data)

    def test_warning_content(self):
        """Test if content of warning is as expected"""
        result = self.client.get(
            self.api_url,
            {"sort_by": "publication_date", "sort_order": "asc"},
            **self.headers,
        )
        self.assertEqual(result.status_code, 200)
        warning = WarningMessage.objects.first()

        expected_data = {
            # "type": "warning",
            "title": warning.title,
            "publication_date": warning.publication_date,
            "meta_id": {
                "type": "warning",
                "id": warning.pk,
            },
            "images": [],
        }
        self.assertDictEqual(result.data[0], expected_data)

    def test_warning_content_with_image(self):
        """Test if content of warning with image is as expected"""
        project_data = self.data.projects[0]
        project_data["foreign_id"] = 9999
        project = Project.objects.create(**project_data)

        warning_data = self.data.warning_message
        warning_data["project_id"] = project.pk
        warning = WarningMessage.objects.create(**warning_data)
        warning.refresh_from_db()

        warning_image_data = {
            "warning_id": warning.pk,
            "is_main": True,
        }
        warning_image = WarningImage.objects.create(**warning_image_data)

        image_data = self.data.images[0]
        image = Image.objects.create(**image_data)
        warning_image.images.add(image)

        result = self.client.get(
            self.api_url, {"project_ids": project.pk}, **self.headers
        )
        self.assertEqual(result.status_code, 200)

        expected_data = {
            # "type": "warning",
            "title": warning.title,
            "publication_date": warning.publication_date,
            "meta_id": {
                "type": "warning",
                "id": warning.pk,
            },
            "images": [
                {
                    "id": warning_image.pk,
                    "sources": [
                        {
                            "uri": f"http://testserver/api/v1/image?id={image.pk}",
                            "width": image.width,
                            "height": image.height,
                        }
                    ],
                }
            ],
        }
        self.assertDictEqual(result.data[0], expected_data)

    def test_sort_news_by_publication_date_descending(self):
        """Test getting news sorted by publication date descending"""
        articles = Article.objects.all()
        warnings = WarningMessage.objects.all()
        news = []
        news.extend(articles)
        news.extend(warnings)
        news_pub_dates = [x.publication_date for x in news]
        sorted_pub_dates = sorted(news_pub_dates, reverse=True)

        result = self.client.get(
            self.api_url,
            {"sort_by": "publication_date", "sort_order": "desc"},
            **self.headers,
        )
        self.assertEqual(result.status_code, 200)
        result_pub_dates = [x["publication_date"] for x in result.data]

        self.assertEqual(result_pub_dates, sorted_pub_dates)

    def test_invalid_sort_key(self):
        """Test sorting news with invalid sort key"""
        result = self.client.get(self.api_url, {"sort_by": "foobar"}, **self.headers)
        self.assertEqual(result.status_code, 400)

    def test_invalid_sort_key_but_no_news(self):
        """Test sorting news with invalid sort key"""
        result = self.client.get(
            self.api_url, {"project_ids": "9999", "sort_by": "foobar"}, **self.headers
        )
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.data), 0)


class TestNews(TestArticlesBase):
    """Test single article view"""

    def setUp(self):
        """Setup test db"""
        super().setUp()
        self.api_url = "/api/v1/project/news"

        app_token = os.getenv("APP_TOKEN")
        aes_secret = os.getenv("AES_SECRET")
        token = AESCipher(app_token, aes_secret).encrypt()
        self.headers = {"DeviceAuthorization": token}

        projects = []
        for project_data in self.data.projects:
            project = Project.objects.create(**project_data)
            projects.append(project)

        articles = []
        for article_data in self.data.articles:
            article = Article.objects.create(**article_data)
            articles.append(article)

        articles[0].projects.add(projects[0])
        articles[0].publication_date = "2023-01-01T12:00:00+00:00"
        articles[0].save()

        articles[1].projects.add(projects[1])
        articles[1].publication_date = "2023-01-01T11:00:00+00:00"
        articles[1].save()

    def test_get_single_article(self):
        """Test retrieving single article"""
        article = Article.objects.first()
        result = self.client.get(self.api_url, {"id": article.pk}, headers=self.headers)
        self.assertEqual(result.status_code, 200)

        target_tzinfo = datetime.fromisoformat(result.data["last_seen"]).tzinfo

        expected_data = {
            "id": article.pk,
            "meta_id": {
                "id": article.pk,
                "type": "article",
            },
            "foreign_id": article.foreign_id,
            "active": article.active,
            "last_seen": tt(str(article.last_seen), target_tzinfo),
            "title": article.title,
            "intro": article.intro,
            "body": article.body,
            "image": article.image,
            "url": article.url,
            "creation_date": tt(str(article.creation_date), target_tzinfo),
            "modification_date": tt(str(article.modification_date), target_tzinfo),
            "publication_date": tt(str(article.publication_date), target_tzinfo),
            "expiration_date": tt(str(article.expiration_date), target_tzinfo),
            "projects": [x.pk for x in article.projects.all()],
        }
        result_dict = json.loads(result.content)
        self.assertDictEqual(result_dict, expected_data)

    def test_missing_article_id(self):
        """Test calling API without article id param"""
        result = self.client.get(
            self.api_url, {"foobar": "foobar"}, headers=self.headers
        )
        self.assertEqual(result.status_code, 400)

    def test_article_not_found(self):
        """Test requesting article id which does not exist"""
        result = self.client.get(self.api_url, {"id": 9999}, headers=self.headers)
        self.assertEqual(result.status_code, 404)
