""" unit_tests """

import base64
import json
import os
import uuid

from django.test import Client, TestCase

from construction_work.api_messages import Messages
from construction_work.generic_functions.aes_cipher import AESCipher
from construction_work.models import Image, Project, ProjectManager, WarningMessage, project
from construction_work.serializers import WarningMessagePublicSerializer, WarningMessageSerializer
from construction_work.unit_tests.mock_data import TestData

messages = Messages()


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
        self.url = "/api/v1/project/warning"
        self.url_warnings_get = "/api/v1/project/warnings"
        app_token = os.getenv("APP_TOKEN")
        aes_secret = os.getenv("AES_SECRET")
        self.token = AESCipher(app_token, aes_secret).encrypt()
        self.headers = {"UserAuthorization": self.token}
        self.content_type = "application/json"
        self.client = Client()

        for project in self.data.projects:
            Project.objects.create(**project)

        for project_manager in self.data.project_manager:
            ProjectManager.objects.create(**project_manager)

    def tearDown(self):
        WarningMessage.objects.all().delete()
        Project.objects.all().delete()
        ProjectManager.objects.all().delete()

    def create_message_from_data(self, data, project_active=True) -> WarningMessage:
        project = Project.objects.get(project_id=data.get("project_identifier"))
        project.active = project_active
        project.save()

        project_manager = ProjectManager.objects.get(pk=data.get("project_manager_id"))

        new_message = WarningMessage(
            title=data.get("title"),
            body=data.get("body"),
            project=project,
            project_manager=project_manager,
        )
        new_message.save()
        return new_message

    def test_post_warning_message_valid(self):
        """Test posting valid warning message"""
        data = {
            "title": "foobar title",
            "body": "foobar body",
            "project_identifier": "0000000000",
            "project_manager_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)
        self.assertEqual(result.status_code, 200)

        warning_message = WarningMessage.objects.filter(project__project_id="0000000000").first()
        self.assertEqual(result.data.get("id"), warning_message.id)

    def test_post_warning_message_invalid_project_id(self):
        """Test add message for unknown project"""
        data = {
            "title": "foobar title",
            "body": "foobar body",
            "project_identifier": "foobar",
            "project_manager_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 404)
        self.assertDictEqual(result.data, {"status": False, "result": messages.no_record_found})

    def test_post_warning_message_invalid_project_manager(self):
        """test posting from a non-existing project manager"""
        data = {
            "title": "foobar title",
            "body": "foobar body",
            "project_identifier": "0000000000",
            "project_manager_id": str(uuid.uuid4()),
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 404)
        self.assertDictEqual(result.data, {"status": False, "result": messages.no_record_found})

    def test_post_warning_message_without_title(self):
        """test posting with an empty body"""
        data = {
            # "title": "foobar title",
            "body": "foobar body",
            "project_identifier": "0000000000",
            "project_manager_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 400)
        self.assertDictEqual(result.data, {"status": False, "result": messages.invalid_query})

    def test_post_warning_message_without_body(self):
        """test posting with an empty body"""
        data = {
            "title": "foobar title",
            # "body": foobar body,
            "project_identifier": "0000000000",
            "project_manager_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 400)
        self.assertDictEqual(result.data, {"status": False, "result": messages.invalid_query})

    def test_post_unauthorized(self):
        """test unauthorized posting"""
        data = {}

        result = self.client.post(self.url, json.dumps(data), content_type=self.content_type)

        self.assertEqual(result.status_code, 403)
        self.assertEqual(result.reason_phrase, "Forbidden")

    def test_get_warning_message_success(self):
        """Tet get warning message"""
        data = {
            "title": "foobar title",
            "body": "foobar body",
            "project_identifier": "0000000000",
            "project_manager_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        }
        new_message = self.create_message_from_data(data)

        result = self.client.get(f"{self.url}?id={new_message.pk}")
        self.assertEqual(result.status_code, 200)

        expected_result = {
            "id": new_message.pk,
            "title": "foobar title",
            "body": "foobar body",
            "project": "0000000000",
            "images": [],
            "publication_date": str(new_message.publication_date).replace(" ", "T"),
            "modification_date": str(new_message.modification_date).replace(" ", "T"),
            "author_email": "mock0@amsterdam.nl",
        }
        self.assertDictEqual(result.data, expected_result)

    def test_get_warning_message_inactive_project(self):
        """Tet get warning message"""
        data = {
            "title": "foobar title",
            "body": "foobar body",
            "project_identifier": "0000000000",
            "project_manager_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        }
        new_message = self.create_message_from_data(data, project_active=False)

        result = self.client.get(f"{self.url}?id={new_message.pk}")
        self.assertEqual(result.status_code, 404)

    def test_get_warning_message_no_identifier(self):
        """Test get waring message without identifier"""
        result = self.client.get(f"{self.url}")
        self.assertEqual(result.status_code, 400)

    def test_get_warning_message_invalid_id(self):
        """Test get warning message with invalid identifier"""
        result = self.client.get(f"{self.url}?id=9999")
        self.assertEqual(result.status_code, 404)
        self.assertDictEqual(result.data, {"status": False, "result": "No record found"})

    def test_get_warning_message_project_id_does_not_exist(self):
        """Test get warning message but identifier does not exist"""
        result = self.client.get(f"{self.url}?id=1111111111")

        self.assertEqual(result.status_code, 404)
        self.assertDictEqual(result.data, {"status": False, "result": messages.no_record_found})

    def test_post_warning_message_image_upload(self):
        """Test uploading image for warning message"""
        data = {
            "title": "foobar title",
            "body": "foobar body",
            "project_identifier": "0000000000",
            "project_manager_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        }
        warning_message = self.create_message_from_data(data)

        path = "{cwd}/construction_work/unit_tests/image_data/portrait.jpg".format(cwd=os.getcwd())
        base64_image_data = base64.b64encode(self.read_file(path)).decode("utf-8")

        image_data = {
            "image": {"main": "true", "data": base64_image_data, "description": "unittest"},
            "project_warning_id": warning_message.pk,
        }

        result = self.client.post(
            "{url}/image".format(url=self.url),
            json.dumps(image_data),
            headers=self.headers,
            content_type=self.content_type,
        )

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {"status": True, "result": "Images stored in database"})

        warning_message = WarningMessage.objects.filter(project__project_id="0000000000").first()
        self.assertEqual(len(warning_message.warningimage_set.all()), 1)

        warning_message_serializer = WarningMessagePublicSerializer(instance=warning_message)

        warning_image = warning_message_serializer.data.get("images")[0]
        sources = warning_image.get("sources")
        self.assertEqual(len(sources), 5)
        for source in sources:
            image = Image.objects.filter(pk=source["image_id"]).first()
            self.assertEqual(image.description, warning_image["description"])
            self.assertEqual(image.aspect_ratio, warning_image["aspect_ratio"])
            self.assertEqual(image.coordinates, warning_image["coordinates"])

            self.assertEqual(image.width, source["width"])
            self.assertEqual(image.height, source["height"])
            self.assertEqual(image.mime_type, source["mime_type"])

    def test_post_warning_message_unsupported_image_upload(self):
        """test uploading an unsupported image format"""
        data = {
            "title": "title",
            "project_identifier": "0000000000",
            "project_manager_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "body": "Body text",
        }
        warning_message = self.create_message_from_data(data)

        base64_image_data = base64.b64encode(b"0xff").decode("utf-8")

        image_data = {
            "image": {"main": "true", "data": base64_image_data, "description": "unittest"},
            "project_warning_id": warning_message.pk,
        }

        result = self.client.post(
            "{url}/image".format(url=self.url),
            json.dumps(image_data),
            headers=self.headers,
            content_type=self.content_type,
        )

        self.assertEqual(result.status_code, 400)
        self.assertDictEqual(result.data, {"status": False, "result": messages.unsupported_image_format})

        warning_message = WarningMessage.objects.filter(project__project_id="0000000000").first()
        self.assertEqual(len(warning_message.warningimage_set.all()), 0)

    def test_post_warning_message_image_upload_no_data(self):
        """test uploading an image without any data"""
        data = {
            "title": "title",
            "project_identifier": "0000000000",
            "project_manager_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "body": "Body text",
        }

        warning_message = self.create_message_from_data(data)

        image_data = {"image": {"main": "true"}, "project_warning_id": warning_message.pk}

        result = self.client.post(
            "{url}/image".format(url=self.url),
            json.dumps(image_data),
            headers=self.headers,
            content_type=self.content_type,
        )

        self.assertEqual(result.status_code, 400)
        self.assertDictEqual(result.data, {"status": False, "result": messages.invalid_query})

    def test_post_warning_message_image_upload_no_main(self):
        """test posting an image upload without 'main''"""
        data = {
            "title": "title",
            "project_identifier": "0000000000",
            "project_manager_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "body": "Body text",
        }
        warning_message = self.create_message_from_data(data)

        image_data = {
            "image": {
                "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg=="  # pylint: disable=line-too-long
            },
            "project_warning_id": warning_message.pk,
        }

        result = self.client.post(
            "{url}/image".format(url=self.url),
            json.dumps(image_data),
            headers=self.headers,
            content_type=self.content_type,
        )

        self.assertEqual(result.status_code, 400)
        self.assertDictEqual(result.data, {"status": False, "result": messages.invalid_query})

    def test_post_warning_message_image_upload_no_warning_message(self):
        """test uploading warning image without a warning message"""
        image_data = {
            "image": {
                "main": "true",
                "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg==",  # pylint: disable=line-too-long
            },
            "project_warning_id": 4096,
        }

        result = self.client.post(
            "{url}/image".format(url=self.url),
            json.dumps(image_data),
            headers=self.headers,
            content_type=self.content_type,
        )

        self.assertEqual(result.status_code, 404)
        self.assertDictEqual(result.data, {"status": False, "result": messages.no_record_found})

    def test_post_warning_message_image_project_warning_id_should_not_be_string(self):
        """test warning_id should not be a string but an integer"""
        image_data = {
            "image": {"main": "true", "data": ""},
            "project_warning_id": "1",
        }

        result = self.client.post(
            "{url}/image".format(url=self.url),
            json.dumps(image_data),
            headers=self.headers,
            content_type=self.content_type,
        )

        self.assertEqual(result.status_code, 400)
        self.assertDictEqual(result.data, {"status": False, "result": messages.invalid_query})

    def test_post_warning_message_image_upload_no_image_and_project_warning_id(self):
        """test posting a warning message without image and project id"""
        image_data = {}
        result = self.client.post(
            "{url}/image".format(url=self.url),
            json.dumps(image_data),
            headers=self.headers,
            content_type=self.content_type,
        )

        self.assertEqual(result.status_code, 400)
        self.assertDictEqual(result.data, {"status": False, "result": messages.invalid_query})

    def test_patch_warning_message_valid(self):
        """test patching a warning message"""
        data = {
            "title": "title",
            "project_identifier": "0000000000",
            "project_manager_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "body": "body text",
        }
        warning_message = self.create_message_from_data(data)

        patch_data = {
            "title": "new title",
            "body": "new body text",
            "identifier": warning_message.pk,
        }

        result = self.client.patch(
            self.url, json.dumps(patch_data), headers=self.headers, content_type=self.content_type
        )
        warning_message.refresh_from_db()

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {"status": True, "result": "Message patched"})
        self.assertEqual(warning_message.body, patch_data["body"])
        self.assertEqual(warning_message.title, patch_data["title"])

    def test_patch_warning_message_missing_title(self):
        """test pathing a missing title in warning message"""
        data = {
            "title": "title",
            "project_identifier": "0000000000",
            "project_manager_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "body": "Body text",
        }
        warning_message = self.create_message_from_data(data)

        patch_data = {"body": "New body text", "identifier": warning_message.pk}

        result = self.client.patch(
            self.url, json.dumps(patch_data), headers=self.headers, content_type=self.content_type
        )
        warning_message.refresh_from_db()

        self.assertEqual(result.status_code, 400)
        self.assertDictEqual(result.data, {"status": False, "result": messages.invalid_query})
        self.assertEqual(warning_message.body, data["body"])
        self.assertEqual(warning_message.title, data["title"])

    def test_patch_warning_message_missing_content(self):
        """test pathing a warning message with missing content"""
        data = {
            "title": "title",
            "project_identifier": "0000000000",
            "project_manager_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "body": "Body text",
        }
        warning_message = self.create_message_from_data(data)

        patch_data = {"title": "new title", "identifier": warning_message.pk}

        result = self.client.patch(
            self.url, json.dumps(patch_data), headers=self.headers, content_type=self.content_type
        )
        warning_message.refresh_from_db()

        self.assertEqual(result.status_code, 400)
        self.assertDictEqual(result.data, {"status": False, "result": messages.invalid_query})
        self.assertEqual(warning_message.body, data["body"])
        self.assertEqual(warning_message.title, data["title"])

    def test_patch_warning_message_missing_message(self):
        """test pathing a warning message with missing message"""
        patch_data = {"title": "new title", "body": "", "identifier": 4096}

        result = self.client.patch(
            self.url, json.dumps(patch_data), headers=self.headers, content_type=self.content_type
        )

        self.assertEqual(result.status_code, 404)
        self.assertDictEqual(result.data, {"status": False, "result": messages.no_record_found})

    def test_patch_warning_message_unauthorized(self):
        """test pathing without authorization"""
        result = self.client.patch(self.url, content_type=self.content_type)

        self.assertEqual(result.status_code, 403)
        self.assertEqual(result.reason_phrase, "Forbidden")

    def test_delete_warning_message(self):
        """test deleting a warning message"""
        data = {
            "title": "title",
            "project_identifier": "0000000000",
            "project_manager_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "body": "Body text",
        }
        warning_message = self.create_message_from_data(data)

        result = self.client.delete(
            "{url}?id={identifier}".format(url=self.url, identifier=warning_message.pk),
            headers=self.headers,
            content_type=self.content_type,
        )

        patched_warning_message = WarningMessage.objects.filter(pk=warning_message.pk).first()

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {"status": False, "result": "Message deleted"})
        self.assertEqual(patched_warning_message, None)

    def test_delete_warning_message_missing_identifier(self):
        """test deleting a warning message with missing identifier"""
        result = self.client.delete(self.url, headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 400)
        self.assertDictEqual(result.data, {"status": False, "result": messages.invalid_query})

    def test_delete_warning_message_unauthorized(self):
        """test deleting a warning message without authorization"""
        result = self.client.delete(
            "{url}?id={identifier}".format(url=self.url, identifier=str(uuid.uuid4())), content_type=self.content_type
        )

        self.assertEqual(result.status_code, 403)
        self.assertEqual(result.reason_phrase, "Forbidden")
