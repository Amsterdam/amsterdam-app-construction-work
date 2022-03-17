import json
from django.db import connections, DEFAULT_DB_ALIAS
from django.test import Client
from django.test import TestCase
from amsterdam_app_api.UNITTESTS.mock_data import TestData
from amsterdam_app_api.models import Projects
from amsterdam_app_api.models import ProjectDetails
from amsterdam_app_api.api_messages import Messages

messages = Messages()


class SetUp:
    def __init__(self):
        # Create needed database extensions
        connection = connections[DEFAULT_DB_ALIAS]
        cursor = connection.cursor()
        cursor.execute('CREATE EXTENSION pg_trgm')
        cursor.execute('CREATE EXTENSION unaccent')

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
        self.data.projects[0]['last_seen'] = result['result'][0]['last_seen']

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, {'status': True, 'result': [self.data.projects[0]]})

    def test_projects_by_district_id_erroneous(self):
        c = Client()
        response = c.get('/api/v1/projects', {'district-id': 'a'})
        results = json.loads(response.content)
        for result in results['result']:
            for i in range(0, len(self.data.projects), 1):
                if result['identifier'] == self.data.projects[i]['identifier']:
                    self.data.projects[i]['last_seen'] = result['last_seen']

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(results, {'status': True, 'result': self.data.projects})

    def test_projects_by_project_type(self):
        c = Client()
        response = c.get('/api/v1/projects', {'project-type': 'kade'})
        result = json.loads(response.content)
        self.data.projects[0]['last_seen'] = result['result'][0]['last_seen']

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, {'status': True, 'result': [self.data.projects[0]]})

    def test_projects_sort_by_district_id_desc(self):
        c = Client()
        response = c.get('/api/v1/projects', {'sort-by': 'district_id', 'sort-order': 'desc'})
        results = json.loads(response.content)
        for result in results['result']:
            for i in range(0, len(self.data.projects), 1):
                if result['identifier'] == self.data.projects[i]['identifier']:
                    self.data.projects[i]['last_seen'] = result['last_seen']

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(results, {'status': True, 'result': self.data.projects[::-1]})

    def test_projects_sort_by_district_id_asc(self):
        c = Client()
        response = c.get('/api/v1/projects', {'sort-by': 'district_id', 'sort-order': 'asc'})
        results = json.loads(response.content)
        for result in results['result']:
            for i in range(0, len(self.data.projects), 1):
                if result['identifier'] == self.data.projects[i]['identifier']:
                    self.data.projects[i]['last_seen'] = result['last_seen']

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(results, {'status': True, 'result': self.data.projects})

    def test_projects_all(self):
        c = Client()
        response = c.get('/api/v1/projects')
        results = json.loads(response.content)
        for result in results['result']:
            for i in range(0, len(self.data.projects), 1):
                if result['identifier'] == self.data.projects[i]['identifier']:
                    self.data.projects[i]['last_seen'] = result['last_seen']

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(results, {'status': True, 'result': self.data.projects})

    def test_projects_filter_by_title_and_identifier(self):
        c = Client()
        response = c.get('/api/v1/projects', {'fields': 'title,identifier'})
        results = json.loads(response.content)
        expected_result = {
            'status': True,
            'result': [{'title': 'title', 'identifier': '0000000000'}, {'title': 'title', 'identifier': '0000000001'}]
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(results, expected_result)


class TestApiProjectsSearch(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestApiProjectsSearch, self).__init__(*args, **kwargs)

    def setUp(self):
        SetUp()

    def test_search(self):
        c = Client()
        query = {
            'text': 'title',
            'query_fields': 'title,subtitle',
            'fields': 'title,subtitle',
            'page_size': 1,
            'page': 1
        }
        response = c.get('/api/v1/projects/search', query)
        result = json.loads(response.content)
        expected_result = {
            'status': True,
            'result': [{'title': 'title', 'subtitle': 'subtitle', 'score': 1.3333333432674408}],
            'pages': 2
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, expected_result)

    def test_no_text(self):
        c = Client()
        query = {
            'query_fields': 'title,subtitle',
            'fields': 'title,subtitle',
            'page_size': 1,
            'page': 1
        }
        response = c.get('/api/v1/projects/search', query)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(result, {'status': False, 'result': messages.invalid_query})

    def test_invalid_model_field(self):
        c = Client()
        query = {
            'text': 'mock',
            'query_fields': 'mock',
            'fields': 'title,subtitle',
            'page_size': 1,
            'page': 1
        }
        response = c.get('/api/v1/projects/search', query)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(result, {'status': False, 'result': messages.no_such_field_in_model})

    def test_invalid_model_return_field(self):
        c = Client()
        query = {
            'text': 'mock',
            'query_fields': 'title,subtitle',
            'fields': 'mock',
            'page_size': 1,
            'page': 1
        }
        response = c.get('/api/v1/projects/search', query)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(result, {'status': False, 'result': messages.no_such_field_in_model})


class TestApiProjectDetails(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestApiProjectDetails, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        SetUp()

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
        self.data.project_details[0]['last_seen'] = result['result']['last_seen']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, {'status': True, 'result': self.data.project_details[0]})

    def test_identifier_does_not_exist(self):
        c = Client()
        response = c.get('/api/v1/project/details', {'id': 'does not exist'})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {'status': False, 'result': messages.no_record_found})


class TestApiProjectDetailsSearch(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestApiProjectDetailsSearch, self).__init__(*args, **kwargs)

    def setUp(self):
        SetUp()

    def test_search(self):
        c = Client()
        query = {
            'text': 'test0',
            'query_fields': 'title,subtitle',
            'fields': 'title,subtitle',
            'page_size': 1,
            'page': 1
        }
        response = c.get('/api/v1/project/details/search', query)
        result = json.loads(response.content)
        expected_result = {
            'status': True,
            'result': [{'title': 'test0', 'subtitle': 'subtitle', 'score': 1.0}],
            'pages': 2
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, expected_result)

    def test_no_text(self):
        c = Client()
        query = {
            'query_fields': 'title,subtitle',
            'fields': 'title,subtitle',
            'page_size': 1,
            'page': 1
        }
        response = c.get('/api/v1/project/details/search', query)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(result, {'status': False, 'result': messages.invalid_query})

    def test_invalid_model_field(self):
        c = Client()
        query = {
            'text': 'mock',
            'query_fields': 'mock',
            'fields': 'title,subtitle',
            'page_size': 1,
            'page': 1
        }
        response = c.get('/api/v1/project/details/search', query)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(result, {'status': False, 'result': messages.no_such_field_in_model})

    def test_invalid_model_return_field(self):
        c = Client()
        query = {
            'text': 'mock',
            'query_fields': 'title,subtitle',
            'fields': 'mock',
            'page_size': 1,
            'page': 1
        }
        response = c.get('/api/v1/project/details/search', query)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(result, {'status': False, 'result': messages.no_such_field_in_model})

