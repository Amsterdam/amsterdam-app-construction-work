""" unit_tests """
from datetime import datetime
import uuid
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from django.test import TestCase
from construction_work.generic_functions.date_translation import translate_timezone

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
from construction_work.models.device import Device
from construction_work.models.project import Project
from construction_work.models.project_manager import ProjectManager
from construction_work.models.warning_and_notification import WarningMessage

from construction_work.serializers import (
    ArticleSerializer,
    AssetsSerializer,
    ImageSerializer,
    Notification,
    NotificationSerializer,
    ProjectCreateSerializer,
    ProjectManagerSerializer,
    WarningMessagePublicSerializer,
)
from construction_work.unit_tests.mock_data import TestData
from construction_work.generic_functions.generic_logger import Logger


logger = Logger()


class TestAssetModel(TestCase):
    """Test asset model"""

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
    """Test image model"""

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
    """Test project model"""

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

        target_dt = datetime.fromisoformat(serializer.data["creation_date"])

        first_project["creation_date"] = translate_timezone(
            first_project["creation_date"], target_dt.tzinfo
        )
        first_project["modification_date"] = translate_timezone(
            first_project["modification_date"], target_dt.tzinfo
        )
        first_project["publication_date"] = translate_timezone(
            first_project["publication_date"], target_dt.tzinfo
        )
        first_project["expiration_date"] = translate_timezone(
            first_project["expiration_date"], target_dt.tzinfo
        )

        self.assertDictEqual(serializer.data, first_project)

    def test_projects_does_not_exist(self):
        """test not exist"""
        projects_objects = Project.objects.filter(project_id=9999).first()

        self.assertEqual(projects_objects, None)


class TestArticleModel(TestCase):
    """Test article model"""

    def setUp(self):
        self.data = TestData()

        for project in self.data.projects:
            Project.objects.create(**project)

        for article in self.data.articles:
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
        self.data.articles[0]["last_seen"] = serializer.data["last_seen"]

        self.assertEqual(self.data.articles[0]["active"], True)

    def test_article_does_not_exist(self):
        """test not exist"""
        news_object = Article.objects.filter(article_id=9999).first()

        self.assertEqual(news_object, None)


class TestProjectManagerModel(TestCase):
    """Test project manager model"""

    def setUp(self):
        """unit_tests db setup"""
        self.data = TestData()

        for project in self.data.projects:
            Project.objects.create(**project)

        for pm in self.data.project_managers:
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
    """Test warning message model"""

    def setUp(self):
        """Setup test db"""
        self.data = TestData()
        for project in self.data.projects:
            Project.objects.create(**project)

        for project_manager in self.data.project_managers:
            ProjectManager.objects.create(**project_manager)

    def tearDown(self) -> None:
        Project.objects.all().delete()
        WarningMessage.objects.all().delete()
        ProjectManager.objects.all().delete()
        return super().tearDown()

    def create_message(self):
        message_data = self.data.warning_message
        message_data["project_id"] = Project.objects.first().pk
        message_data["project_manager_id"] = ProjectManager.objects.first().pk

        warning_message = WarningMessage.objects.create(**message_data)
        return warning_message

    def test_create_message(self):
        """Test create warning message"""
        warning_message = self.create_message()

        self.assertEqual(
            warning_message.author_email, self.data.project_managers[0]["email"]
        )
        self.assertIsNotNone(warning_message.publication_date)
        self.assertIsNotNone(warning_message.modification_date)

    def test_modification_date(self):
        """test modification date on changing a message"""
        warning_message = self.create_message()

        original_date = warning_message.modification_date
        warning_message.save()
        updateded_date = warning_message.modification_date

        self.assertNotEqual(original_date, updateded_date)

    def test_serializer_internal(self):
        """Purpose: test if project_manager_id is present in serializer"""
        warning_message = self.create_message()

        serializer = WarningMessagePublicSerializer(
            instance=warning_message, data={}, partial=True
        )
        self.assertTrue(serializer.is_valid())
        serializer.data

        expected_result = {
            "id": serializer.data["id"],
            "title": "warning message title",
            "body": "warning message body",
            "project_id": "2048",
            "project_manager_key": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "publication_date": serializer.data["publication_date"],
            "modification_date": serializer.data["modification_date"],
            "author_email": "mock0@amsterdam.nl",
            "images": [],
        }

        self.assertDictEqual(serializer.data, expected_result)


