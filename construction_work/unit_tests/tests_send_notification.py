""" unit_tests """
import logging
import os
import uuid
from unittest.mock import call, patch

from django.test import TestCase

from construction_work.api_messages import Messages
from construction_work.models import Article, Notification, Project, ProjectManager, WarningMessage
from construction_work.models.device import Device
from construction_work.push_notifications.send_notification import NotificationService
from construction_work.unit_tests.mock_data import TestData
from construction_work.unit_tests.mock_functions import firebase_admin_messaging_send_multicast

messages = Messages()


class TestSendNotification(TestCase):
    """unit_tests"""

    def __init__(self, *args, **kwargs):
        super(TestSendNotification, self).__init__(*args, **kwargs)
        self.data = TestData()

    def tearDown(self):
        """Remove test db items"""
        pass  # pylint: disable=unnecessary-pass

    def setUp(self):
        """Setup test db"""
        Project.objects.all().delete()
        projects = []
        for project in self.data.projects:
            new_project = Project.objects.create(**project)
            projects.append(new_project)

        ProjectManager.objects.all().delete()
        for project_manager in self.data.project_managers:
            ProjectManager.objects.create(**project_manager)

        self.data.articles[0]["project_identifier"] = Project.objects.filter(
            pk=self.data.articles[0]["project_identifier"]
        ).first()
        news = Article.objects.create(**self.data.articles[0])
        self.news_identifier = news.foreign_id

        warning_message_data1 = {
            "title": "title",
            "project_identifier": projects[0],
            "project_manager_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "body": {"preface": "short text", "content": "long text"},
            "images": [],
        }

        warning_message_data2 = {
            "title": "title",
            "project_identifier": projects[1],
            "project_manager_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "body": {"preface": "short text", "content": "long text"},
            "images": [],
        }
        WarningMessage.objects.all().delete()

        warning_message1 = WarningMessage.objects.create(**warning_message_data1)
        warning_message2 = WarningMessage.objects.create(**warning_message_data2)

        self.warning_identifier1 = str(warning_message1.identifier)
        self.warning_identifier2 = str(warning_message2.identifier)

        notification_message_data1 = {
            "title": "title",
            "body": "text",
            "warning_identifier": self.warning_identifier1,
        }
        notification_message_data2 = {
            "title": "title",
            "body": "text",
            "warning_identifier": self.warning_identifier2,
        }
        notification_message_data3 = {
            "title": "title",
            "body": "text",
            "news_identifier": self.news_identifier,
        }

        notification1 = Notification.objects.create(**notification_message_data1)
        notification2 = Notification.objects.create(**notification_message_data2)
        notification3 = Notification.objects.create(**notification_message_data3)

        self.notification_identifier1 = str(notification1.identifier)
        self.notification_identifier2 = str(notification2.identifier)
        self.notification_identifier3 = str(notification3.identifier)

        Device.objects.all().delete()
        for device in self.data.devices:
            new_device = Device.objects.create(**device)
            new_device.followed_projects.add(projects[0])

    @patch(
        "firebase_admin.messaging.send_each_for_multicast",
        side_effect=firebase_admin_messaging_send_multicast,
    )
    def test_send_warning(self, _firebase_admin_messaging_send_multicast):
        """First message should always fail in the mocked send_multicast mock!!!
        Send warning message
        """
        debug = os.environ.get("DEBUG", "")
        os.environ["DEBUG"] = "false"

        mock_logging = logging.getLogger("construction_work.generic_functions.generic_logger")
        with patch.object(mock_logging, "error") as mocked_log:
            send_notification = NotificationService(self.notification_identifier1)
            send_notification.send_multicast_and_handle_errors()

            assert mocked_log.call_args_list == [call("List of tokens that caused failures: ['foobar_token1']")]
            self.assertEqual(len(send_notification.subscribed_device_batches), 1)
            self.assertEqual(len(send_notification.subscribed_device_batches[0]), 2)

        # reset environment
        os.environ["DEBUG"] = debug

    @patch(
        "firebase_admin.messaging.send_each_for_multicast",
        side_effect=firebase_admin_messaging_send_multicast,
    )
    def test_send_unknown_notification(self, _firebase_admin_messaging_send_multicast):
        """First message should always fail in the mocked send_multicast mock!!!
        Send non-existing notification
        """
        debug = os.environ.get("DEBUG", "")
        os.environ["DEBUG"] = "false"

        mock_logging = logging.getLogger("construction_work.generic_functions.generic_logger")
        with patch.object(mock_logging, "error") as mocked_log:
            send_notification = NotificationService(str(uuid.uuid4()))
            send_notification.send_multicast_and_handle_errors()

            self.assertEqual(send_notification.firebase_notification, None)
            self.assertEqual(send_notification.project_id, None)
            self.assertEqual(send_notification.subscribed_device_batches, None)
            self.assertEqual(send_notification.valid_notification, False)
            expected_result = [
                call(
                    "Caught error in SendNotification.set_notification(): "
                    "'NoneType' object has no attribute 'project_identifier_id'"
                )
            ]
            assert mocked_log.call_args_list == expected_result

        # reset environment
        os.environ["DEBUG"] = debug

    @patch(
        "firebase_admin.messaging.send_each_for_multicast",
        side_effect=firebase_admin_messaging_send_multicast,
    )
    def test_send_news(self, _firebase_admin_messaging_send_multicast):
        """First message should always fail in the mocked send_multicast mock!!!
        Send news item as notification
        """
        debug = os.environ.get("DEBUG", "")
        os.environ["DEBUG"] = "false"

        mock_logging = logging.getLogger("construction_work.generic_functions.generic_logger")
        with patch.object(mock_logging, "error") as mocked_log:
            send_notification = NotificationService(self.notification_identifier3)
            send_notification.send_multicast_and_handle_errors()

            assert mocked_log.call_args_list == [call("List of tokens that caused failures: ['foobar_token1']")]
            self.assertEqual(len(send_notification.subscribed_device_batches), 1)
            self.assertEqual(len(send_notification.subscribed_device_batches[0]), 2)

        # reset environment
        os.environ["DEBUG"] = debug
