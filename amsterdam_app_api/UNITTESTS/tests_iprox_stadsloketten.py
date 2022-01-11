from django.test import TestCase
from unittest.mock import patch, call
from amsterdam_app_api.UNITTESTS.mock_functions import IproxStadslokettenValid, IproxStadslokettenInvalid, IproxStadslokettenException
from amsterdam_app_api.FetchData.IproxStadsloketten import IproxStadsloketten
from amsterdam_app_api.models import CityContacts


class TestProjects(TestCase):
    @patch('requests.get', side_effect=IproxStadslokettenValid)
    def test_ingest_data(self, IproxStadslokettenValid):
        isl = IproxStadsloketten()
        isl.get_data()
        isl.parse_data()
        contact_info = CityContacts.objects.first()

        self.assertDictEqual(contact_info.contact, {'contact': {'html': 'text', 'text': 'text'}})

    @patch('requests.get', side_effect=IproxStadslokettenInvalid)
    def test_ingest_invalid_data(self, IproxStadslokettenInvalid):
        isl = IproxStadsloketten()
        isl.get_data()
        contact_info = CityContacts.objects.first()

        self.assertEqual(contact_info, None)

    @patch('requests.get', side_effect=IproxStadslokettenException)
    def test_ingest_Exception(self, IproxStadslokettenException):
        isl = IproxStadsloketten()
        isl.get_data()
        contact_info = CityContacts.objects.first()

        self.assertEqual(contact_info, None)


