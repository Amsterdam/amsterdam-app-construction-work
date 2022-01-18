from django.test import TestCase
from unittest.mock import patch, call
from amsterdam_app_api.UNITTESTS.mock_data import TestData
from amsterdam_app_api.UNITTESTS.mock_functions import mocked_requests_get
from amsterdam_app_api.FetchData.IproxProject import IproxProject
from amsterdam_app_api.GenericFunctions.Logger import Logger


iprox_details_result = {'identifier': 'identifier', 'body': {'contact': [{'title': 'Contact', 'html': '\r\n              <div>\r\n                <ul>\r\n                  <li>\r\n                    <p>Ester Seinen, omgevingsmanager<br /><a href="mailto:e.seijnen@amsterdam.nl">e.seijnen@amsterdam.nl</a><br /><a href="tel:0657875986" class="externLink">06 5787 5986</a></p>\r\n                  </li>\r\n                </ul>\r\n              </div>\r\n            ', 'text': 'Ester Seinen, omgevingsmanager\n\ne.seijnen@amsterdam.nl\n\n06 5787 5986'}], 'what': [{'title': 'Wat er gaat gebeuren', 'html': '\r\n              <div>\r\n                <p>De kademuur ter hoogte van Herengracht 213 tot en met 243 is in slechte staat. Dit is de kade tussen de Raadhuisstraat en de Gasthuismolensteeg. Op lange termijn gaan we kademuur helemaal vernieuwen. We hebben tijdelijke maatregelen genomen om de kademuur veilig te houden tot de vernieuwing.</p>\r\n                <p>In 2021 is op basis van onderzoek en metingen vastgesteld dat de houten fundering onder de kademuur op meerdere plekken gebreken vertoont. Zoals funderingspalen die scheef onder de kademuur staan. In het metselwerk van de kademuur zitten scheuren. De kademuur bewoog op meerdere punten richting het water.</p>\r\n              </div>\r\n            ', 'text': 'De kademuur ter hoogte van Herengracht 213 tot en met 243 is in slechte staat. Dit is de kade tussen de Raadhuisstraat en de Gasthuismolensteeg. Op lange termijn gaan we kademuur helemaal vernieuwen. We hebben tijdelijke maatregelen genomen om de kademuur veilig te houden tot de vernieuwing.\n\nIn 2021 is op basis van onderzoek en metingen vastgesteld dat de houten fundering onder de kademuur op meerdere plekken gebreken vertoont. Zoals funderingspalen die scheef onder de kademuur staan. In het metselwerk van de kademuur zitten scheuren. De kademuur bewoog op meerdere punten richting het water.'}], 'when': [], 'where': [], 'work': [{'title': 'Maatregelen', 'html': '\r\n              <div>\r\n                <ul>\r\n                  <li>Van 10 mei tot 27 augustus 2021 was de Herengracht tussen de Raadhuisstraat en de Gasthuismolensteeg afgesloten voor gemotoriseerd verkeer.</li>\r\n                  <li>Van 12 juli tot 26 augustus 2021 is de kademuur versterkt met een veiligheidsconstructie van damwanden die in het water voor de kade is geplaatst.</li>\r\n                  <li>Op de rand van de kade staat een laag, groen hek. Dit is een bescherming om te voorkomen dat mensen hier van de kade, op de veiligheidsconstructie vallen. Het hek blijft staan tot de vernieuwing van de kademuur.</li>\r\n                  <li>Ter hoogte van Herengracht 213 tot en met 243 geldt een afmeerverbod. De veiligheidsconstructie voor de kade is niet berekend op het afmeren van vaartuigen.</li>\r\n                  <li>In het najaar van 2021 zetten we planten in het zand tussen de veiligheidsconstructie en de kademuur. Zo geven we de kade een groenere aanblik en stimuleren we de biodiversiteit.</li>\r\n                  <li>We blijven de kademuur voorlopig volgen met metingen.</li>\r\n                </ul>\r\n              </div>\r\n            ', 'text': 'Van 10 mei tot 27 augustus 2021 was de Herengracht tussen de Raadhuisstraat en de Gasthuismolensteeg afgesloten voor gemotoriseerd verkeer.\n\nVan 12 juli tot 26 augustus 2021 is de kademuur versterkt met een veiligheidsconstructie van damwanden die in het water voor de kade is geplaatst.\n\nOp de rand van de kade staat een laag, groen hek. Dit is een bescherming om te voorkomen dat mensen hier van de kade, op de veiligheidsconstructie vallen. Het hek blijft staan tot de vernieuwing van de kademuur.\n\nTer hoogte van Herengracht 213 tot en met 243 geldt een afmeerverbod. De veiligheidsconstructie voor de kade is niet berekend op het afmeren van vaartuigen.\n\nIn het najaar van 2021 zetten we planten in het zand tussen de veiligheidsconstructie en de kademuur. Zo geven we de kade een groenere aanblik en stimuleren we de biodiversiteit.\n\nWe blijven de kademuur voorlopig volgen met metingen.'}], 'more-info': [], 'timeline': {}}, 'coordinates': {'lon': 4.887316271657294, 'lat': 52.37283170758355}, 'district_id': 5398, 'district_name': 'Centrum', 'images': [{'type': '', 'sources': {'460px': {'url': 'https://www.amsterdam.nl/publish/pages/970738/460px/940x415_herengracht.jpg', 'image_id': 'f095eeef510f01e1e01c5f7f063a77fe', 'filename': '940x415_herengracht.jpg', 'description': ''}, '80px': {'url': 'https://www.amsterdam.nl/publish/pages/970738/80px/940x415_herengracht.jpg', 'image_id': '012cf4438e0c48f845d26990b4c61960', 'filename': '940x415_herengracht.jpg', 'description': ''}, '220px': {'url': 'https://www.amsterdam.nl/publish/pages/970738/220px/940x415_herengracht.jpg', 'image_id': '41e5ee9929926969a030488f4f82b216', 'filename': '940x415_herengracht.jpg', 'description': ''}, '700px': {'url': 'https://www.amsterdam.nl/publish/pages/970738/700px/940x415_herengracht.jpg', 'image_id': 'ba42fc12977613b3441bc5284b4c133e', 'filename': '940x415_herengracht.jpg', 'description': ''}, 'orig': {'url': 'https://www.amsterdam.nl/publish/pages/970738/940x415_herengracht.jpg', 'image_id': 'ec2d07b2ba8382d636bd5b5354da094d', 'filename': '940x415_herengracht.jpg', 'description': ''}}}], 'news': [], 'page_id': 970738, 'title': 'Herengracht 213 tot 243', 'subtitle': 'Maatregelen door slechte kademuur', 'rel_url': 'verkeersprojecten/kademuren/maatregelen-vernieuwen/herengracht-213-243', 'url': 'https://www.amsterdam.nl/verkeersprojecten/kademuren/maatregelen-vernieuwen/herengracht-213-243/'}


