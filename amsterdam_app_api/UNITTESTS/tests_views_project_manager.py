from django.test import Client
from django.test import TestCase
from amsterdam_app_api.models import ProjectManager
from amsterdam_app_api.models import Projects
from amsterdam_app_api.UNITTESTS.mock_data import TestData

from amsterdam_app_api.api_messages import Messages

messages = Messages()


class TestApiProjectManager(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestApiProjectManager, self).__init__(*args, **kwargs)
        self.data = TestData()
        self.url = '/api/v1/project/manager'

    def setUp(self):
        ProjectManager.objects.all().delete()
        for project_manager in self.data.project_manager:
            ProjectManager.objects.create(**project_manager)

        Projects.objects.all().delete()
        for project in self.data.projects:
            Projects.objects.create(**project)

    def test_get_all_project_managers(self):
        c = Client()
        response = c.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, {'status': True, 'result': self.data.project_manager})

    def test_get_single_project_managers(self):
        c = Client()
        response = c.get('{url}?id=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'.format(url=self.url))

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, {'status': True, 'result': [self.data.project_manager[0]]})

    def test_delete_project_manager_no_identifier(self):
        c = Client()
        response = c.delete(self.url)

        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(response.data, {'status': False, 'result': messages.invalid_query})

    def test_delete_project_manager(self):
        c = Client()
        response = c.delete('{url}?id=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'.format(url=self.url))

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, {'status': True, 'result': 'Project manager removed'})

    def test_post_project_manager_valid(self):
        json_data = '{"email": "mock3@amsterdam.nl", "projects": ["0000000000"]}'

        c = Client()
        response = c.post(self.url, json_data, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, {'status': True, 'result': 'Project manager updated'})

    def test_post_project_manager_invalid_email(self):
        json_data = '{"email": "mock@example.com", "projects": ["0000000000"]}'

        c = Client()
        response = c.post(self.url, json_data, content_type="application/json")

        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(response.data,
                             {'status': False, 'result': 'Invalid email, should be <username>@amsterdam.nl'})

    def test_post_project_manager_no_email(self):
        json_data = '{"projects": ["0000000000"]}'

        c = Client()
        response = c.post(self.url, json_data, content_type="application/json")

        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(response.data, {'status': False, 'result': messages.invalid_query})

    def test_post_project_manager_invalid_project(self):
        json_data = '{"email": "mock3@amsterdam.nl", "projects": ["AAAAAAAAAA"]}'

        c = Client()
        response = c.post(self.url, json_data, content_type="application/json")

        self.assertEqual(response.status_code, 404)
        self.assertDictEqual(response.data, {'status': False, 'result': messages.no_record_found})

    def test_post_project_manager_update(self):
        json_data0 = '{"email": "mock3@amsterdam.nl", "projects": []}'

        c = Client()
        response = c.post(self.url, json_data0, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, {'status': True, 'result': 'Project manager updated'})

        json_data1 = '{"email": "mock3@amsterdam.nl", "projects": ["0000000000"]}'
        response = c.post(self.url, json_data1, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, {'status': True, 'result': 'Project manager updated'})
