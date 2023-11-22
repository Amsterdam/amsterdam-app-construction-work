""" unit_tests """
import logging
from unittest.mock import call, patch

from django.test import TestCase

from construction_work.api_messages import Messages
from construction_work.models import (
    Notification,
    Project,
    ProjectManager,
    WarningMessage,
)
from construction_work.models.device import Device
from construction_work.push_notifications.send_notification import NotificationService
from construction_work.unit_tests.mock_data import TestData
from construction_work.unit_tests.mock_functions import (
    firebase_admin_messaging_send_multicast,
)

messages = Messages()


class TestNotificationService(TestCase):
    def setUp(self) -> None:
        """Setup data for testing notification service"""
        self.data = TestData()

        project_manager = ProjectManager.objects.create(**self.data.project_managers[0])

        # Create notification for project with following devices
        self.notification_with_followers = self.create_notification(
            self.data.projects[0], project_manager
        )

        for device in self.data.devices:
            new_device = Device.objects.create(**device)
            new_device.followed_projects.add(
                self.notification_with_followers.warning.project
            )

        # Create notification for project with following devices
        self.notification_without_followers = self.create_notification(
            self.data.projects[1], project_manager
        )

    def create_notification(self, project_data, project_manager):
        """Helper function to create notification"""
        project = Project.objects.create(**project_data)

        warning_message_data = {
            "title": "title",
            "project": project,
            "project_manager": project_manager,
            "body": {"preface": "short text", "content": "long text"},
        }
        warning_message1 = WarningMessage.objects.create(**warning_message_data)

        notification_message_data = {
            "title": "title",
            "body": "text",
            "warning": warning_message1,
        }
        notification = Notification.objects.create(**notification_message_data)
        return notification

    def test_create_token_batches_for_followed_project(self):
        """Test if batches are created as expected with a followed project"""
        ns = NotificationService(self.notification_with_followers, 1)
        created_batch = ns._create_subscribed_device_batches()
        expected_tokens = [[x["firebase_token"]] for x in self.data.devices]

        self.assertEqual(len(created_batch), 2)
        self.assertEqual(created_batch, expected_tokens)

    def test_create_token_batches_for_non_followed_project(self):
        """Test if batches are created as expected with a project without followers"""
        ns = NotificationService(self.notification_without_followers, 1)
        created_batch = ns._create_subscribed_device_batches()

        self.assertEqual(len(created_batch), 0)
        self.assertEqual(created_batch, [])

    def test_setup_creates_firebase_notification_instance(self):
        """Test if firebase notification object is created"""
        ns = NotificationService(self.notification_with_followers, 1)
        ns.setup()

        self.assertIsNotNone(ns.firebase_notification)

    def test_setup_creates_batches_and_returns_true(self):
        """Test if setup creates batches and therefor returns true"""
        ns = NotificationService(self.notification_with_followers, 1)
        setup_result = ns.setup()
        created_batch = ns.subscribed_device_batches
        expected_tokens = [[x["firebase_token"]] for x in self.data.devices]

        self.assertEqual(len(created_batch), 2)
        self.assertEqual(created_batch, expected_tokens)
        self.assertTrue(setup_result)

    def test_setup_returns_false_with_empty_batch_list(self):
        """Test if setup returns false if no batches were created"""
        ns = NotificationService(self.notification_without_followers, 1)
        setup_result = ns.setup()

        self.assertFalse(setup_result)

        ns = NotificationService(self.notification_with_followers, 1)
        ns.setup()
        ns.send_multicast_and_handle_errors()

    @patch(
        "firebase_admin.messaging.send_each_for_multicast",
        side_effect=firebase_admin_messaging_send_multicast,
    )
    def test_send_multicast_mock_function(self, _):
        """First message should always fail in the mocked send_multicast mock!!!
        Send warning message
        """

        mock_logging = logging.getLogger(
            "construction_work.generic_functions.generic_logger"
        )
        with patch.object(mock_logging, "error") as mocked_log:
            ns = NotificationService(self.notification_with_followers)
            ns.setup()
            ns.send_multicast_and_handle_errors()

            assert mocked_log.call_args_list == [
                call("List of tokens that caused failures: ['foobar_token1']")
            ]
            self.assertEqual(len(ns.subscribed_device_batches), 1)
            self.assertEqual(len(ns.subscribed_device_batches[0]), 2)
