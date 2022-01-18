from django.test import TestCase
from unittest.mock import patch
from amsterdam_app_api.UNITTESTS.mock_functions import IproxStadslokettenValid
from amsterdam_app_api.UNITTESTS.mock_functions import IproxStadslokettenInvalid
from amsterdam_app_api.UNITTESTS.mock_functions import IproxStadslokettenException
from amsterdam_app_api.UNITTESTS.mock_functions import IproxStadsloketValid
from amsterdam_app_api.UNITTESTS.mock_functions import IproxStadsloketInvalid
from amsterdam_app_api.UNITTESTS.mock_functions import IproxStadsloketScraper
from amsterdam_app_api.UNITTESTS.mock_functions import IproxStadsloketException
from amsterdam_app_api.UNITTESTS.mock_functions import IproxStadsloketScraperImages
from amsterdam_app_api.UNITTESTS.mock_functions import MockedThreading
from amsterdam_app_api.FetchData.IproxStadsloketten import IproxStadsloketten
from amsterdam_app_api.FetchData.IproxStadsloketten import IproxStadsloket
from amsterdam_app_api.FetchData.IproxStadsloketten import Scraper
from amsterdam_app_api.models import CityContact, CityOffice, CityOffices
from amsterdam_app_api.serializers import CityContactSerializer, CityOfficeSerializer,CityOfficesSerializer


class TestIproxStadsLoketten(TestCase):
    @patch('requests.get', side_effect=IproxStadslokettenValid)
    def test_ingest_data(self, IproxStadslokettenValid):
        isl = IproxStadsloketten()
        isl.get_data()
        isl.parse_data()
        contact_info = CityContact.objects.first()
        serializer = CityContactSerializer(contact_info, many=False)
        expected_contact_info = {'sections': [{'html': 'text', 'text': 'text', 'title': 'contact'}]}
        self.assertDictEqual(serializer.data, expected_contact_info)

        offices_info = CityOffices.objects.first()
        serializer = CityOfficesSerializer(offices_info, many=False)
        expected_offices_info = {'offices': [{'location': 'loketten', 'url': 'https://sub-page/', 'identifier': 'acddc71dab316d120cc5d84b5565c874'}]}
        self.assertDictEqual(serializer.data, expected_offices_info)

    @patch('requests.get', side_effect=IproxStadslokettenInvalid)
    def test_ingest_invalid_data(self, IproxStadslokettenInvalid):
        isl = IproxStadsloketten()
        isl.get_data()
        contact_info = CityContact.objects.first()

        self.assertEqual(contact_info, None)

    @patch('requests.get', side_effect=IproxStadslokettenException)
    def test_ingest_Exception(self, IproxStadslokettenException):
        isl = IproxStadsloketten()
        isl.get_data()
        contact_info = CityContact.objects.first()

        self.assertEqual(contact_info, None)


