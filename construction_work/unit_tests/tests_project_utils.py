from datetime import datetime, timedelta

from django.test import TestCase
from django.utils import timezone

from construction_work.generic_functions.model_utils import create_id_dict
from construction_work.generic_functions.project_utils import (
    create_project_news_lookup,
    get_recent_articles_of_project,
)
from construction_work.models.article import Article
from construction_work.models.project import Project
from construction_work.models.warning_and_notification import WarningMessage
from construction_work.serializers import (
    ArticleMinimalSerializer,
    WarningMessageMinimalSerializer,
)
from construction_work.unit_tests.mock_data import TestData


class TestProjectUtilsBase(TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.data = TestData()
        self.project = Project.objects.create(**self.data.projects[0])

    def tearDown(self) -> None:
        Project.objects.all().delete()
        Article.objects.all().delete()
        WarningMessage.objects.all().delete()

    def create_article(self, foreign_id, pub_date, project=None):
        if project is None:
            project = self.project

        article_data = self.data.articles[0]

        article_data["foreign_id"] = foreign_id
        article_data["publication_date"] = pub_date
        article = Article.objects.create(**article_data)
        article.projects.add(project)
        article.refresh_from_db()
        return article

    def create_warning(self, pub_date, project=None):
        if project is None:
            project = self.project

        warning_data = self.data.warning_message

        warning_data["project"] = project
        warning_data["publication_date"] = pub_date
        warning = WarningMessage.objects.create(**warning_data)
        warning.refresh_from_db()
        return warning


class TestGetRecentArticlesOfProject(TestProjectUtilsBase):
    def test_article_age_being_applied(self):
        # Set up articles with varying publication dates
        article1 = self.create_article(10, timezone.now() - timedelta(days=10))
        article2 = self.create_article(20, timezone.now() - timedelta(days=5))
        article3 = self.create_article(30, timezone.now() - timedelta(days=1))

        article_serializer_class = ArticleMinimalSerializer
        warning_serializer_class = WarningMessageMinimalSerializer
        # Call the function with max age of 7 days
        recent_articles = get_recent_articles_of_project(
            project=self.project,
            article_max_age=7,
            article_serializer_class=article_serializer_class,
            warning_serializer_class=warning_serializer_class,
        )

        # Check that only article2 and article3 are included (within the 7-day range)
        self.assertEqual(len(recent_articles), 2)

        # Check if output was serialized and present in list
        article1_serializer = article_serializer_class(article1)
        article1_data = article1_serializer.data

        article2_serializer = article_serializer_class(article2)
        article2_data = article2_serializer.data

        article3_serializer = article_serializer_class(article3)
        article3_data = article3_serializer.data

        self.assertNotIn(article1_data, recent_articles)
        self.assertIn(article2_data, recent_articles)
        self.assertIn(article3_data, recent_articles)

    def test_get_mix_of_articles_and_warnings(self):
        article1 = self.create_article(10, timezone.now() - timedelta(days=6))
        article2 = self.create_article(20, timezone.now() - timedelta(days=5))
        warning1 = self.create_warning(timezone.now() - timedelta(days=3))
        warning2 = self.create_warning(timezone.now() - timedelta(days=1))

        # Call the function with max age of 7 days
        recent_articles = get_recent_articles_of_project(
            project=self.project,
            article_max_age=7,
            article_serializer_class=ArticleMinimalSerializer,
            warning_serializer_class=WarningMessageMinimalSerializer,
        )

        self.assertEqual(len(recent_articles), 4)

        recent_articles_ids = [item["meta_id"]["id"] for item in recent_articles]
        self.assertIn(article1.pk, recent_articles_ids)
        self.assertIn(article2.pk, recent_articles_ids)
        self.assertIn(warning1.pk, recent_articles_ids)
        self.assertIn(warning2.pk, recent_articles_ids)


class TestCreateProjectNewsLookup(TestProjectUtilsBase):
    def test_article_age_being_applied(self):
        # Set up articles and warning messages with varying publication dates
        article1 = self.create_article(
            foreign_id=1, pub_date=timezone.now() - timedelta(days=10)
        )
        article2 = self.create_article(
            foreign_id=2, pub_date=timezone.now() - timedelta(days=5)
        )
        warning1 = self.create_warning(pub_date=timezone.now() - timedelta(days=2))
        warning2 = self.create_warning(pub_date=timezone.now() - timedelta(days=1))

        # Call the function with max age of 7 days
        project_news_mapping = create_project_news_lookup(
            projects=[self.project], article_max_age=7
        )

        # Check that the mapping only contains articles and warnings within the 7-day range for the project
        project_id = self.project.pk
        project_articles = [
            news["meta_id"]["id"]
            for news in project_news_mapping[project_id]
            if news["meta_id"]["type"] == "article"
        ]
        project_warnings = [
            news["meta_id"]["id"]
            for news in project_news_mapping[project_id]
            if news["meta_id"]["type"] == "warning"
        ]

        self.assertNotIn(article1.pk, project_articles)
        self.assertIn(article2.pk, project_articles)
        self.assertIn(warning1.pk, project_warnings)
        self.assertIn(warning2.pk, project_warnings)

    def test_lookup_map_created_correctly(self):
        project2 = Project.objects.create(**self.data.projects[1])

        article1 = self.create_article(
            10, timezone.now() - timedelta(days=15), self.project
        )
        article2 = self.create_article(
            20, timezone.now() - timedelta(days=10), project2
        )
        warning1 = self.create_warning(timezone.now() - timedelta(days=5), project2)

        project_news_mapping = create_project_news_lookup(
            projects=[self.project, project2], article_max_age=30
        )

        expected_project_map = {
            self.project.pk: [
                {
                    "meta_id": create_id_dict(Article, article1.pk),
                }
            ],
            project2.pk: [
                {
                    "meta_id": create_id_dict(Article, article2.pk),
                },
                {
                    "meta_id": create_id_dict(WarningMessage, warning1.pk),
                },
            ],
        }

        # Testing without modification date to annoying to parse and compare correctly
        for _, v in project_news_mapping.items():
            for d in v:
                d.pop("modification_date")

        self.assertDictEqual(project_news_mapping, expected_project_map)
