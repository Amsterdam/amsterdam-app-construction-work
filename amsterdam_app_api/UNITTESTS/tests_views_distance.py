import json
from django.test import Client
from django.test import TestCase
from unittest.mock import patch
from amsterdam_app_api.UNITTESTS.mock_functions import address_to_coordinates
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
        self.assertDictEqual(result, {'status': False, 'result': messages.distance_params})

    def test_invalid_lon_lat(self):
        c = Client()
        response = c.get('/api/v1/projects/distance', {'lat': 'a', 'lon': 'b'})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 500)
        self.assertDictEqual(result, {'status': False, 'result': "could not convert string to float: 'a'"})

    def test_valid_lon_lat(self):
        c = Client()
        response = c.get('/api/v1/projects/distance', {'lat': '1.0', 'lon': '0.0', 'fields': 'identifier,title'})
        result = json.loads(response.content)
        expected_result = {
            'status': True,
            'result': [
                {'identifier': '0000000001', 'title': 'title', 'meter': 111302, 'strides': 150408},
                {'identifier': '0000000000', 'title': 'title', 'meter': None, 'strides': None}
            ]
        }
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, expected_result)

    def test_valid_lon_lat_radius(self):
        c = Client()
        response = c.get('/api/v1/projects/distance', {'lat': '1.0', 'lon': '0.1', 'radius': 111000, 'fields': 'identifier,title'})
        result = json.loads(response.content)
        expected_result = {
            'status': True,
            'result': [{'identifier': '0000000001', 'title': 'title', 'meter': 100172, 'strides': 135368}]
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, expected_result)

    @patch('requests.get', side_effect=address_to_coordinates)
    def test_by_street(self, address_to_coordinates):
        c = Client()
        response = c.get('/api/v1/projects/distance', {'address': 'sesame street 1', 'fields': 'identifier,title'})
        result = json.loads(response.content)
        expected_result = {
            'status': True,
            'result': [
                {'identifier': '0000000001', 'title': 'title', 'meter': 10112540, 'strides': 13665594},
                {'identifier': '0000000000', 'title': 'title', 'meter': None, 'strides': None}
            ]
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, expected_result)

    @patch('requests.get', side_effect=address_to_coordinates)
    def test_no_fields_filter(self, address_to_coordinates):
        c = Client()
        response = c.get('/api/v1/projects/distance', {'address': 'sesame street 1'})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result['result']), 2)
        self.assertEqual(len(result['result'][0]), 16)
        self.assertEqual(len(result['result'][1]), 16)