class TestNotificationModel(TestCase):
    """Test notification model"""

    def setUp(self):
        """Setup test db"""
        self.data = TestData()
        project = Project.objects.create(**self.data.projects[0])
        project_manager = ProjectManager.objects.create(**self.data.project_managers[0])

        message_data = self.data.warning_message
        message_data["project_id"] = project.pk
        message_data["project_manager_id"] = project_manager.pk
        self.warning_message = WarningMessage.objects.create(**message_data)

    def tearDown(self) -> None:
        Project.objects.all().delete()
        WarningMessage.objects.all().delete()

        return super().tearDown()

    def test_create_notification(self):
        """Create a notification"""
        data = {
            "title": "notification title",
            "body": "notification subtitle",
            "warning": self.warning_message,
        }
        notification = Notification.objects.create(**data)
        notification.save()

        self.assertEqual(len(Notification.objects.all()), 1)

    def test_serializer(self):
        """Test the serializer for notification messages"""
        data = {
            "title": "notification title",
            "body": "notification body",
            "warning": self.warning_message.pk,
        }
        serializer = NotificationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        expected_result = {
            "id": serializer.data["id"],
            "title": data["title"],
            "body": data["body"],
            "warning": self.warning_message.pk,
            "publication_date": serializer.data["publication_date"],
        }

        self.assertDictEqual(serializer.data, expected_result)


class TestDeviceModel(TestCase):
    "Test device model"

    def setUp(self) -> None:
        """Set up test data"""
        self.data = TestData()

    def test_create_devices(self):
        """Test creating new devices"""
        for device in self.data.devices:
            Device.objects.create(**device)

        self.assertEqual(len(Device.objects.all()), 2)

    def test_device_id_not_unique(self):
        """Test of device id uniqueness"""
        first_device_data = self.data.devices[0]
        Device.objects.create(**first_device_data)

        second_device_data = self.data.devices[1]
        second_device_data["device_id"] = first_device_data["device_id"]
        with self.assertRaises(IntegrityError) as context:
            Device.objects.create(**second_device_data)

        self.assertIn("device_id", context.exception.args[0])

    def test_firebase_token_not_unique(self):
        """Test firebase token uniqueness"""
        first_device_data = self.data.devices[0]
        Device.objects.create(**first_device_data)

        second_device_data = self.data.devices[1]
        second_device_data["firebase_token"] = first_device_data["firebase_token"]
        with self.assertRaises(IntegrityError) as context:
            Device.objects.create(**second_device_data)

        self.assertIn("firebase_token", context.exception.args[0])

    def test_firebase_token_can_be_null(self):
        """Test that firebasetoken can be null"""
        first_device_data = self.data.devices[0]
        first_device_data["firebase_token"] = None
        Device.objects.create(**first_device_data)

        self.assertEqual(len(Device.objects.all()), 1)

    def test_last_access_is_updated(self):
        """Test that last access is updated"""
        first_device_data = self.data.devices[0]
        device = Device.objects.create(**first_device_data)
        initial_access_date = device.last_access

        device.save()
        updated_access_date = device.last_access

        self.assertNotEqual(initial_access_date, updated_access_date)

    def test_add_and_remove_followed_project(self):
        """Test if project can added and removed"""
        first_project = self.data.projects[0]
        project = Project.objects.create(**first_project)

        first_device_data = self.data.devices[0]
        device = Device.objects.create(**first_device_data)
        device.followed_projects.add(project)
        self.assertEqual(len(device.followed_projects.all()), 1)

        device.followed_projects.remove(project)

        self.assertEqual(len(device.followed_projects.all()), 0)
