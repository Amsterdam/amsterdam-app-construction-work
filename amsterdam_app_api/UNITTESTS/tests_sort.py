""" UNITTESTS """

from django.test import TestCase
from amsterdam_app_api.GenericFunctions.Sort import Sort


class TestSort(TestCase):
    """ test sorting """
    def test_sort_dict_asc(self):
        """ test ascending """
        data = [{'data': 1}, {'data': 0}]
        sort = Sort()
        result = sort.list_of_dicts(data, key='data', sort_order='asc')

        self.assertEqual(result, [{'data': 0}, {'data': 1}])

    def test_sort_dict_desc(self):
        """ test descending """
        data = [{'data': 0}, {'data': 1}]
        sort = Sort()
        result = sort.list_of_dicts(data, key='data', sort_order='desc')

        self.assertEqual(result, [{'data': 1}, {'data': 0}])

    def test_sort_erroneous_data(self):
        """ test invalid input """
        data = [{'data': 0}, None]
        sort = Sort()
        result = sort.list_of_dicts(data, key='data')

        self.assertEqual(result, [{'data': 0}, None])
