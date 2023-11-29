""" unit_tests """

import base64
import json
import os
import uuid
from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from construction_work.api_messages import Messages
from construction_work.generic_functions.aes_cipher import AESCipher
from construction_work.generic_functions.date_translation import translate_timezone
from construction_work.models import Project, ProjectManager, WarningMessage
from construction_work.serializers import WarningMessagePublicSerializer
from construction_work.unit_tests.mock_data import TestData

messages = Messages()

MOCK_USERNAME = "mock"
MOCK_PASSWORD = "mock"
MOCK_EMAIL = "mock@localhost"


class TestApiProjectWarning(TestCase):
    """Test project warnings"""

    @staticmethod
    def read_file(filename):
        """Read data from file"""
        with open(filename, "rb") as f:
            data = f.read()
        return data

    def setUp(self):
        """setup test db"""
        self.maxDiff = None
        self.data = TestData()
        self.client = Client()

        self.url = "/api/v1/project/warning"
        self.url_warnings_get = "/api/v1/project/warnings"
        self.aes_secret = os.getenv("AES_SECRET")
        self.content_type = "application/json"

        # Create user for token
        self.user = get_user_model().objects.create_user(
            username=MOCK_USERNAME, password=MOCK_PASSWORD, email=MOCK_EMAIL
        )
        self.user.save()

        for project in self.data.projects:
            Project.objects.create(**project)

        for project_manager in self.data.project_managers:
            ProjectManager.objects.create(**project_manager)

    def tearDown(self):
        WarningMessage.objects.all().delete()
        Project.objects.all().delete()
        ProjectManager.objects.all().delete()

    def get_user_auth_header(self, manager_key):
        self.token = AESCipher(manager_key, self.aes_secret).encrypt()
        headers = {"UserAuthorization": self.token}
        return headers

    def get_device_auth_header(self):
        app_token = os.getenv("APP_TOKEN")
        self.token = AESCipher(app_token, self.aes_secret).encrypt()
        headers = {"DeviceAuthorization": self.token}
        return headers

    def get_jwt_auth_header(self):
        response = self.client.post(
            "/api/v1/get-token/", {"username": MOCK_USERNAME, "password": MOCK_PASSWORD}
        )
        headers = {"AUTHORIZATION": response.data["access"]}
        return headers

    def create_message_from_data(self, data) -> WarningMessage:
        project_obj = Project.objects.filter(
            foreign_id=data.get("project_foreign_id")
        ).first()
        project_obj.save()

        project_manager = ProjectManager.objects.filter(
            manager_key=data.get("project_manager_key")
        ).first()
        project_manager.projects.add(project_obj)

        new_message = WarningMessage(
            title=data.get("title"),
            body=data.get("body"),
            project=project_obj,
            project_manager=project_manager,
        )
        new_message.save()
        return new_message

    def test_post_warning_message_valid(self):
        """Test posting valid warning message"""
        project_obj = Project.objects.filter(foreign_id=2048).first()

        data = {
            "title": "foobar title",
            "body": "foobar body",
            "project_id": project_obj.pk,
            "project_manager_key": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        }

        project_manager = ProjectManager.objects.filter(
            manager_key=data.get("project_manager_key")
        ).first()
        project_manager.projects.add(project_obj)

        headers = self.get_user_auth_header(data["project_manager_key"])
        result = self.client.post(
            self.url, json.dumps(data), headers=headers, content_type=self.content_type
        )
        self.assertEqual(result.status_code, 200)

        target_dt = datetime.fromisoformat(result.data["publication_date"])

        warning_message = WarningMessage.objects.filter(
            project__id=project_obj.pk
        ).first()

        expected_result = {
            "id": warning_message.pk,
            "title": "foobar title",
            "body": "foobar body",
            "publication_date": translate_timezone(
                str(warning_message.publication_date), target_dt.tzinfo
            ),
            "modification_date": translate_timezone(
                str(warning_message.modification_date), target_dt.tzinfo
            ),
            "author_email": "mock0@amsterdam.nl",
            "project": project_obj.pk,
            "project_manager": project_manager.pk,
        }

        self.assertDictEqual(result.data, expected_result)

    def test_post_warning_message_invalid_project_id_I(self):
        """Test add message for unknown project"""
        data = {
            "title": "foobar title",
            "body": "foobar body",
            "project_id": "1",
            "project_manager_key": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        }

        headers = self.get_user_auth_header(data["project_manager_key"])
        result = self.client.post(
            self.url, json.dumps(data), headers=headers, content_type=self.content_type
        )

        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data, messages.invalid_query)

    def test_post_warning_message_invalid_project_id_II(self):
        """Test add message for unknown project"""
        data = {
            "title": "foobar title",
            "body": "foobar body",
            "project_id": 9999,
            "project_manager_key": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        }

        headers = self.get_user_auth_header(data["project_manager_key"])
        result = self.client.post(
            self.url, json.dumps(data), headers=headers, content_type=self.content_type
        )

        self.assertEqual(result.status_code, 404)
        self.assertEqual(result.data, messages.no_record_found)

    def test_post_warning_message_invalid_project_manager(self):
        """test posting from a non-existing project manager"""
        project_obj = Project.objects.filter(foreign_id=2048).first()
        data = {
            "title": "foobar title",
            "body": "foobar body",
            "project_id": project_obj.pk,
            "project_manager_key": str(uuid.uuid4()),
        }

        headers = self.get_user_auth_header(data["project_manager_key"])
        result = self.client.post(
            self.url, json.dumps(data), headers=headers, content_type=self.content_type
        )

        self.assertEqual(result.status_code, 403)

    def test_post_warning_message_non_authorized_project_manager(self):
        """test posting from a non-existing project manager"""

        project_manager = ProjectManager.objects.filter(
            manager_key="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
        ).first()
        project_obj = Project.objects.filter(foreign_id=2048).first()

        # Remove the project manager from the project's managers
        project_obj.projectmanager_set.remove(project_manager)

        data = {
            "title": "foobar title",
            "body": "foobar body",
            "project_id": project_obj.pk,
            "project_manager_key": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        }

        headers = self.get_user_auth_header(data["project_manager_key"])
        result = self.client.post(
            self.url, json.dumps(data), headers=headers, content_type=self.content_type
        )

        self.assertEqual(result.status_code, 403)

    def test_post_warning_message_without_title(self):
        """test posting with an empty body"""
        data = {
            # "title": "foobar title",
            "body": "foobar body",
            "project_identifier": 2048,
            "project_manager_key": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        }

        headers = self.get_user_auth_header(data["project_manager_key"])
        result = self.client.post(
            self.url, json.dumps(data), headers=headers, content_type=self.content_type
        )

        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data, messages.invalid_query)

    def test_post_warning_message_without_body(self):
        """test posting with an empty body"""
        data = {
            "title": "foobar title",
            # "body": foobar body,
            "project_identifier": 2048,
            "project_manager_key": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        }

        headers = self.get_user_auth_header(data["project_manager_key"])
        result = self.client.post(
            self.url, json.dumps(data), headers=headers, content_type=self.content_type
        )

        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data, messages.invalid_query)

    def test_post_warning_message_invalid_body(self):
        """Test invalid warning body"""
        data = {
            "title": "foobar title",
            "body": None,
            "project_id": 1,
            "project_manager_key": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        }

        headers = self.get_user_auth_header(data["project_manager_key"])
        result = self.client.post(
            self.url, json.dumps(data), headers=headers, content_type=self.content_type
        )

        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data, messages.invalid_query)

    def test_post_unauthorized(self):
        """test unauthorized posting"""
        data = {}

        result = self.client.post(
            self.url, json.dumps(data), content_type=self.content_type
        )

        self.assertEqual(result.status_code, 403)
        self.assertEqual(result.reason_phrase, "Forbidden")

    def test_get_warning_message_success(self):
        """Tet get warning message"""
        data = {
            "title": "foobar title",
            "body": "foobar body",
            "project_foreign_id": 2048,
            "project_manager_key": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        }
        new_message = self.create_message_from_data(data)

        headers = self.get_device_auth_header()
        result = self.client.get(f"{self.url}?id={new_message.pk}", headers=headers)
        self.assertEqual(result.status_code, 200)

        target_dt = datetime.fromisoformat(result.data["publication_date"])

        expected_result = {
            "id": new_message.pk,
            "images": [],
            "title": "foobar title",
            "body": "foobar body",
            "publication_date": translate_timezone(
                str(new_message.publication_date), target_dt.tzinfo
            ),
            "modification_date": translate_timezone(
                str(new_message.modification_date), target_dt.tzinfo
            ),
            "author_email": "mock0@amsterdam.nl",
        }
        self.assertDictEqual(result.data, expected_result)

    def test_get_warning_message_inactive_project(self):
        """Tet get warning message"""
        data = {
            "title": "foobar title",
            "body": "foobar body",
            "project_foreign_id": 2048,
            "project_manager_key": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        }

        new_message = self.create_message_from_data(data)

        # Deactivate the project
        project_obj = Project.objects.filter(foreign_id=2048).first()
        project_obj.deactivate()

        headers = self.get_device_auth_header()
        result = self.client.get(f"{self.url}?id={new_message.pk}", headers=headers)
        self.assertEqual(result.status_code, 404)
        self.assertEqual(result.data, messages.no_record_found)

    def test_get_warning_message_no_identifier(self):
        """Test get waring message without identifier"""
        headers = self.get_device_auth_header()
        result = self.client.get(f"{self.url}", headers=headers)
        self.assertEqual(result.status_code, 400)

    def test_get_warning_message_invalid_id(self):
        """Test get warning message with invalid identifier"""
        headers = self.get_device_auth_header()
        result = self.client.get(f"{self.url}?id=9999", headers=headers)
        self.assertEqual(result.status_code, 404)
        self.assertEqual(result.data, messages.no_record_found)

    def test_get_warning_message_project_id_does_not_exist(self):
        """Test get warning message but identifier does not exist"""
        headers = self.get_device_auth_header()
        result = self.client.get(f"{self.url}?id=1111111111", headers=headers)

        self.assertEqual(result.status_code, 404)
        self.assertEqual(result.data, messages.no_record_found)

    def test_post_warning_message_image_upload(self):
        """Test uploading image for warning message"""
        project_obj = Project.objects.filter(foreign_id=2048).first()
        data = {
            "title": "foobar title",
            "body": "foobar body",
            "project_foreign_id": project_obj.foreign_id,
            "project_manager_key": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        }
        warning_message = self.create_message_from_data(data)

        path = "{cwd}/construction_work/unit_tests/image_data/portrait.jpg".format(
            cwd=os.getcwd()
        )
        base64_image_data = base64.b64encode(self.read_file(path)).decode("utf-8")

        image_data = {
            "image": {
                "main": "true",
                "data": base64_image_data,
                "description": "unittest",
            },
            "warning_id": warning_message.pk,
        }

        headers = self.get_user_auth_header(data["project_manager_key"])
        result = self.client.post(
            f"{self.url}/image",
            json.dumps(image_data),
            headers=headers,
            content_type=self.content_type,
        )

        self.assertEqual(result.status_code, 200)
        # self.assertDictEqual(result.data, {"status": True, "result": "Images stored in database"})

        project_obj = Project.objects.filter(foreign_id=2048).first()
        warning_message = WarningMessage.objects.filter(project=project_obj.pk).first()
        self.assertEqual(len(warning_message.warningimage_set.all()), 1)

        warning_message_serializer = WarningMessagePublicSerializer(
            instance=warning_message, context={"base_url": "http://mock/"}
        )

        warning_image = warning_message_serializer.data.get("images")[0]
        sources = warning_image.get("sources")
        self.assertEqual(len(sources), 5)

        expected_result = [
            {"url": "http://mock/image?id=1", "width": 135, "height": 180},
            {"url": "http://mock/image?id=2", "width": 324, "height": 432},
            {"url": "http://mock/image?id=3", "width": 540, "height": 720},
            {"url": "http://mock/image?id=4", "width": 810, "height": 1080},
            {"url": "http://mock/image?id=5", "width": 3024, "height": 4032},
        ]

        for i, source in enumerate(sources):
            self.assertEqual(expected_result[i]["width"], dict(source)["width"])
            self.assertEqual(expected_result[i]["height"], dict(source)["height"])

    def test_post_warning_message_unsupported_image_upload(self):
        """test uploading an unsupported image format"""
        data = {
            "title": "title",
            "body": "Body text",
            "project_foreign_id": 2048,
            "project_manager_key": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        }
        warning_message = self.create_message_from_data(data)

        base64_image_data = base64.b64encode(b"0xff").decode("utf-8")

        image_data = {
            "image": {
                "main": "true",
                "data": base64_image_data,
                "description": "unittest",
            },
            "warning_id": warning_message.pk,
        }

        headers = self.get_user_auth_header(data["project_manager_key"])
        result = self.client.post(
            "{url}/image".format(url=self.url),
            json.dumps(image_data),
            headers=headers,
            content_type=self.content_type,
        )

        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data, messages.unsupported_image_format)

        warning_message = WarningMessage.objects.filter(
            project__foreign_id=2048
        ).first()
        self.assertEqual(len(warning_message.warningimage_set.all()), 0)

    def test_post_warning_message_image_upload_no_data(self):
        """test uploading an image without any data"""
        data = {
            "title": "title",
            "body": "Body text",
            "project_foreign_id": 2048,
            "project_manager_key": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        }

        warning_message = self.create_message_from_data(data)

        image_data = {
            "image": {"main": "true"},
            "project_warning_id": warning_message.pk,
        }

        headers = self.get_user_auth_header(data["project_manager_key"])
        result = self.client.post(
            "{url}/image".format(url=self.url),
            json.dumps(image_data),
            headers=headers,
            content_type=self.content_type,
        )

        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data, messages.invalid_query)

    def test_post_warning_message_image_upload_no_main(self):
        """test posting an image upload without 'main''"""
        data = {
            "title": "title",
            "body": "Body text",
            "project_foreign_id": 2048,
            "project_manager_key": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        }
        warning_message = self.create_message_from_data(data)

        image_data = {
            "image": {
                "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg=="  # pylint: disable=line-too-long
            },
            "project_warning_id": warning_message.pk,
        }

        headers = self.get_user_auth_header(data["project_manager_key"])
        result = self.client.post(
            "{url}/image".format(url=self.url),
            json.dumps(image_data),
            headers=headers,
            content_type=self.content_type,
        )

        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data, messages.invalid_query)

    def test_post_warning_message_image_upload_no_warning_message(self):
        """test uploading warning image without a warning message"""
        image_data = {
            "image": {
                "main": "true",
                "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg==",  # pylint: disable=line-too-long
            },
            "warning_id": 4096,
        }

        project_manager_key = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
        headers = self.get_user_auth_header(project_manager_key)
        result = self.client.post(
            "{url}/image".format(url=self.url),
            json.dumps(image_data),
            headers=headers,
            content_type=self.content_type,
        )

        self.assertEqual(result.status_code, 404)
        self.assertEqual(result.data, messages.no_record_found)

    def test_post_warning_message_image_project_warning_id_should_not_be_string(self):
        """test warning_id should not be a string but an integer"""
        image_data = {
            "image": {"main": "true", "data": ""},
            "project_warning_id": "1",
        }

        project_manager_key = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
        headers = self.get_user_auth_header(project_manager_key)
        result = self.client.post(
            "{url}/image".format(url=self.url),
            json.dumps(image_data),
            headers=headers,
            content_type=self.content_type,
        )

        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data, messages.invalid_query)

    def test_post_warning_message_image_upload_no_image_and_project_warning_id(self):
        """test posting a warning message without image and project id"""
        image_data = {}

        project_manager_key = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
        headers = self.get_user_auth_header(project_manager_key)
        result = self.client.post(
            "{url}/image".format(url=self.url),
            json.dumps(image_data),
            headers=headers,
            content_type=self.content_type,
        )

        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data, messages.invalid_query)

    def test_patch_warning_message_valid(self):
        """test patching a warning message"""
        data = {
            "title": "title",
            "body": "body text",
            "project_foreign_id": 2048,
            "project_manager_key": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        }
        warning_message = self.create_message_from_data(data)

        patch_data = {
            "title": "new title",
            "body": "new body text",
            "id": warning_message.pk,
        }

        headers = self.get_jwt_auth_header()
        result = self.client.patch(
            self.url,
            json.dumps(patch_data),
            headers=headers,
            content_type=self.content_type,
        )
        warning_message.refresh_from_db()

        target_dt = datetime.fromisoformat(result.data["publication_date"])

        expected_result = {
            "id": warning_message.pk,
            "title": "new title",
            "body": "new body text",
            "publication_date": translate_timezone(
                str(warning_message.publication_date), target_dt.tzinfo
            ),
            "modification_date": translate_timezone(
                str(warning_message.modification_date), target_dt.tzinfo
            ),
            "author_email": "mock0@amsterdam.nl",
            "project": warning_message.project.pk,
            "project_manager": warning_message.project_manager.pk,
        }

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, expected_result)

    def test_patch_non_existing_warning_message(self):
        """test patching a warning message"""
        patch_data = {
            "title": "new title",
            "body": "new body text",
            "id": 666,
        }
        headers = self.get_jwt_auth_header()
        result = self.client.patch(
            self.url,
            json.dumps(patch_data),
            headers=headers,
            content_type=self.content_type,
        )

        self.assertEqual(result.status_code, 404)
        self.assertEqual(result.data, messages.no_record_found)

    def test_patch_warning_message_missing_title(self):
        """test pathing a missing title in warning message"""
        data = {
            "title": "title",
            "body": "Body text",
            "project_foreign_id": 2048,
            "project_manager_key": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        }
        warning_message = self.create_message_from_data(data)

        patch_data = {"body": "New body text", "identifier": warning_message.pk}

        headers = self.get_jwt_auth_header()
        result = self.client.patch(
            self.url,
            json.dumps(patch_data),
            headers=headers,
            content_type=self.content_type,
        )
        warning_message.refresh_from_db()

        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data, messages.invalid_query)
        self.assertEqual(warning_message.body, data["body"])
        self.assertEqual(warning_message.title, data["title"])

    def test_patch_warning_message_missing_content(self):
        """test pathing a warning message with missing content"""
        data = {
            "title": "title",
            "body": "Body text",
            "project_foreign_id": 2048,
            "project_manager_key": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        }
        warning_message = self.create_message_from_data(data)

        patch_data = {"title": "new title", "identifier": warning_message.pk}

        headers = self.get_jwt_auth_header()
        result = self.client.patch(
            self.url,
            json.dumps(patch_data),
            headers=headers,
            content_type=self.content_type,
        )
        warning_message.refresh_from_db()

        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data, messages.invalid_query)
        self.assertEqual(warning_message.body, data["body"])
        self.assertEqual(warning_message.title, data["title"])

    def test_patch_warning_message_missing_message(self):
        """test pathing a warning message with missing body"""

        patch_data = {"title": "new title", "body": "", "id": 1}

        headers = self.get_jwt_auth_header()
        result = self.client.patch(
            self.url,
            json.dumps(patch_data),
            headers=headers,
            content_type=self.content_type,
        )

        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data, messages.invalid_query)

    def test_patch_warning_message_unauthorized(self):
        """test pathing without authorization"""
        result = self.client.patch(self.url, content_type=self.content_type)

        self.assertEqual(result.status_code, 403)
        self.assertEqual(result.reason_phrase, "Forbidden")

    def test_delete_warning_message(self):
        """test deleting a warning message"""
        data = {
            "title": "title",
            "body": "Body text",
            "project_foreign_id": 2048,
            "project_manager_key": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        }
        warning_message = self.create_message_from_data(data)

        headers = self.get_jwt_auth_header()
        result = self.client.delete(
            "{url}?id={id}".format(url=self.url, id=warning_message.pk),
            headers=headers,
            content_type=self.content_type,
        )

        patched_warning_message = WarningMessage.objects.filter(
            pk=warning_message.pk
        ).first()

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, "Message deleted")
        self.assertEqual(patched_warning_message, None)

    def test_delete_warning_message_missing_identifier(self):
        """test deleting a warning message with missing identifier"""
        headers = self.get_jwt_auth_header()
        result = self.client.delete(
            self.url, headers=headers, content_type=self.content_type
        )

        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data, messages.invalid_query)

    def test_delete_warning_message_unauthorized(self):
        """test deleting a warning message without authorization"""
        result = self.client.delete(
            "{url}?id={id}".format(url=self.url, id=str(uuid.uuid4())),
            content_type=self.content_type,
        )

        self.assertEqual(result.status_code, 403)
        self.assertEqual(result.reason_phrase, "Forbidden")

    def test_project_warnings_valid(self):
        data = [
            {
                "title": "title",
                "body": "Body text",
                "project_foreign_id": 2048,
                "project_manager_key": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            },
            {
                "title": "title",
                "body": "Body text",
                "project_foreign_id": 4096,
                "project_manager_key": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            },
        ]
        [self.create_message_from_data(x) for x in data]

        headers = self.get_device_auth_header()
        result = self.client.get(
            "{url}".format(url=self.url_warnings_get),
            headers=headers,
            content_type=self.content_type,
        )

        self.assertEqual(len(result.data), 2)

    def test_project_warnings_invalid_project_id(self):
        headers = self.get_device_auth_header()
        result = self.client.get(
            "{url}?project_id=999".format(url=self.url_warnings_get),
            headers=headers,
            content_type=self.content_type,
        )

        self.assertEqual(result.status_code, 404)
        self.assertEqual(result.data, messages.no_record_found)

    def test_project_warnings_with_project_id(self):
        project_obj = Project.objects.filter(foreign_id=2048).first()
        data = {
            "title": "title",
            "body": "Body text",
            "project_foreign_id": project_obj.foreign_id,
            "project_manager_key": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        }
        warning_message = self.create_message_from_data(data)

        headers = self.get_device_auth_header()
        result = self.client.get(
            f"{self.url_warnings_get}?project_id={project_obj.pk}",
            headers=headers,
            content_type=self.content_type,
        )

        result_data = result.json()

        target_dt = datetime.fromisoformat(result_data[0]["publication_date"])
        expected_value = {
            "id": warning_message.id,
            "images": [],
            "title": "title",
            "body": "Body text",
            "publication_date": translate_timezone(
                str(warning_message.publication_date), target_dt.tzinfo
            ),
            "modification_date": translate_timezone(
                str(warning_message.modification_date), target_dt.tzinfo
            ),
            "author_email": "mock0@amsterdam.nl",
        }

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(expected_value, result_data[0])
