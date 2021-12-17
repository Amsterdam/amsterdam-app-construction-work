import json
from django.test import Client
from django.test import TestCase
from amsterdam_app_api.UNITTESTS.mock_data import TestData
from amsterdam_app_api.models import Projects
from amsterdam_app_api.models import ProjectDetails
from amsterdam_app_api.api_messages import Messages

messages = Messages()


class SetUp:
    def __init__(self):
        self.data = TestData()
        for project in self.data.projects:
            Projects.objects.create(**project)

        for project in self.data.project_details:
            ProjectDetails.objects.create(**project)


class TestApiProjectDistance(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestApiProjectDistance, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        SetUp()

    def test_invalid_query(self):
        c = Client()
        response = c.get('/api/v1/projects/distance', {})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(result, {'status': False, 'result': messages.invalid_query})

    def test_invalid_lon_lat(self):
        c = Client()
        response = c.get('/api/v1/projects/distance', {'lat': 'a', 'lon': 'b'})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 500)
        self.assertDictEqual(result, {'status': False, 'result': "could not convert string to float: 'a'"})

    def test_valid_lon_lat(self):
        c = Client()
        response = c.get('/api/v1/projects/distance', {'lat': '1.0', 'lon': '0.0'})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, {'status': True, 'result': [{'project_id': '0000000000', 'name': 'test0', 'meter': 110574, 'strides': 149424}, {'project_id': '0000000001', 'name': 'test0', 'meter': 111302, 'strides': 150408}]})

    def test_valid_lon_lat_radius(self):
        c = Client()
        response = c.get('/api/v1/projects/distance', {'lat': '1.0', 'lon': '0.0', 'radius': 111000})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, {'status': True, 'result': [{'project_id': '0000000000', 'name': 'test0', 'meter': 110574, 'strides': 149424}]})
