import uuid
import logging
import os
from django.test import TestCase
from unittest.mock import patch, call
from amsterdam_app_api.UNITTESTS.mock_data import TestData
from amsterdam_app_api.UNITTESTS.mock_functions import firebase_admin_messaging_send_multicast
from amsterdam_app_api.PushNotifications.SendNotification import SendNotification
from amsterdam_app_api.models import MobileDevices
from amsterdam_app_api.models import Notification
from amsterdam_app_api.models import News
from amsterdam_app_api.models import WarningMessages
from amsterdam_app_api.models import ProjectManager
from amsterdam_app_api.api_messages import Messages

messages = Messages()


class TestSendNotification(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestSendNotification, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        ProjectManager.objects.all().delete()
        for project_manager in self.data.project_manager:
            ProjectManager.objects.create(**project_manager)

        news = News.objects.create(**self.data.news[0])
        self.news_identifier = news.identifier

        warning_message_data1 = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': {'preface': 'short text', 'content': 'long text'},
            'images': []
        }

        warning_message_data2 = {
            'title': 'title',
            'project_identifier': '0000000002',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': {'preface': 'short text', 'content': 'long text'},
            'images': []
        }
        WarningMessages.objects.all().delete()

        warning_message1 = WarningMessages.objects.create(**warning_message_data1)
        warning_message2 = WarningMessages.objects.create(**warning_message_data2)

        self.warning_identifier1 = str(warning_message1.identifier)
        self.warning_identifier2 = str(warning_message2.identifier)

        notification_message_data1 = {'title': 'title', 'body': 'text', 'warning_identifier': self.warning_identifier1}
        notification_message_data2 = {'title': 'title', 'body': 'text', 'warning_identifier': self.warning_identifier2}
        notification_message_data3 = {'title': 'title', 'body': 'text', 'news_identifier': self.news_identifier}

        notification1 = Notification.objects.create(**notification_message_data1)
        notification2 = Notification.objects.create(**notification_message_data2)
        notification3 = Notification.objects.create(**notification_message_data3)

        self.notification_identifier1 = str(notification1.identifier)
        self.notification_identifier2 = str(notification2.identifier)
        self.notification_identifier3 = str(notification3.identifier)

        mobile_devices = [
            {"device_token": "0000000000", "os_type": "ios", "projects": ["0000000000"]},
            {"device_token": "0000000001", "os_type": "ios", "projects": ["0000000001"]},
            {"device_token": "0000000002", "os_type": "ios", "projects": ["0000000000"]},
            {"device_token": "0000000003", "os_type": "ios", "projects": ["0000000001"]}
        ]
        for mobile_device in mobile_devices:
            MobileDevices.objects.create(**mobile_device)

    @patch('firebase_admin.messaging.send_multicast', side_effect=firebase_admin_messaging_send_multicast)
    def test_send_warning(self, firebase_admin_messaging_send_multicast):
        """ First message should always fail in the mocked send_multicast mock!!!
        """
        debug = os.environ.get('DEBUG', '')
        os.environ['DEBUG'] = 'false'

        mock_logging = logging.getLogger('amsterdam_app_api.GenericFunctions.Logger')
        with patch.object(mock_logging, 'error') as mocked_log:
            send_notification = SendNotification(self.notification_identifier1)
            send_notification.send_multicast_and_handle_errors()

            assert mocked_log.call_args_list == [call("List of tokens that caused failures: ['0000000000']")]
            self.assertEqual(len(send_notification.subscribed_device_batches), 1)
            self.assertEqual(len(send_notification.subscribed_device_batches[0]), 2)

        # reset environment
        os.environ['DEBUG'] = debug

    @patch('firebase_admin.messaging.send_multicast', side_effect=firebase_admin_messaging_send_multicast)
    def test_send_no_device_subscribed(self, firebase_admin_messaging_send_multicast):
        """ First message should always fail in the mocked send_multicast mock!!!
        """
        debug = os.environ.get('DEBUG', '')
        os.environ['DEBUG'] = 'false'

        mock_logging = logging.getLogger('amsterdam_app_api.GenericFunctions.Logger')
        with patch.object(mock_logging, 'error') as mocked_log:
            send_notification = SendNotification(self.notification_identifier2)
            send_notification.send_multicast_and_handle_errors()

            self.assertEqual(len(send_notification.subscribed_device_batches), 0)

        # reset environment
        os.environ['DEBUG'] = debug

    @patch('firebase_admin.messaging.send_multicast', side_effect=firebase_admin_messaging_send_multicast)
    def test_send_unknow_notification(self, firebase_admin_messaging_send_multicast):
        """ First message should always fail in the mocked send_multicast mock!!!
        """
        debug = os.environ.get('DEBUG', '')
        os.environ['DEBUG'] = 'false'

        mock_logging = logging.getLogger('amsterdam_app_api.GenericFunctions.Logger')
        with patch.object(mock_logging, 'error') as mocked_log:
            send_notification = SendNotification(str(uuid.uuid4()))
            send_notification.send_multicast_and_handle_errors()

            self.assertEqual(send_notification.notification, None)
            self.assertEqual(send_notification.project_identifier, None)
            self.assertEqual(send_notification.subscribed_device_batches, None)
            self.assertEqual(send_notification.valid_notification, False)
            assert  mocked_log.call_args_list == [call("Caught error in SendNotification.set_notification(): 'NoneType' object has no attribute 'project_identifier'")]

        # reset environment
        os.environ['DEBUG'] = debug

    @patch('firebase_admin.messaging.send_multicast', side_effect=firebase_admin_messaging_send_multicast)
    def test_send_news(self, firebase_admin_messaging_send_multicast):
        """ First message should always fail in the mocked send_multicast mock!!!
        """
        debug = os.environ.get('DEBUG', '')
        os.environ['DEBUG'] = 'false'

        mock_logging = logging.getLogger('amsterdam_app_api.GenericFunctions.Logger')
        with patch.object(mock_logging, 'error') as mocked_log:
            send_notification = SendNotification(self.notification_identifier3)
            send_notification.send_multicast_and_handle_errors()

            assert mocked_log.call_args_list == [call("List of tokens that caused failures: ['0000000000']")]
            self.assertEqual(len(send_notification.subscribed_device_batches), 1)
            self.assertEqual(len(send_notification.subscribed_device_batches[0]), 2)

        # reset environment
        os.environ['DEBUG'] = debug