class TestIproxStadsLoket(TestCase):
    @patch('requests.get', side_effect=IproxStadsloketValid)
    def test_ingest_data(self, IproxStadsloketValid):
        isl = IproxStadsloket('https://unittest', '0000000000')
        isl.get_data()
        isl.parse_data()
        data = CityOffice.objects.first()
        serializer = CityOfficeSerializer(data, many=False)
        expected_result = {
            'identifier': '0000000000',
            'location': 'Stadsloket Centrum',
            'contact': {
                'Mailen': {'txt': 'text', 'html': 'text'},
                'Openingstijden': {'txt': 'text', 'html': 'text'}
            },
            'images': {
                'type': '',
                'sources': {
                    '1px': {
                        'url': 'https://www.amsterdam.nl/1/2/3/1px/text.jpg',
                        'filename': 'text.jpg',
                        'image_id': 'c561169ab1afedd2130ee56f89e91a99',
                        'description': ''
                    },
                    'orig': {
                        'url': 'https://www.amsterdam.nl/1/2/3/test_orig.jpg',
                        'filename': 'test_orig.jpg',
                        'image_id': 'c717e41e0e5d4946a62dc567b2fda45e',
                        'description': ''
                    }
                }
            },
            'info': {'txt': 'text', 'html': 'text'},
            'address': {'txt': 'text', 'html': 'text'},
            'last_seen': str(data.last_seen).replace(' ', 'T'),
            'active': True
        }

        self.assertDictEqual(serializer.data, expected_result)

    @patch('requests.get', side_effect=IproxStadsloketValid)
    def test_ingest_data_twice(self, IproxStadsloketValid):
        isl = IproxStadsloket('https://unittest', '0000000000')
        isl.get_data()
        isl.parse_data()
        isl.get_data()
        isl.parse_data()
        data = CityOffice.objects.all()
        serializer = CityOfficeSerializer(data, many=True)
        expected_result = {
            'identifier': '0000000000',
            'location': 'Stadsloket Centrum',
            'contact': {
                'Mailen': {'txt': 'text', 'html': 'text'},
                'Openingstijden': {'txt': 'text', 'html': 'text'}
            },
            'images': {
                'type': '',
                'sources': {
                    '1px': {
                        'url': 'https://www.amsterdam.nl/1/2/3/1px/text.jpg',
                        'filename': 'text.jpg',
                        'image_id': 'c561169ab1afedd2130ee56f89e91a99',
                        'description': ''
                    },
                    'orig': {
                        'url': 'https://www.amsterdam.nl/1/2/3/test_orig.jpg',
                        'filename': 'test_orig.jpg',
                        'image_id': 'c717e41e0e5d4946a62dc567b2fda45e',
                        'description': ''
                    }
                }
            },
            'info': {'txt': 'text', 'html': 'text'},
            'address': {'txt': 'text', 'html': 'text'},
            'last_seen': str(data[0].last_seen).replace(' ', 'T'),
            'active': True
        }

        self.assertEqual(len(serializer.data), 1)
        self.assertDictEqual(serializer.data[0], expected_result)

    @patch('requests.get', side_effect=IproxStadsloketInvalid)
    def test_ingest_invalid_data(self, IproxStadsloketInvalid):
        isl = IproxStadsloket('https://unittest', '0000000000')
        isl.get_data()
        isl.parse_data()
        data = CityOffice.objects.first()

        self.assertEqual(data, None)

    @patch('requests.get', side_effect=IproxStadsloketException)
    def test_ingest_Exception(self, IproxStadsloketException):
        isl = IproxStadsloket('https://unittest', '0000000000')
        isl.get_data()
        isl.parse_data()
        data = CityOffice.objects.first()

        self.assertEqual(data, None)


class TestIproxStadsLoketScraper(TestCase):
    @patch('threading.Thread', side_effect=MockedThreading)
    @patch('requests.get', side_effect=IproxStadsloketScraper)
    def test_iprox_stads_loket_scraper(self, MockedThreading, IproxStadsloketScraper):
        with patch('amsterdam_app_api.FetchData.Image.run', side_effect=IproxStadsloketScraperImages):
            scraper = Scraper()
            scraper.run()

        contact_info = CityContact.objects.first()
        serializer = CityContactSerializer(contact_info, many=False)
        expected_contact_info = {'sections': [{'html': 'text', 'text': 'text', 'title': 'contact'}]}
        self.assertDictEqual(serializer.data, expected_contact_info)

        offices_info = CityOffices.objects.first()
        serializer = CityOfficesSerializer(offices_info, many=False)
        expected_offices_info = {'offices': [
            {'location': 'loketten', 'url': 'https://sub-page/', 'identifier': 'acddc71dab316d120cc5d84b5565c874'}]}
        self.assertDictEqual(serializer.data, expected_offices_info)

        data = CityOffice.objects.first()
        serializer = CityOfficeSerializer(data, many=False)
        expected_result = {
            'identifier': 'acddc71dab316d120cc5d84b5565c874',
            'location': 'Stadsloket Centrum',
            'contact': {
                'Mailen': {'txt': 'text', 'html': 'text'},
                'Openingstijden': {'txt': 'text', 'html': 'text'}
            },
            'images': {
                'type': '',
                'sources': {
                    '1px': {
                        'url': 'https://www.amsterdam.nl/1/2/3/1px/text.jpg',
                        'filename': 'text.jpg',
                        'image_id': 'c561169ab1afedd2130ee56f89e91a99',
                        'description': ''
                    },
                    'orig': {
                        'url': 'https://www.amsterdam.nl/1/2/3/test_orig.jpg',
                        'filename': 'test_orig.jpg',
                        'image_id': 'c717e41e0e5d4946a62dc567b2fda45e',
                        'description': ''
                    }
                }
            },
            'info': {'txt': 'text', 'html': 'text'},
            'address': {'txt': 'text', 'html': 'text'},
            'last_seen': str(data.last_seen).replace(' ', 'T'),
            'active': True
        }

        self.assertDictEqual(serializer.data, expected_result)
