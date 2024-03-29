""" UNITTEST """
import json
import os
from unittest.mock import patch

from django.test import Client, TestCase

from construction_work.api_messages import Messages
from construction_work.generic_functions.aes_cipher import AESCipher
from construction_work.models import Project, ProjectManager, WarningMessage
from construction_work.models.device import Device
from construction_work.models.warning_and_notification import Notification
from construction_work.unit_tests.mock_data import TestData
from construction_work.unit_tests.mock_functions import (
    firebase_admin_messaging_send_multicast,
)

messages = Messages()


class TestApiNotification(TestCase):
    """Test notifications API views"""

    def setUp(self):
        """Setup test db"""
        self.data = TestData()
        self.post_url = "/api/v1/notification"
        self.get_url = "/api/v1/notifications"

        # app_token = os.getenv("APP_TOKEN")
        self.aes_secret = os.getenv("AES_SECRET")
        # self.token = AESCipher(app_token, aes_secret).encrypt()
        # self.headers = {"DeviceAuthorization": self.token}
        self.content_type = "application/json"
        self.client = Client()
        self.token = None

        for project in self.data.projects:
            project = Project.objects.create(**project)

        for project_manager in self.data.project_managers:
            ProjectManager.objects.create(**project_manager)

    def tearDown(self) -> None:
        ProjectManager.objects.all().delete()
        WarningMessage.objects.all().delete()
        Device.objects.all().delete()

    def get_user_auth_header(self, manager_key):
        """Get user auth header"""
        self.token = AESCipher(manager_key, self.aes_secret).encrypt()
        headers = {"UserAuthorization": self.token}
        return headers

    def get_device_auth_header(self):
        """Get device auth header"""
        app_token = os.getenv("APP_TOKEN")
        self.token = AESCipher(app_token, self.aes_secret).encrypt()
        headers = {"DeviceAuthorization": self.token}
        return headers

    @patch(
        "firebase_admin.messaging.send_multicast",
        side_effect=firebase_admin_messaging_send_multicast,
    )
    def test_post_notification_with_subscribed_device(self, _):
        """Test creating new notification when there is a subscribed device to the related warning"""
        project = Project.objects.first()
        project_manager = ProjectManager.objects.first()

        device_data = self.data.devices[0]
        device = Device.objects.create(**device_data)
        device.followed_projects.add(project)

        warning_data = {
            "title": "foobar",
            "body": "foobar",
            "project": project,
            "project_manager": project_manager,
        }
        warning_message = WarningMessage.objects.create(**warning_data)

        data = {"title": "foobar", "body": "foobar", "warning_id": warning_message.pk}
        headers = self.get_user_auth_header(str(project_manager.manager_key))
        result = self.client.post(
            self.post_url,
            json.dumps(data),
            headers=headers,
            content_type=self.content_type,
        )

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, "Push notifications sent")

        notification = Notification.objects.filter(warning=warning_message.pk).first()
        self.assertIsNotNone(notification)

    @patch(
        "firebase_admin.messaging.send_multicast",
        side_effect=firebase_admin_messaging_send_multicast,
    )
    def test_post_notification_no_subscriptions(self, _):
        """Test creating new notification without subscriptions"""
        project = Project.objects.first()
        project_manager = ProjectManager.objects.first()

        warning_data = {
            "title": "foobar",
            "body": "foobar",
            "project": project,
            "project_manager": project_manager,
        }
        warning_message = WarningMessage.objects.create(**warning_data)

        data = {"title": "foobar", "body": "foobar", "warning_id": warning_message.pk}
        headers = self.get_user_auth_header(str(project_manager.manager_key))
        result = self.client.post(
            self.post_url,
            json.dumps(data),
            headers=headers,
            content_type=self.content_type,
        )

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, "No subscribed devices found")

        notifications = list(Notification.objects.all())
        self.assertEqual(notifications, [])

    def test_post_notification_no_warning_message(self):
        """Test post notification without a warning message"""
        project_manager = ProjectManager.objects.first()
        headers = self.get_user_auth_header(str(project_manager.manager_key))

        data = {"title": "title", "body": "text", "warning_id": 9999}
        result = self.client.post(
            self.post_url,
            json.dumps(data),
            headers=headers,
            content_type=self.content_type,
        )

        self.assertEqual(result.status_code, 404)
        self.assertEqual(result.data, messages.no_record_found)

        notifications = list(Notification.objects.all())
        self.assertEqual(notifications, [])

    def test_post_notification_without_warning_id(self):
        """test post a notification without a warning id"""
        project_manager = ProjectManager.objects.first()
        headers = self.get_user_auth_header(str(project_manager.manager_key))

        data = {"title": "title", "body": "text"}
        result = self.client.post(
            self.post_url,
            json.dumps(data),
            headers=headers,
            content_type=self.content_type,
        )

        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data, messages.invalid_query)

    def test_post_notification_without_title(self):
        """test post a notification without a warning id"""
        project = Project.objects.first()
        project_manager = ProjectManager.objects.first()

        warning_data = {
            "title": "foobar",
            "body": "foobar",
            "project": project,
            "project_manager": project_manager,
        }
        warning_message = WarningMessage.objects.create(**warning_data)

        headers = self.get_user_auth_header(str(project_manager.manager_key))
        data = {"body": "foobar", "warning_id": warning_message.pk}
        result = self.client.post(
            self.post_url,
            json.dumps(data),
            headers=headers,
            content_type=self.content_type,
        )

        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data, messages.invalid_query)

    def test_post_notification_without_body(self):
        """test post a notification without a warning id"""
        project = Project.objects.first()
        project_manager = ProjectManager.objects.first()

        warning_data = {
            "title": "foobar",
            "body": "foobar",
            "project": project,
            "project_manager": project_manager,
        }
        warning_message = WarningMessage.objects.create(**warning_data)

        headers = self.get_user_auth_header(str(project_manager.manager_key))
        data = {"title": "foobar", "warning_id": warning_message.pk}
        result = self.client.post(
            self.post_url,
            json.dumps(data),
            headers=headers,
            content_type=self.content_type,
        )

        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data, messages.invalid_query)
