""" unit_tests """
from datetime import datetime
import uuid
from django.core.exceptions import ValidationError

from django.test import TestCase

from construction_work.models import (
    Article,
    Asset,
    Image,
    Project,
    ProjectManager,
    WarningMessage,
)
from construction_work.models.article import Article
from construction_work.models.asset_and_image import Asset, Image
from construction_work.models.project import Project
from construction_work.models.project_manager import ProjectManager
from construction_work.models.warning_and_notification import WarningMessage

from construction_work.serializers import (
    ArticleSerializer,
    AssetsSerializer,
    ImageSerializer,
    Notification,
    ProjectCreateSerializer,
    ProjectManagerSerializer,
    WarningMessagePublicSerializer,
    WarningMessageSerializer,
)
from construction_work.unit_tests.mock_data import TestData
from construction_work.generic_functions.generic_logger import Logger


logger = Logger()

# TODO: unit tests for Device model
# what is the function of these tests? just test the Django ORM? added value?

# NOTE: properly test CRUD of models with serializers

class TestAssetsModel(TestCase):
    """unit_tests"""

    def setUp(self):
        """UNITTEST DB setup"""
        self.data = TestData()

        Asset.objects.all().delete()
        for asset in self.data.assets:
            Asset.objects.create(**asset)

    def test_asset_delete(self):
        """test delete"""
        Asset.objects.get(pk="0000000000").delete()
        asset_objects = Asset.objects.all()
        serializer = AssetsSerializer(asset_objects, many=True)

        self.assertEqual(len(serializer.data), 1)

    def test_asset_get_all(self):
        """test retrieve"""
        asset_objects = Asset.objects.all()
        self.assertEqual(len(asset_objects), 2)

    def test_asset_exists(self):
        """test exist"""
        asset = Asset.objects.get(pk="0000000000")

        self.assertEqual(asset.identifier, "0000000000")
        self.assertEqual(asset.url, "https://localhost/test0.pdf")
        self.assertEqual(asset.mime_type, "application/pdf")
        self.assertEqual(asset.data, b"")

    def test_asset_does_not_exist(self):
        """test not exist"""
        asset = Asset.objects.filter(pk="not-there").first()

        self.assertEqual(asset, None)


class TestImageModel(TestCase):
    """unit_tests"""

    def setUp(self):
        """unit_tests setup"""
        self.data = TestData()

        Image.objects.all().delete()
        for image in self.data.images:
            Image.objects.create(**image)

    def test_image_delete(self):
        """test delete"""
        Image.objects.all().first().delete()
        image_objects = Image.objects.all()
        serializer = ImageSerializer(image_objects, many=True)

        self.assertEqual(len(serializer.data), 2)

    def test_image_get_all(self):
        """test retrieve"""
        image_objects = Image.objects.all()

        self.assertEqual(len(image_objects), 3)

    def test_image_exists(self):
        """test exist"""
        image_object = Image.objects.all().first()

        self.assertEqual(image_object.data, b"")
        self.assertEqual(image_object.description, "square image")
        self.assertEqual(image_object.width, 10)
        self.assertEqual(image_object.height, 10)
        self.assertEqual(image_object.aspect_ratio, 1)
        self.assertEqual(image_object.coordinates, {"lat": 0.0, "lon": 0.0})
        self.assertEqual(image_object.mime_type, "image/jpg")

    def test_image_does_not_exist(self):
        """test not exist"""
        image = Image.objects.filter(pk=999).first()

        self.assertEqual(image, None)


class TestProjectModel(TestCase):
    """unit_tests"""

    def setUp(self):
        """unit_tests db setup"""
        self.data = TestData()
        self.maxDiff = None

        Project.objects.all().delete()
        for project in self.data.projects:
            Project.objects.create(**project)

    def test_projects_delete(self):
        """test delete"""
        Project.objects.all().first().delete()
        project_objects = list(Project.objects.all())
        serializer = ProjectCreateSerializer(project_objects, many=True)

        self.assertEqual(len(serializer.data), 1)

    def test_projects_get_all(self):
        """test retrieve"""
        project_objects = Project.objects.all()
        # Using create serializer in order to not return any extra data
        serializer = ProjectCreateSerializer(
            instance=project_objects, data=[], many=True, partial=True
        )
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)
        self.assertEqual(len(serializer.data), 2)

    def test_project_does_exist(self):
        """test exist"""
        projects_object = Project.objects.filter(project_id=2048).first()
        # Using create serializer in order to not return any extra data
        serializer = ProjectCreateSerializer(
            instance=projects_object, data={}, partial=True
        )
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)

        first_project = self.data.projects[0]
        first_project["id"] = serializer.data["id"]
        first_project["last_seen"] = serializer.data["last_seen"]
        
        def translate_timezone(date_str, target_tz_date_str) -> str:
            target_tz = datetime.fromisoformat(target_tz_date_str)
            tmp_date = datetime.fromisoformat(date_str)
            tmp_date = tmp_date.astimezone(target_tz.tzinfo)
            return tmp_date.isoformat()

        first_project["creation_date"] = translate_timezone(first_project["creation_date"], serializer.data["creation_date"])
        first_project["modification_date"] = translate_timezone(first_project["modification_date"], serializer.data["modification_date"])
        first_project["publication_date"] = translate_timezone(first_project["publication_date"], serializer.data["publication_date"])
        first_project["expiration_date"] = translate_timezone(first_project["expiration_date"], serializer.data["expiration_date"])

        self.assertDictEqual(serializer.data, first_project)

    def test_projects_does_not_exist(self):
        """test not exist"""
        projects_objects = Project.objects.filter(project_id=9999).first()

        self.assertEqual(projects_objects, None)