class TestProjectDetails(TestCase):
    @patch('requests.get', mocked_requests_get)
    def test_get_data_valid_item_is_none(self):
        iprox_project = IproxProject('invalid_json_response', 'identifier')
        iprox_project.get_data()

        self.assertEqual(iprox_project.identifier, 'identifier')
        self.assertDictEqual(iprox_project.page, {})
        self.assertEqual(iprox_project.page_type, '')
        self.assertEqual(iprox_project.url, 'invalid_json_response?AppIdt=app-pagetype&reload=true')

    @patch('requests.get', mocked_requests_get)
    def test_get_data_valid_item_is_not_none(self):
        iprox_project = IproxProject('valid_json_response', 'identifier')
        iprox_project.get_data()

        self.assertEqual(iprox_project.identifier, 'identifier')
        self.assertDictEqual(iprox_project.page, {'pagetype': 'mock'})
        self.assertEqual(iprox_project.page_type, 'mock')
        self.assertEqual(iprox_project.url, 'valid_json_response?AppIdt=app-pagetype&reload=true')

    @patch.object(Logger, 'error')
    @patch('requests.get', mocked_requests_get)
    def test_get_data_raise_exception(self, mock):
        iprox_project = IproxProject('raise_exception', 'identifier')
        iprox_project.get_data()

        self.assertEqual(iprox_project.identifier, 'identifier')
        self.assertDictEqual(iprox_project.page, {})
        self.assertEqual(iprox_project.page_type, '')
        self.assertEqual(iprox_project.url, 'raise_exception?AppIdt=app-pagetype&reload=true')
        assert mock.call_args_list == [call('failed fetching data from raise_exception?AppIdt=app-pagetype&reload=true: Mock exception')]

    def test_parse_data(self):
        test_data = TestData()
        iprox_project = IproxProject('None', 'identifier')
        iprox_project.raw_data = test_data.iprox_project_detail
        iprox_project.page = test_data.iprox_project_detail.get('item').get('page')
        iprox_project.parse_data()

        self.assertDictEqual(iprox_project.details, iprox_details_result)
