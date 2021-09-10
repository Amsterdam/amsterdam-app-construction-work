from django.test import TestCase
from unittest.mock import patch, call
from amsterdam_app_api.UNITTESTS.mock_data import TestData
from amsterdam_app_api.UNITTESTS.mock_functions import mocked_requests_get
from amsterdam_app_api.FetchData.IproxProjects import IproxProjects
from amsterdam_app_api.GenericFunctions.Logger import Logger


iprox_raw_data_result = [{'category': 'Algemeen', 'feedid': 'https://www.amsterdam.nl/projecten/kademuren/maatregelen-vernieuwen/baarsjesweg-216-313/', 'publication_date': '2020-06-27', 'modification_date': '2021-08-31', 'image_url': 'https://www.amsterdam.nl/publish/varianten/368/logo_voor_social.png', 'title': 'Baarsjesweg 216 - 313: vernieuwen kademuur', 'content': '<div><p>De kademuur ter hoogte van de Baarsjesweg 216 tot 313, tussen de Postjesweg en Surinamestraat, is in slechte staat. We nemen tijdelijke maatregelen.</p></div>', 'source_url': 'https://www.amsterdam.nl/projecten/kademuren/maatregelen-vernieuwen/baarsjesweg-216-313/', 'related_articles': '', 'author': '', 'photo_author': '', 'images': []}]
iprox_parsed_data = [{'project_type': 'identifier', 'identifier': '8ac7ed07fc76a0812b3afbd5f0182aeb', 'district_id': -1, 'district_name': '', 'title': 'Baarsjesweg 216 - 313', 'subtitle': 'Vernieuwen kademuur', 'content_html': '<div><p>De kademuur ter hoogte van de Baarsjesweg 216 tot 313, tussen de Postjesweg en Surinamestraat, is in slechte staat. We nemen tijdelijke maatregelen.</p></div>', 'content_text': 'De kademuur ter hoogte van de Baarsjesweg 216 tot 313, tussen de Postjesweg en Surinamestraat, is in slechte staat. We nemen tijdelijke maatregelen.', 'images': [], 'publication_date': '2020-06-27', 'modification_date': '2021-08-31', 'source_url': 'https://www.amsterdam.nl/projecten/kademuren/maatregelen-vernieuwen/baarsjesweg-216-313/'}]


class TestProjects(TestCase):
    @patch.object(Logger, 'error')
    @patch('requests.get', mocked_requests_get)
    def test_get_data_raise_exception(self, mock):
        iprox_project = IproxProjects('/raise_exception', 'identifier')
        iprox_project.get_data()

        assert mock.call_args_list == [call('failed fetching data from https://www.amsterdam.nl/raise_exception?new_json=true&pager_rows=1000: Mock exception')]

    @patch.object(Logger, 'error')
    @patch('requests.get', mocked_requests_get)
    def test_get_data(self, mock):
        iprox_project = IproxProjects('/get', 'identifier')
        iprox_project.get_data()

        self.assertEqual(iprox_project.raw_data, iprox_raw_data_result)

    def test_parse_data(self):
        test_data = TestData()
        iprox_project = IproxProjects('/get', 'identifier')
        iprox_project.raw_data = test_data.iprox_projects
        iprox_project.parse_data()

        self.assertEqual(iprox_project.parsed_data, iprox_parsed_data)

    @patch.object(Logger, 'error')
    def test_parse_data_raise_exception(self, mock):
        test_data = TestData()
        test_data.iprox_projects[0]['title'] = b'0xFFFF'  # Bytes are not str.splittable
        iprox_project = IproxProjects('/get', 'identifier')
        iprox_project.raw_data = test_data.iprox_projects
        iprox_project.parse_data()

        assert mock.call_args_list == [call("failed parsing data from https://www.amsterdam.nl/get?new_json=true&pager_rows=1000: a bytes-like object is required, not 'str'")]
