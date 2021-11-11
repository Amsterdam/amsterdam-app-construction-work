import json
from django.test import Client
from django.test import TestCase
from amsterdam_app_api.UNITTESTS.mock_data import TestData
from amsterdam_app_api.models import Projects
from amsterdam_app_api.models import ProjectDetails
from amsterdam_app_api.models import News
from amsterdam_app_api.api_messages import Messages

messages = Messages()


class SetUp:
    def __init__(self):
        self.data = TestData()
        for project in self.data.projects:
            Projects.objects.create(**project)

        for project in self.data.project_details:
            ProjectDetails.objects.create(**project)


class TestApiProjects(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestApiProjects, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        SetUp()

    def test_method_not_allowed(self):
        c = Client()
        response = c.post('/api/v1/projects')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertDictEqual(result, {'detail': 'Method "POST" not allowed.'})

    def test_invalid_query(self):
        c = Client()
        response = c.get('/api/v1/projects', {'project-type': 'does not exist'})

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.data, {'status': False, 'result': messages.invalid_query})

    def test_projects_by_district_id(self):
        c = Client()
        response = c.get('/api/v1/projects', {'district-id': 0})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, {'status': True, 'result': [self.data.projects[0]]})

    def test_projects_by_district_id_erroneous(self):
        c = Client()
        response = c.get('/api/v1/projects', {'district-id': 'a'})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, {'status': True, 'result': self.data.projects})

    def test_projects_by_project_type(self):
        c = Client()
        response = c.get('/api/v1/projects', {'project-type': 'kade'})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, {'status': True, 'result': [self.data.projects[0]]})

    def test_projects_sort_by_district_id_desc(self):
        c = Client()
        response = c.get('/api/v1/projects', {'sort-by': 'district_id', 'sort-order': 'desc'})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, {'status': True, 'result': self.data.projects[::-1]})

    def test_projects_sort_by_district_id_asc(self):
        c = Client()
        response = c.get('/api/v1/projects', {'sort-by': 'district_id', 'sort-order': 'asc'})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, {'status': True, 'result': self.data.projects})

    def test_projects_all(self):
        c = Client()
        response = c.get('/api/v1/projects')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, {'status': True, 'result': self.data.projects})


class TestApiProjectDetails(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestApiProjectDetails, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        SetUp()
        self.identifiers = []
        for news in self.data.news:
            news_item = News.objects.create(**news)
            news_item.save()
            self.identifiers.append(news_item.identifier)

    def test_method_not_allowed(self):
        c = Client()
        response = c.post('/api/v1/project/details')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertDictEqual(result, {'detail': 'Method "POST" not allowed.'})

    def test_invalid_query(self):
        c = Client()
        response = c.get('/api/v1/project/details')

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.data, {'status': False, 'result': messages.invalid_query})

    def test_identifier_does_exist(self):
        c = Client()
        response = c.get('/api/v1/project/details', {'id': '0000000000'})
        result = json.loads(response.content)
        expected_result = self.data.project_details[0]
        del expected_result['news']
        expected_result['articles'] = [{'identifier': '0000000000', 'title': 'title0', 'publication_date': '1970-01-01', 'type': 'news', 'image': {'type': 'banner', 'sources': {'orig': {'url': 'https://localhost/image.jpg', 'size': 'orig', 'filename': 'image.jpg', 'image_id': '0000000000', 'description': ''}}}}]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, {'status': True, 'result': expected_result})

    def test_identifier_does_not_exist(self):
        c = Client()
        response = c.get('/api/v1/project/details', {'id': 'does not exist'})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {'status': False, 'result': messages.no_record_found})
