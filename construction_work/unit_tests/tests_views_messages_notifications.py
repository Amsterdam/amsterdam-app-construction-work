""" UNITTEST """
import json
import os
import uuid
from unittest.mock import patch

from django.test import Client, TestCase

from construction_work.api_messages import Messages
from construction_work.generic_functions.aes_cipher import AESCipher
from construction_work.models import FollowedProject, Project, ProjectManager, WarningMessage
from construction_work.models.device import Device
from construction_work.unit_tests.mock_data import TestData
from construction_work.unit_tests.mock_functions import firebase_admin_messaging_send_multicast

messages = Messages()


# TODO: fix tests
FirebaseToken = None

class TestApiNotification(TestCase):
    """UNITTEST"""

    def __init__(self, *args, **kwargs):
        super(TestApiNotification, self).__init__(*args, **kwargs)
        self.data = TestData()
        self.url = "/api/v1/notification"
        self.token = AESCipher("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", os.getenv("AES_SECRET")).encrypt()
        self.headers = {"UserAuthorization": self.token}
        self.content_type = "application/json"
        self.client = Client()
        self.warning_identifier = None

    def setUp(self):
        """Setup test db"""
        for project in self.data.projects:
            Project.objects.create(**project)

        ProjectManager.objects.all().delete()
        for project_manager in self.data.project_manager:
            ProjectManager.objects.create(**project_manager)

        data = {
            "title": "title",
            "project_identifier": Project.objects.filter(pk="0000000000").first(),
            "project_manager_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "body": {"preface": "short text", "content": "long text"},
            "images": [],
        }
        WarningMessage.objects.all().delete()
        warning_message = WarningMessage.objects.create(**data)
        self.warning_identifier = str(warning_message.identifier)

    @patch("firebase_admin.messaging.send_multicast", side_effect=firebase_admin_messaging_send_multicast)
    def test_post_notification(self, _firebase_admin_messaging_send_multicast):
        """Test post notification"""
        Device.objects.all().delete()
        devices = []
        for device in self.data.devices:
            device = Device.objects.create(**device)
            devices.append(device)

        FirebaseToken.objects.all().delete()
        for i, token in enumerate(self.data.firebase_tokens):
            FirebaseToken.objects.create(device=devices[i], **token)
        
        FollowedProject.objects.all().delete()
        for project in self.data.followed_projects:
            FollowedProject.objects.create(**project)

        data = {"title": "title", "body": "text", "warning_identifier": self.warning_identifier}
        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {"status": True, "result": "push-notification accepted"})

    @patch("firebase_admin.messaging.send_multicast", side_effect=firebase_admin_messaging_send_multicast)
    def test_post_notification_no_subscriptions(self, _firebase_admin_messaging_send_multicast):
        """Test post notification without subscriptions"""
        data = {"title": "title", "body": "text", "warning_identifier": self.warning_identifier}
        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {"status": False, "result": "No subscribed devices found"})

    def test_post_notification_no_warning_message(self):
        """Test post notification without a warning message"""
        data = {"title": "title", "body": "text", "warning_identifier": str(uuid.uuid4())}
        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 404)
        self.assertDictEqual(result.data, {"status": False, "result": messages.no_record_found})

    def test_post_notification_no_news_message(self):
        """Test post notification without a news message"""
        data = {"title": "title", "body": "text", "warning_identifier": self.warning_identifier, "news_identifier": ""}
        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 404)
        self.assertDictEqual(result.data, {"status": False, "result": messages.no_record_found})

    def test_post_notification_no_identifiers(self):
        """test post a notification without an identifier"""
        data = {"title": "title", "body": "text"}
        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {"status": False, "result": messages.invalid_query})

    def test_post_notification_without_title_or_body(self):
        """Post notification without a title or body"""
        data = {}
        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {"status": False, "result": messages.invalid_query})

    @patch("firebase_admin.messaging.send_multicast", side_effect=firebase_admin_messaging_send_multicast)
    def test_get_notification(self, _firebase_admin_messaging_send_multicast):
        """Get notifications from db"""
        
        Device.objects.all().delete()
        devices = []
        for device in self.data.devices:
            device = Device.objects.create(**device)
            devices.append(device)

        FirebaseToken.objects.all().delete()
        for i, token in enumerate(self.data.firebase_tokens):
            FirebaseToken.objects.create(device=devices[i], **token)

        FollowedProject.objects.all().delete()
        for project in self.data.followed_projects:
            FollowedProject.objects.create(**project)

        data = {"title": "title", "body": "text", "warning_identifier": self.warning_identifier}
        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {"status": True, "result": "push-notification accepted"})

        result = self.client.get("{url}s?project-ids=0000000000".format(url=self.url))
        result_data = json.loads(result.content.decode())
        identifier = result_data["result"][0]["identifier"]
        expected_result = {
            "status": True,
            "result": [
                {
                    "identifier": identifier,
                    "title": "title",
                    "body": "text",
                    "project_identifier": "0000000000",
                    "news_identifier": None,
                    "warning_identifier": self.warning_identifier,
                    "publication_date": result_data["result"][0]["publication_date"],
                }
            ],
        }

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result_data, expected_result)

    @patch("firebase_admin.messaging.send_multicast", side_effect=firebase_admin_messaging_send_multicast)
    def test_get_notification_inactive_project(self, _firebase_admin_messaging_send_multicast):
        """Get notifications on inactive projects"""
        Device.objects.all().delete()
        devices = []
        for device in self.data.devices:
            device = Device.objects.create(**device)
            devices.append(device)

        FirebaseToken.objects.all().delete()
        for i, token in enumerate(self.data.firebase_tokens):
            FirebaseToken.objects.create(device=devices[i], **token)

        FollowedProject.objects.all().delete()
        for project in self.data.followed_projects:
            FollowedProject.objects.create(**project)

        data = {"title": "title", "body": "text", "warning_identifier": self.warning_identifier}
        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {"status": True, "result": "push-notification accepted"})

        project = Project.objects.filter(pk="0000000000").first()
        project.active = False
        project.save()

        result = self.client.get("{url}s?project-ids=0000000000".format(url=self.url))

        self.assertEqual(result.status_code, 404)
        self.assertDictEqual(result.data, {"status": False, "result": "No record found"})

    def test_get_notification_invalid_query(self):
        """Get notifications with an invalid query"""
        result = self.client.get("{url}s".format(url=self.url))

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {"status": False, "result": messages.invalid_query})
