""" unit_tests """
from django.db import DEFAULT_DB_ALIAS, connections
from django.test import TestCase

from construction_work.generic_functions.text_search import search_text_in_model
from construction_work.models import Project
from construction_work.unit_tests.mock_data import TestData


class TestTextSearch(TestCase):
    """Unittest text search"""

    def __init__(self, *args, **kwargs):
        super(TestTextSearch, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        """Setup test db"""
        connection = connections[DEFAULT_DB_ALIAS]
        cursor = connection.cursor()
        cursor.execute("CREATE EXTENSION pg_trgm")
        cursor.execute("CREATE EXTENSION unaccent")

        self.data = TestData()
        for project in self.data.projects:
            Project.objects.create(**project)

    def test_search(self):
        """Test text search"""
        results = search_text_in_model(Project, "titl", "title,subtitle", return_fields="title,subtitle")

        expected_result = [2048, 4096]
        for i, result in enumerate(results):
            self.assertEqual(expected_result[i], result.foreign_id)

    def test_search_2_letters(self):
        """test text search 2 char"""
        result = search_text_in_model(Project, "ti", "title,subtitle", return_fields="title,subtitle")
        expected_result = []

        self.assertListEqual(result, expected_result)
