import json
from django.test import TestCase
from unittest.mock import patch
from django.test import Client
from amsterdam_app_api.UNITTESTS.mock_functions import IproxStadslokettenValid
from amsterdam_app_api.UNITTESTS.mock_functions import IproxStadsloketValid
from amsterdam_app_api.FetchData.IproxStadsloketten import IproxStadsloketten
from amsterdam_app_api.FetchData.IproxStadsloketten import IproxStadsloket
from amsterdam_app_api.api_messages import Messages
from amsterdam_app_api.models import CityOffice

messages = Messages()


class SetUp:
    def __init__(self):
        self.ingest_data_stadsloketten()
        self.ingest_data_stadsloket()

    @patch('requests.get', side_effect=IproxStadslokettenValid)
    def ingest_data_stadsloketten(self, IproxStadslokettenValid):
        isl = IproxStadsloketten()
        isl.get_data()
        isl.parse_data()

    @patch('requests.get', side_effect=IproxStadsloketValid)
    def ingest_data_stadsloket(self, IproxStadsloketValid):
        isl = IproxStadsloket('https://unittest', '0000000000')
        isl.get_data()
        isl.parse_data()


class TestApiCity(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestApiCity, self).__init__(*args, **kwargs)

    def setUp(self):
        SetUp()

    def test_contact(self):
        c = Client()
        response = c.get('/api/v1/city/contact', {})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, {'status': True, 'result': {'sections': [{'html': 'text', 'text': 'text', 'title': 'contact'}]}})

    def test_offices(self):
        c = Client()
        response = c.get('/api/v1/city/offices', {})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, {'status': True, 'result': {'offices': [{'url': 'https://sub-page/', 'title': 'loketten', 'identifier': 'acddc71dab316d120cc5d84b5565c874'}]}})

    def test_office_valid(self):
        c = Client()
        response = c.get('/api/v1/city/office', {'id': '0000000000'})
        result = json.loads(response.content)
        office = CityOffice.objects.filter(pk='0000000000').first()
        expected_result = {
            'status': True,
            'result': {
                'identifier': '0000000000',
                'title': 'Stadsloket Centrum',
                'contact': {'Mailen': {'text': 'text', 'html': 'text'},
                            'Openingstijden': {'text': 'text', 'html': 'text'}},
                'images': {'type': '',
                           'sources': {'1px':
                                           {'url': 'https://www.amsterdam.nl/1/2/3/1px/text.jpg',
                                            'filename': 'text.jpg',
                                            'image_id': 'c561169ab1afedd2130ee56f89e91a99',
                                            'description': ''},
                                       'orig':
                                           {'url': 'https://www.amsterdam.nl/1/2/3/test_orig.jpg',
                                            'filename': 'test_orig.jpg',
                                            'image_id': 'c717e41e0e5d4946a62dc567b2fda45e',
                                            'description': ''}}},
                'info': {'text': 'text', 'html': 'text'},
                'address': {'text': 'text', 'html': 'text'},
                'last_seen': str(office.last_seen).replace(' ', 'T'),
                'active': True
            }
        }
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, expected_result)

    def test_office_no_record(self):
        c = Client()
        response = c.get('/api/v1/city/office', {'id': 'no such record'})
        result = json.loads(response.content)
        self.assertEqual(response.status_code, 404)
        self.assertDictEqual(result, {'status': False, 'result': 'No record found'})

    def test_office_invalid_query(self):
        c = Client()
        response = c.get('/api/v1/city/office', {})
        result = json.loads(response.content)
        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(result, {'status': False, 'result': messages.invalid_query})
