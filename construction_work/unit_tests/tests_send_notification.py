""" unit_tests """
import logging
import os
import uuid
from unittest.mock import call, patch

from django.test import TestCase

from construction_work.api_messages import Messages
from construction_work.models import (
    Article,
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


# TODO: actually test notification service methods
class TestSendNotification(TestCase):
    """unit_tests"""

    def setUp(self):
        """Setup test db"""
        self.data = TestData()

        projects = []
        for project in self.data.projects:
            new_project = Project.objects.create(**project)
            projects.append(new_project)

        project_managers = []
        for project_manager in self.data.project_managers:
            new_project_manager = ProjectManager.objects.create(**project_manager)
            project_managers.append(new_project_manager)

        warning_message_data1 = {
            "title": "title",
            "project": projects[0],
            "project_manager": project_managers[0],
            "body": {"preface": "short text", "content": "long text"},
        }

        warning_message_data2 = {
            "title": "title",
            "project": projects[1],
            "project_manager": project_managers[1],
            "body": {"preface": "short text", "content": "long text"},
        }

        warning_message1 = WarningMessage.objects.create(**warning_message_data1)
        warning_message2 = WarningMessage.objects.create(**warning_message_data2)

        notification_message_data1 = {
            "title": "title",
            "body": "text",
            "warning": warning_message1,
        }
        notification_message_data2 = {
            "title": "title",
            "body": "text",
            "warning": warning_message2,
        }

        self.notification1 = Notification.objects.create(**notification_message_data1)
        self.notification2 = Notification.objects.create(**notification_message_data2)

        for device in self.data.devices:
            new_device = Device.objects.create(**device)
            new_device.followed_projects.add(projects[0])

    def tearDown(self):
        """Remove test db items"""
        Project.objects.all().delete()
        ProjectManager.objects.all().delete()
        WarningMessage.objects.all().delete()
        Device.objects.all().delete()

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

        mock_logging = logging.getLogger(
            "construction_work.generic_functions.generic_logger"
        )
        with patch.object(mock_logging, "error") as mocked_log:
            send_notification = NotificationService(self.notification1)
            send_notification.setup()
            send_notification.send_multicast_and_handle_errors()

            assert mocked_log.call_args_list == [
                call("List of tokens that caused failures: ['foobar_token1']")
            ]
            self.assertEqual(len(send_notification.subscribed_device_batches), 1)
            self.assertEqual(len(send_notification.subscribed_device_batches[0]), 2)

        # reset environment
        os.environ["DEBUG"] = debug
