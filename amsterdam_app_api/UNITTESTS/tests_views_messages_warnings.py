""" UNITTESTS """

import json
import uuid
import base64
import os
from django.test import Client
from django.test import TestCase
from amsterdam_app_api.UNITTESTS.mock_data import TestData
from amsterdam_app_api.GenericFunctions.AESCipher import AESCipher
from amsterdam_app_api.models import Projects, ProjectManager, WarningMessages, Image
from amsterdam_app_api.api_messages import Messages

messages = Messages()


class TestApiProjectWarning(TestCase):
    """ Test project warnings """
    def __init__(self, *args, **kwargs):
        super(TestApiProjectWarning, self).__init__(*args, **kwargs)
        self.data = TestData()
        self.url = '/api/v1/project/warning'
        self.url_warnings_get = '/api/v1/project/warnings'
        self.token = AESCipher('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', os.getenv('AES_SECRET')).encrypt()
        self.headers = {"UserAuthorization": self.token}
        self.content_type = "application/json"
        self.client = Client()

    @staticmethod
    def read_file(filename):
        """ Read data from file """
        with open(filename, 'rb') as f:
            data = f.read()
        return data

    def setUp(self):
        """ setup test db """
        WarningMessages.objects.all().delete()

        Projects.objects.all().delete()
        for project in self.data.projects:
            Projects.objects.create(**project)

        ProjectManager.objects.all().delete()
        for project_manager in self.data.project_manager:
            ProjectManager.objects.create(**project_manager)

    def test_post_warning_message_valid(self):
        """ test posting valid warning message """
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': 'Body text'
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        warning_message = WarningMessages.objects.filter(project_identifier='0000000000').first()

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': True,
                                           'result': {'warning_identifier': str(warning_message.identifier)}})

    def test_post_warning_message_invalid_project(self):
        """ test posting for invalid project """
        data = {
            'title': 'title',
            'project_identifier': '0000000001',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': 'Body text'
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 404)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.no_record_found})

    def test_post_warning_message_project_manager_does_not_exist(self):
        """ test posting from a non-existing project manager """
        data = {
            'title': 'title',
            'project_identifier': '0000000001',
            'project_manager_id': str(uuid.uuid4()),
            'body': 'Body text'
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 404)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.no_record_found})

    def test_post_warning_message_project_does_not_exist(self):
        """ test posting for a non-existing project """
        data = {
            'title': 'title',
            'project_identifier': 'AAAAAAAAAA',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': 'Body text'
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.invalid_query})

    def test_post_warning_message_body_content_empty(self):
        """ test posting with an empty body """
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': None
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.invalid_query})

    def test_post_warning_message_body_preface_empty(self):
        """ test posting with an empty preface """
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': None
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.invalid_query})

    def test_post_warning_message_missing_items(self):
        """ test posting with missing body items """
        data = {'body': 'Body text'}

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.invalid_query})

    def test_post_unauthorized(self):
        """ test unauthorized posting """
        data = {'body': 'Body text'}

        result = self.client.post(self.url, json.dumps(data), content_type=self.content_type)

        self.assertEqual(result.status_code, 403)
        self.assertEqual(result.reason_phrase, 'Forbidden')

    def test_get_warning_message(self):
        """ test get warning message """
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': 'Body text'
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        warning_message = WarningMessages.objects.filter(project_identifier='0000000000').first()

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': True,
                                           'result': {'warning_identifier': str(warning_message.identifier)}})

        result = self.client.get('{url}?id={identifier}'.format(url=self.url, identifier=warning_message.identifier))
        data = result.data
        data['result']['publication_date'] = data['result']['publication_date'].replace('T', ' ')
        data['result']['modification_date'] = data['result']['modification_date'].replace('T', ' ')

        expected_result = {
            "status": True,
            "result": {
                "identifier": str(warning_message.identifier),
                "title": "title",
                "body": "Body text",
                "project_identifier": "0000000000",
                "images": [],
                "publication_date": str(warning_message.publication_date),
                "modification_date": str(warning_message.modification_date),
                "author_email":"mock0@amsterdam.nl"
            }
        }
        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(data, expected_result)

    def test_get_warning_message_inactive_project(self):
        """ test get warning message for inactive project """
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': 'Body text'
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        warning_message = WarningMessages.objects.filter(project_identifier='0000000000').first()

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': True,
                                           'result': {'warning_identifier': str(warning_message.identifier)}})

        project = Projects.objects.filter(pk='0000000000').first()
        project.active = False
        project.save()

        result = self.client.get('{url}?id={identifier}'.format(url=self.url, identifier=warning_message.identifier))
        data = result.data

        self.assertEqual(result.status_code, 404)
        self.assertDictEqual(data, {'status': False, 'result': messages.no_record_found})

    def test_get_warning_message_no_identifier(self):
        """ test get waring message without identifier """
        result = self.client.get('{url}'.format(url=self.url))
        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data,
                             {'status': False,
                              'result': 'Invalid query parameter(s). See /api/v1/apidocs for more information'})

    def test_get_warning_message_invalid_identifier(self):
        """ test get warning message with invalid identifier """
        result = self.client.get('{url}?id={uuid}'.format(url=self.url, uuid=str(uuid.uuid4())))
        self.assertEqual(result.status_code, 404)
        self.assertDictEqual(result.data, {'status': False, 'result': 'No record found'})

    def test_get_warning_messages(self):
        """ test get warning message """
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': 'Body text'
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        warning_message = WarningMessages.objects.filter(project_identifier='0000000000').first()

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': True,
                                           'result': {'warning_identifier': str(warning_message.identifier)}})

        result = self.client.get('{url}?id=0000000000'.format(url=self.url_warnings_get))
        data = result.data
        data['result'][0]['publication_date'] = data['result'][0]['publication_date'].replace('T', ' ')
        data['result'][0]['modification_date'] = data['result'][0]['modification_date'].replace('T', ' ')

        expected_result = {
            "status": True,
            "result": [{
                "identifier": str(warning_message.identifier),
                "title": "title",
                "body": 'Body text',
                "project_identifier":"0000000000",
                "images":[],
                "publication_date": str(warning_message.publication_date),
                "modification_date": str(warning_message.modification_date),
                "author_email":"mock0@amsterdam.nl"
            }]
        }
        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(data, expected_result)

    def test_get_warning_message_project_identifier_does_not_exist(self):
        """ test get warning message but identifier does not exist """
        result = self.client.get('{url}?id=1111111111'.format(url=self.url_warnings_get))

        self.assertEqual(result.status_code, 404)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.no_record_found})

    def test_get_warning_messages_no_project_identifier(self):
        """ test get warning message but project identifier is missing """
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': 'Body text'
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)
        warning_message = WarningMessages.objects.filter(project_identifier='0000000000').first()

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': True,
                                           'result': {'warning_identifier': str(warning_message.identifier)}})

        result = self.client.get('{url}'.format(url=self.url_warnings_get))
        self.assertEqual(result.status_code, 200)

        result_data = json.loads(result.content.decode('utf-8'))
        self.assertEqual(len(result_data['result']), 1)

    def test_post_warning_message_image_upload(self):
        """ test uploading image for warning message """
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': 'Body text'
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        warning_message = WarningMessages.objects.filter(project_identifier='0000000000').first()

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': True,
                                           'result': {'warning_identifier': str(warning_message.identifier)}})

        path = '{cwd}/amsterdam_app_api/UNITTESTS/image_data/portrait.jpg'.format(cwd=os.getcwd())
        base64_image_data = base64.b64encode(self.read_file(path)).decode('utf-8')

        image_data = {
            "image": {
                "main": "true",
                "data": base64_image_data,
                "description": "unittest"
            },
            "project_warning_id": str(warning_message.identifier)
        }

        result = self.client.post('{url}/image'.format(url=self.url),
                                  json.dumps(image_data),
                                  headers=self.headers,
                                  content_type=self.content_type)

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': True, 'result': 'Images stored in database'})

        warning_message = WarningMessages.objects.filter(project_identifier='0000000000').first()
        self.assertEqual(len(warning_message.images), 1)
        sources = warning_message.images[0]['sources']
        self.assertEqual(len(sources), 5)
        for source in sources:
            image = Image.objects.filter(pk=source['image_id']).first()
            self.assertEqual(image.url, 'db://amsterdam_app_api.warning_message/{id}'.format(id=source['image_id']))
            self.assertEqual(image.mime_type, source['mime_type'])
            self.assertEqual(image.size, '{width}x{height}'.format(width=source['width'], height=source['height']))

    def test_post_warning_message_unsupported_image_upload(self):
        """ test uploading an unsupported image format """
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': 'Body text'
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        warning_message = WarningMessages.objects.filter(project_identifier='0000000000').first()

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': True,
                                           'result': {'warning_identifier': str(warning_message.identifier)}})

        base64_image_data = base64.b64encode(b'0xff').decode('utf-8')

        image_data = {
            "image": {
                "main": "true",
                "data": base64_image_data,
                "description": "unittest"
            },
            "project_warning_id": str(warning_message.identifier)
        }

        result = self.client.post('{url}/image'.format(url=self.url),
                                  json.dumps(image_data),
                                  headers=self.headers,
                                  content_type=self.content_type)

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.unsupported_image_format})

        warning_message = WarningMessages.objects.filter(project_identifier='0000000000').first()
        self.assertEqual(len(warning_message.images), 0)

    def test_post_warning_message_image_upload_no_data(self):
        """ test uploading an image without any data """
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': 'Body text'
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)
        warning_message = WarningMessages.objects.filter(project_identifier='0000000000').first()

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': True,
                                           'result': {'warning_identifier': str(warning_message.identifier)}})

        image_data = {
            "image": {
                "main": "true"
            },
            "project_warning_id": str(warning_message.identifier)
        }

        result = self.client.post('{url}/image'.format(url=self.url),
                                  json.dumps(image_data),
                                  headers=self.headers,
                                  content_type=self.content_type)

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.invalid_query})

    def test_post_warning_message_image_upload_no_type(self):
        """ test posting an image upload without any type """
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': 'Body text'
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)
        warning_message = WarningMessages.objects.filter(project_identifier='0000000000').first()

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': True,
                                           'result': {'warning_identifier': str(warning_message.identifier)}})

        image_data = {
            "image": {
                "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg=="  # pylint: disable=line-too-long
            },
            "project_warning_id": str(warning_message.identifier)
        }

        result = self.client.post('{url}/image'.format(url=self.url),
                                  json.dumps(image_data),
                                  headers=self.headers,
                                  content_type=self.content_type)

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.invalid_query})

    def test_post_warning_message_image_upload_no_warning_message(self):
        """ test uploading warning image without a warning message """
        image_data = {
            "image": {
                "main": "true",
                "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg=="  # pylint: disable=line-too-long
            },
            "project_warning_id": str(uuid.uuid4())
        }

        result = self.client.post('{url}/image'.format(url=self.url),
                                  json.dumps(image_data),
                                  headers=self.headers,
                                  content_type=self.content_type)

        self.assertEqual(result.status_code, 404)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.no_record_found})

    def test_post_warning_message_image_upload_no_image_and_project_warning_id(self):
        """ test posting a warning message without image and project id """
        image_data = {}
        result = self.client.post('{url}/image'.format(url=self.url),
                                  json.dumps(image_data),
                                  headers=self.headers,
                                  content_type=self.content_type)

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.invalid_query})

    def test_patch_warning_message_valid(self):
        """ test patching a warning message """
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': 'Body text'
        }

        self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        warning_message = WarningMessages.objects.filter(project_identifier='0000000000').first()

        patch_data = {
            'title': 'new title',
            'body': 'New body text',
            'identifier': str(warning_message.identifier)
        }

        result = self.client.patch(self.url, json.dumps(patch_data),
                                   headers=self.headers,
                                   content_type=self.content_type)
        patched_warning_message = WarningMessages.objects.filter(identifier=warning_message.identifier).first()

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': True, 'result': 'Message patched'})
        self.assertEqual(patched_warning_message.body, 'New body text')
        self.assertEqual(patched_warning_message.title, patch_data['title'])

    def test_patch_warning_message_missing_title(self):
        """ test pathing a missing title in warning message """
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': 'Body text'
        }

        self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        warning_message = WarningMessages.objects.filter(project_identifier='0000000000').first()

        patch_data = {
            'body': 'New body text',
            'identifier': str(warning_message.identifier)
        }

        result = self.client.patch(self.url,
                                   json.dumps(patch_data),
                                   headers=self.headers,
                                   content_type=self.content_type)
        patched_warning_message = WarningMessages.objects.filter(identifier=warning_message.identifier).first()

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.invalid_query})
        self.assertEqual(patched_warning_message.body, data['body'])
        self.assertEqual(patched_warning_message.title, data['title'])

    def test_patch_warning_message_missing_content(self):
        """ test pathing a warning message with missing content """
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': 'Body text'
        }

        self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        warning_message = WarningMessages.objects.filter(project_identifier='0000000000').first()

        patch_data = {
            'title': 'new title',
            'identifier': str(warning_message.identifier)
        }

        result = self.client.patch(self.url,
                                   json.dumps(patch_data),
                                   headers=self.headers,
                                   content_type=self.content_type)
        patched_warning_message = WarningMessages.objects.filter(identifier=warning_message.identifier).first()

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.invalid_query})
        self.assertEqual(patched_warning_message.body, data['body'])
        self.assertEqual(patched_warning_message.title, data['title'])

    def test_patch_warning_message_missing_message(self):
        """ test pathing a warning message with missing message """
        patch_data = {
            'title': 'new title',
            'body': 'Body text',
            'identifier': str(uuid.uuid4())
        }

        result = self.client.patch(self.url,
                                   json.dumps(patch_data),
                                   headers=self.headers,
                                   content_type=self.content_type)

        self.assertEqual(result.status_code, 404)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.no_record_found})

    def test_patch_warning_message_unauthorized(self):
        """ test pathing without authorization """
        patch_data = {
            'title': 'new title',
            'body': {'preface': 'short text', 'content': 'long text'},
            'identifier': str(uuid.uuid4())
        }

        result = self.client.patch(self.url, json.dumps(patch_data), content_type=self.content_type)

        self.assertEqual(result.status_code, 403)
        self.assertEqual(result.reason_phrase, 'Forbidden')

    def test_delete_warning_message(self):
        """ test deleting a warning message """
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': 'Body text'
        }

        self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        warning_message = WarningMessages.objects.filter(project_identifier='0000000000').first()

        result = self.client.delete('{url}?id={identifier}'.format(url=self.url, identifier=warning_message.identifier),
                                    headers=self.headers,
                                    content_type=self.content_type)

        patched_warning_message = WarningMessages.objects.filter(identifier=warning_message.identifier).first()

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': False, 'result': 'Message deleted'})
        self.assertEqual(patched_warning_message, None)

    def test_delete_warning_message_missing_identifier(self):
        """ test deleting a warning message with missing identifier """
        result = self.client.delete(self.url, headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.invalid_query})

    def test_delete_warning_message_unauthorized(self):
        """ test deleting a warning message without authorization """
        result = self.client.delete('{url}?id={identifier}'.format(url=self.url, identifier=str(uuid.uuid4())),
                                    content_type=self.content_type)

        self.assertEqual(result.status_code, 403)
        self.assertEqual(result.reason_phrase, 'Forbidden')
