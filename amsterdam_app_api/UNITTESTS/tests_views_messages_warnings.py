import json
import uuid
from django.test import Client
from django.test import TestCase
from amsterdam_app_api.UNITTESTS.mock_data import TestData
from amsterdam_app_api.GenericFunctions.AESCipher import AESCipher
from amsterdam_app_api.models import Projects, ProjectManager, WarningMessages, Image
from amsterdam_app_api.api_messages import Messages

messages = Messages()


class TestApiProjectWarning(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestApiProjectWarning, self).__init__(*args, **kwargs)
        self.data = TestData()
        self.url = '/api/v1/project/warning'
        self.url_warnings_get = '/api/v1/project/warnings'
        self.token = AESCipher('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '6886b31dfe27e9306c3d2b553345d9e5').encrypt()
        self.headers = {"UserAuthorization": self.token}
        self.content_type = "application/json"
        self.client = Client()

    def setUp(self):
        WarningMessages.objects.all().delete()

        Projects.objects.all().delete()
        for project in self.data.projects:
            Projects.objects.create(**project)

        ProjectManager.objects.all().delete()
        for project_manager in self.data.project_manager:
            ProjectManager.objects.create(**project_manager)

    def test_post_warning_message_valid(self):
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': {'preface': 'short text', 'content': 'long text'}
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        warning_message = WarningMessages.objects.filter(project_identifier='0000000000').first()

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': True, 'result': {'warning_identifier': str(warning_message.identifier)}})

    def test_post_warning_message_invalid_project(self):
        data = {
            'title': 'title',
            'project_identifier': '0000000001',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': {'preface': 'short text', 'content': 'long text'}
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 404)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.no_record_found})

    def test_post_warning_message_project_manager_does_not_exist(self):
        data = {
            'title': 'title',
            'project_identifier': '0000000001',
            'project_manager_id': str(uuid.uuid4()),
            'body': {'preface': 'short text', 'content': 'long text'}
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 404)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.no_record_found})

    def test_post_warning_message_project_does_not_exist(self):
        data = {
            'title': 'title',
            'project_identifier': 'AAAAAAAAAA',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': {'preface': 'short text', 'content': 'long text'}
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.invalid_query})

    def test_post_warning_message_body_content_empty(self):
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': {'preface': 'short text'}
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.invalid_query})

    def test_post_warning_message_body_preface_empty(self):
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': {'content': 'long text'}
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.invalid_query})

    def test_post_warning_message_missing_items(self):
        data = {'body': {'content': 'long text'}}

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.invalid_query})

    def test_post_unauthorized(self):
        data = {'body': {'content': 'long text'}}

        result = self.client.post(self.url, json.dumps(data), content_type=self.content_type)

        self.assertEqual(result.status_code, 403)
        self.assertEqual(result.reason_phrase, 'Forbidden')


    def test_get_warning_message(self):
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': {'preface': 'short text', 'content': 'long text'}
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        warning_message = WarningMessages.objects.filter(project_identifier='0000000000').first()

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': True, 'result': {'warning_identifier': str(warning_message.identifier)}})

        result = self.client.get('{url}?id={identifier}'.format(url=self.url, identifier=warning_message.identifier))
        data = result.data
        data['result']['publication_date'] = data['result']['publication_date'].replace('T', ' ')
        data['result']['modification_date'] = data['result']['modification_date'].replace('T', ' ')

        expected_result = {
            "status": True,
            "result": {
                "identifier": str(warning_message.identifier),
                "title": "title",
                "body": {"content": "long text", "preface": "short text"},
                "project_identifier":"0000000000",
                "images":[],
                "publication_date": str(warning_message.publication_date),
                "modification_date": str(warning_message.modification_date),
                "author_email":"mock0@amsterdam.nl"
            }
        }
        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(data, expected_result)

    def test_get_warning_message_inactive_project(self):
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': {'preface': 'short text', 'content': 'long text'}
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        warning_message = WarningMessages.objects.filter(project_identifier='0000000000').first()

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': True, 'result': {'warning_identifier': str(warning_message.identifier)}})

        project = Projects.objects.filter(pk='0000000000').first()
        project.active = False
        project.save()

        result = self.client.get('{url}?id={identifier}'.format(url=self.url, identifier=warning_message.identifier))
        data = result.data

        self.assertEqual(result.status_code, 404)
        self.assertDictEqual(data, {'status': False, 'result': messages.no_record_found})


    def test_get_warning_message_no_identifier(self):
        result = self.client.get('{url}'.format(url=self.url))
        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': 'Invalid query parameter(s). See /api/v1/apidocs for more information'})

    def test_get_warning_message_invalid_identifier(self):
        result = self.client.get('{url}?id={uuid}'.format(url=self.url, uuid=str(uuid.uuid4())))
        self.assertEqual(result.status_code, 404)
        self.assertDictEqual(result.data, {'status': False, 'result': 'No record found'})

    def test_get_warning_messages(self):
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': {'preface': 'short text', 'content': 'long text'}
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        warning_message = WarningMessages.objects.filter(project_identifier='0000000000').first()

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': True, 'result': {'warning_identifier': str(warning_message.identifier)}})

        result = self.client.get('{url}?id=0000000000'.format(url=self.url_warnings_get))
        data = result.data
        data['result'][0]['publication_date'] = data['result'][0]['publication_date'].replace('T', ' ')
        data['result'][0]['modification_date'] = data['result'][0]['modification_date'].replace('T', ' ')

        expected_result = {
            "status": True,
            "result": [{
                "identifier": str(warning_message.identifier),
                "title": "title",
                "body": {"content": "long text", "preface": "short text"},
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
        result = self.client.get('{url}?id=1111111111'.format(url=self.url_warnings_get))

        self.assertEqual(result.status_code, 404)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.no_record_found})

    def test_get_warning_messages_no_project_identifier(self):
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': {'preface': 'short text', 'content': 'long text'}
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)
        warning_message = WarningMessages.objects.filter(project_identifier='0000000000').first()

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': True, 'result': {'warning_identifier': str(warning_message.identifier)}})

        result = self.client.get('{url}'.format(url=self.url_warnings_get))
        self.assertEqual(result.status_code, 200)

        result_data = json.loads(result.content.decode('utf-8'))
        self.assertEqual(len(result_data['result']), 1)

    def test_post_warning_message_image_upload(self):
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': {'preface': 'short text', 'content': 'long text'}
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        warning_message = WarningMessages.objects.filter(project_identifier='0000000000').first()

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': True, 'result': {'warning_identifier': str(warning_message.identifier)}})

        image_data = {
            "image": {
                "type": "header",
                "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg=="
            },
            "project_warning_id": str(warning_message.identifier)
        }

        result = self.client.post('{url}/image'.format(url=self.url),
                                  json.dumps(image_data),
                                  headers=self.headers,
                                  content_type=self.content_type)

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': True, 'result': 'Image stored in database'})

        warning_message = WarningMessages.objects.filter(project_identifier='0000000000').first()
        image_identifier = warning_message.images[0]['sources']['1px']['image_id']

        image = Image.objects.filter(pk=image_identifier).first()

        self.assertEqual(image.filename, 'db://amsterdam_app_api.warning_message/{id}'.format(id=image_identifier))
        self.assertEqual(image.url, 'db://amsterdam_app_api.warning_message/{id}'.format(id=image_identifier))
        self.assertEqual(image.mime_type, 'image/png')
        self.assertEqual(image.size, '1px')

    def test_post_warning_message_image_upload_no_data(self):
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': {'preface': 'short text', 'content': 'long text'}
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)
        warning_message = WarningMessages.objects.filter(project_identifier='0000000000').first()

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': True, 'result': {'warning_identifier': str(warning_message.identifier)}})

        image_data = {
            "image": {
                "type": "header"
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
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': {'preface': 'short text', 'content': 'long text'}
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)
        warning_message = WarningMessages.objects.filter(project_identifier='0000000000').first()

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': True, 'result': {'warning_identifier': str(warning_message.identifier)}})

        image_data = {
            "image": {
                "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg=="
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
        image_data = {
            "image": {
                "type": "header",
                "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg=="
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
        image_data = {}
        result = self.client.post('{url}/image'.format(url=self.url),
                                  json.dumps(image_data),
                                  headers=self.headers,
                                  content_type=self.content_type)

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.invalid_query})

    def test_patch_warning_message_valid(self):
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': {'preface': 'short text', 'content': 'long text'}
        }

        self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        warning_message = WarningMessages.objects.filter(project_identifier='0000000000').first()

        patch_data = {
            'title': 'new title',
            'body': {'preface': 'new short text', 'content': 'new long text'},
            'identifier': str(warning_message.identifier)
        }

        result = self.client.patch(self.url, json.dumps(patch_data), headers=self.headers, content_type=self.content_type)
        patched_warning_message = WarningMessages.objects.filter(identifier=warning_message.identifier).first()

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': True, 'result': 'Message patched'})
        self.assertDictEqual(patched_warning_message.body, patch_data['body'])
        self.assertEqual(patched_warning_message.title, patch_data['title'])

    def test_patch_warning_message_missing_title(self):
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': {'preface': 'short text', 'content': 'long text'}
        }

        self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        warning_message = WarningMessages.objects.filter(project_identifier='0000000000').first()

        patch_data = {
            'body': {'preface': 'new short text', 'content': 'new long text'},
            'identifier': str(warning_message.identifier)
        }

        result = self.client.patch(self.url, json.dumps(patch_data), headers=self.headers, content_type=self.content_type)
        patched_warning_message = WarningMessages.objects.filter(identifier=warning_message.identifier).first()

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.invalid_query})
        self.assertDictEqual(patched_warning_message.body, data['body'])
        self.assertEqual(patched_warning_message.title, data['title'])

    def test_patch_warning_message_missing_preface(self):
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': {'preface': 'short text', 'content': 'long text'}
        }

        self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        warning_message = WarningMessages.objects.filter(project_identifier='0000000000').first()

        patch_data = {
            'title': 'new title',
            'body': {'content': 'new long text'},
            'identifier': str(warning_message.identifier)
        }

        result = self.client.patch(self.url, json.dumps(patch_data), headers=self.headers, content_type=self.content_type)
        patched_warning_message = WarningMessages.objects.filter(identifier=warning_message.identifier).first()

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.invalid_query})
        self.assertDictEqual(patched_warning_message.body, data['body'])
        self.assertEqual(patched_warning_message.title, data['title'])

    def test_patch_warning_message_missing_content(self):
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': {'preface': 'short text', 'content': 'long text'}
        }

        self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        warning_message = WarningMessages.objects.filter(project_identifier='0000000000').first()

        patch_data = {
            'title': 'new title',
            'body': {'preface': 'short text'},
            'identifier': str(warning_message.identifier)
        }

        result = self.client.patch(self.url, json.dumps(patch_data), headers=self.headers, content_type=self.content_type)
        patched_warning_message = WarningMessages.objects.filter(identifier=warning_message.identifier).first()

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.invalid_query})
        self.assertDictEqual(patched_warning_message.body, data['body'])
        self.assertEqual(patched_warning_message.title, data['title'])

    def test_patch_warning_message_missing_message(self):
        patch_data = {
            'title': 'new title',
            'body': {'preface': 'short text', 'content': 'long text'},
            'identifier': str(uuid.uuid4())
        }

        result = self.client.patch(self.url, json.dumps(patch_data), headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 404)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.no_record_found})

    def test_patch_warning_message_unauthorized(self):
        patch_data = {
            'title': 'new title',
            'body': {'preface': 'short text', 'content': 'long text'},
            'identifier': str(uuid.uuid4())
        }

        result = self.client.patch(self.url, json.dumps(patch_data), content_type=self.content_type)

        self.assertEqual(result.status_code, 403)
        self.assertEqual(result.reason_phrase, 'Forbidden')

    def test_delete_warning_message(self):
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': {'preface': 'short text', 'content': 'long text'}
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
        result = self.client.delete(self.url, headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.invalid_query})

    def test_delete_warning_message__unauthorized(self):
        result = self.client.delete('{url}?id={identifier}'.format(url=self.url, identifier=str(uuid.uuid4())),
                                    content_type=self.content_type)

        self.assertEqual(result.status_code, 403)
        self.assertEqual(result.reason_phrase, 'Forbidden')