class TestArticleModel(TestCase):
    """unit_tests"""

    def setUp(self):
        self.data = TestData()
        
        for project in self.data.projects:
            Project.objects.create(**project)

        for article in self.data.article:
            Article.objects.create(**article)

        all_articles = list(Article.objects.all())
        all_projects = list(Project.objects.all())
        all_articles[0].projects.set(all_projects[:1])
        all_articles[1].projects.set(all_projects)
        all_articles

    def tearDown(self) -> None:
        Project.objects.all().delete()
        Article.objects.all().delete()

        return super().tearDown()

    def test_article_delete(self):
        """test delete"""
        Article.objects.first().delete()
        news_objects = Article.objects.all()
        serializer = ArticleSerializer(news_objects, many=True)

        self.assertEqual(len(serializer.data), 1)

    def test_article_get_all(self):
        """test retrieve"""
        news_objects = Article.objects.all()
        serializer = ArticleSerializer(news_objects, many=True)

        self.assertEqual(len(serializer.data), 2)

    def test_article_exists(self):
        """test exist"""
        news_object = Article.objects.get(article_id=128)
        serializer = ArticleSerializer(news_object)
        self.data.article[0]["last_seen"] = serializer.data["last_seen"]

        self.assertEqual(self.data.article[0]["active"], True)

    def test_article_does_not_exist(self):
        """test not exist"""
        news_object = Article.objects.filter(article_id=9999).first()

        self.assertEqual(news_object, None)


class TestProjectManagerModel(TestCase):
    """unit_tests"""

    def setUp(self):
        """unit_tests db setup"""
        self.data = TestData()

        for project in self.data.projects:
            Project.objects.create(**project)

        for pm in self.data.project_manager:
            ProjectManager.objects.create(**pm)

        all_project_managers = list(ProjectManager.objects.all())
        all_projects = list(Project.objects.all())
        all_project_managers[0].projects.set(all_projects[:1])
        all_project_managers[1].projects.set(all_projects)

    def tearDown(self) -> None:
        ProjectManager.objects.all().delete()

        return super().tearDown()

    def test_pm_delete(self):
        """test delete"""
        ProjectManager.objects.first().delete()
        pm_objects = ProjectManager.objects.all()
        serializer = ProjectManagerSerializer(pm_objects, many=True)

        self.assertEqual(len(serializer.data), 1)

    def test_pm_get_all(self):
        """test retrieve"""
        pm_objects = ProjectManager.objects.all()

        self.assertEqual(len(pm_objects), 2)

    def test_pm_exists(self):
        """test exist"""
        pm_objects = ProjectManager.objects.get(
            manager_key=uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
        )

        self.assertEqual(
            pm_objects.manager_key, uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
        )
        self.assertEqual(pm_objects.email, "mock0@amsterdam.nl")

    def test_pm_does_not_exist(self):
        """test not exist"""
        pm_object = ProjectManager.objects.filter(
            manager_key=uuid.UUID("00000000-0000-0000-0000-000000000000")
        ).first()

        self.assertEqual(pm_object, None)

    def test_pm_has_invalid_email(self):
        """test email"""
        data = {
            "manager_key": "cccccccc-cccc-cccc-cccc-cccccccccccc",
            "email": "mock@invalid",
        }

        with self.assertRaises(ValidationError) as context:
            pm = ProjectManager.objects.create(**data)
            pm.full_clean()
    
    def test_pm_not_amsterdam_email(self):
        """test email"""
        data = {
            "manager_key": "cccccccc-cccc-cccc-cccc-cccccccccccc",
            "email": "mock@mail.com",
        }

        with self.assertRaises(ValidationError) as context:
            pm = ProjectManager.objects.create(**data)
            pm.full_clean()


