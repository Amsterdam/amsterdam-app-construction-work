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
            'project_manager_token': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
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
            'project_manager_token': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': {'preface': 'short text', 'content': 'long text'}
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 404)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.no_record_found})

    def test_post_warning_message_project_manager_does_not_exist(self):
        data = {
            'title': 'title',
            'project_identifier': '0000000001',
            'project_manager_token': str(uuid.uuid4()),
            'body': {'preface': 'short text', 'content': 'long text'}
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 404)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.no_record_found})

    def test_post_warning_message_project_does_not_exist(self):
        data = {
            'title': 'title',
            'project_identifier': 'AAAAAAAAAA',
            'project_manager_token': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': {'preface': 'short text', 'content': 'long text'}
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.invalid_query})

    def test_post_warning_message_body_content_empty(self):
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_token': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': {'preface': 'short text'}
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.invalid_query})

    def test_post_warning_message_body_preface_empty(self):
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_token': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
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
            'project_manager_token': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'body': {'preface': 'short text', 'content': 'long text'}
        }

        result = self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)

        warning_message = WarningMessages.objects.filter(project_identifier='0000000000').first()

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': True, 'result': {'warning_identifier': str(warning_message.identifier)}})

        result = self.client.get('{url}?id=0000000000'.format(url=self.url))
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
        result = self.client.get('{url}?id=1111111111'.format(url=self.url))

        self.assertEqual(result.status_code, 404)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.no_record_found})

    def test_get_warning_message_no_project_identifier(self):
        result = self.client.get('{url}'.format(url=self.url))

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.invalid_query})

    def test_post_warning_message_image_upload(self):
        data = {
            'title': 'title',
            'project_identifier': '0000000000',
            'project_manager_token': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
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
            'project_manager_token': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
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
            'project_manager_token': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
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
