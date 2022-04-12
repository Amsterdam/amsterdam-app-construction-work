import json
from django.test import TestCase
from django.test import Client
from amsterdam_app_api.models import CityOffice, CityOffices, CityContact
from amsterdam_app_api.api_messages import Messages

messages = Messages()


class TestApiCity(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestApiCity, self).__init__(*args, **kwargs)

    def setUp(self):
        stadslokketten = [{'url': 'https://mock/', 'title': 'mock', 'identifier': '0000000000'}]
        stadsloket = {
            "identifier": "0000000000",
            "title": "mock",
            "contact": {
                "Bellen": {
                    "html": "<div>mock</div>",
                    "text": "mock"
                },
                "Mailen": {
                    "html": "<div>mock</div>",
                    "text": "mock"
                },
                "Openingstijden": {
                    "html": "<div>mock</div>",
                    "text": "mock"
                },
            },
            "images": {
                "type": "",
                "sources": {
                    "80px": {
                        "url": "https://mock.jpg",
                        "filename": "mock.jpg",
                        "image_id": "00000000",
                        "description": ""
                    }
                }
            },
            "info": {
                "html": "<div>mock</div>",
                "text": "mock"
            },
            "address": {
                "html": "<div>mock</div>",
                "text": "mock"
            },
            "last_seen": "1970-01-01T00:00:00.000000",
            "active": True
        }
        sections = [{'html': '<div>mock</div>', 'text': 'mock', 'title': 'mock'}]
        CityOffices(offices=stadslokketten).save()
        CityOffice(**stadsloket).save()
        CityContact(sections=sections).save()

    def test_contact(self):
        c = Client()
        response = c.get('/api/v1/city/contact', {})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, {'status': True, 'result': {'sections': [{'html': '<div>mock</div>', 'text': 'mock', 'title': 'mock'}]}})

    def test_offices(self):
        c = Client()
        response = c.get('/api/v1/city/offices', {})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, {'status': True, 'result': {'offices': [{'url': 'https://mock/', 'title': 'mock', 'identifier': '0000000000'}]}})

    def test_office_valid(self):
        c = Client()
        response = c.get('/api/v1/city/office', {'id': '0000000000'})
        result = json.loads(response.content)
        office = CityOffice.objects.filter(pk='0000000000').first()
        expected_result = {'status': True,
                           'result': {'identifier': '0000000000',
                                      'title': 'mock',
                                      'contact': {'Bellen': {'html': '<div>mock</div>', 'text': 'mock'},
                                                  'Mailen': {'html': '<div>mock</div>', 'text': 'mock'},
                                                  'Openingstijden': {'html': '<div>mock</div>', 'text': 'mock'}},
                                      'images': {'type': '', 'sources': {'80px': {'url': 'https://mock.jpg', 'filename': 'mock.jpg', 'image_id': '00000000', 'description': ''}}},
                                      'info': {'html': '<div>mock</div>', 'text': 'mock'},
                                      'address': {'html': '<div>mock</div>', 'text': 'mock'},
                                      'last_seen': str(office.last_seen).replace(' ', 'T'), 'active': True}}
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