class TestWarningMessagesModel(TestCase):
    """unit_tests"""

    def setUp(self):
        """Setup test db"""
        self.data = TestData()
        for project in self.data.projects:
            Project.objects.create(**project)

        for project_manager in self.data.project_manager:
            ProjectManager.objects.create(**project_manager)

    def tearDown(self) -> None:
        Project.objects.all().delete()
        WarningMessage.objects.all().delete()
        ProjectManager.objects.all().delete()
        return super().tearDown()

    def test_create_message(self):
        """Test create warning message"""
        message_data = self.data.warning_message
        message_data["project_id"] = Project.objects.first().pk
        message_data["project_manager_id"] = ProjectManager.objects.first().pk

        warning_message = WarningMessage.objects.create(**message_data)

        self.assertEqual(
            warning_message.author_email, self.data.project_manager[0]["email"]
        )
        self.assertNotEqual(warning_message.publication_date, None)
        self.assertNotEqual(warning_message.modification_date, None)

    # def test_default_email(self):
    #     """Test default email on creation"""
    #     data = dict(self.data.warning_message)
    #     data["project_manager_id"] = uuid.uuid4()
    #     data["project_identifier"] = Project.objects.filter(
    #         pk=data["project_identifier"]
    #     ).first()
    #     warning_message = WarningMessage.objects.create(**data)

    #     self.assertEqual(warning_message.author_email, "redactieprojecten@amsterdam.nl")

    # def test_modification_date(self):
    #     """test modification date on changing a message"""
    #     self.data.warning_message["project_identifier"] = Project.objects.filter(
    #         pk=self.data.warning_message["project_identifier"]
    #     ).first()
    #     warning_message = WarningMessage.objects.create(**self.data.warning_message)
    #     date = warning_message.modification_date
    #     warning_message.save()

    #     self.assertNotEqual(warning_message.modification_date, date)

    # def test_serializer_internal(self):
    #     """Purpose: test if project_manager_id is present in serializer"""
    #     self.data.warning_message["project_identifier"] = Project.objects.filter(
    #         pk=self.data.warning_message["project_identifier"]
    #     ).first()
    #     warning_message = WarningMessage.objects.create(**self.data.warning_message)
    #     serializer = WarningMessageSerializer(warning_message, many=False)
    #     data = dict(serializer.data)
    #     expected_result = {
    #         "identifier": data["identifier"],
    #         "title": "title",
    #         "body": "Body text",
    #         "project_identifier": "0000000000",
    #         "project_manager_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
    #         "images": [],
    #         "publication_date": data["publication_date"],
    #         "modification_date": data["modification_date"],
    #         "author_email": "mock0@amsterdam.nl",
    #     }

    #     self.assertDictEqual(data, expected_result)

    # def test_serializer_external(self):
    #     """Purpose: test if project_manager_id is NOT present in serializer"""
    #     self.data.warning_message["project_identifier"] = Project.objects.filter(
    #         pk=self.data.warning_message["project_identifier"]
    #     ).first()
    #     warning_message = WarningMessage.objects.create(**self.data.warning_message)
    #     serializer = WarningMessagePublicSerializer(warning_message, many=False)
    #     data = dict(serializer.data)
    #     expected_result = {
    #         "identifier": data["identifier"],
    #         "title": "title",
    #         "body": "Body text",
    #         "project_identifier": "0000000000",
    #         "images": [],
    #         "publication_date": data["publication_date"],
    #         "modification_date": data["modification_date"],
    #         "author_email": "mock0@amsterdam.nl",
    #     }

    #     self.assertDictEqual(data, expected_result)


class TestNotificationModel(TestCase):
    """unit_tests"""

    def __init__(self, *args, **kwargs):
        super(TestNotificationModel, self).__init__(*args, **kwargs)
        self.data = TestData()
        self.warning_identifier = None

    def setUp(self):
        """Setup test db"""
        Project.objects.all().delete()
        for project in self.data.projects:
            Project.objects.create(**project)

        WarningMessage.objects.all().delete()
        self.data.warning_message["project_identifier"] = Project.objects.filter(
            pk=self.data.warning_message["project_identifier"]
        ).first()
        warning_message = WarningMessage.objects.create(**self.data.warning_message)
        self.warning_identifier = warning_message.identifier

    def test_create_notification(self):
        """Create a notification"""
        data = {
            "title": "test",
            "body": "test",
            "warning_identifier": self.warning_identifier,
        }
        notification = Notification.objects.create(**data)
        notification.save()
        data = ArticleSerializer(notification, many=False).data

        self.assertEqual(data["project_identifier"], "0000000000")

    def test_serializer(self):
        """Test the serializer for notification messages"""
        data = {
            "title": "test",
            "body": "test",
            "warning_identifier": self.warning_identifier,
        }
        notification = Notification.objects.create(**data)
        serializer = ArticleSerializer(notification, many=False)
        serializer_data = dict(serializer.data)

        expected_result = {
            "identifier": str(notification.identifier),
            "project_identifier": "0000000000",
            "title": "test",
            "publication_date": str(notification.publication_date),
            "body": "test",
            "images": None,
            "assets": None,
            "last_seen": None,
        }

        self.assertDictEqual(serializer_data, expected_result)


class TestDeviceModel(TestCase):
    pass