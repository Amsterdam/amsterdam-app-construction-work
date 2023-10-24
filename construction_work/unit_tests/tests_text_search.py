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
        result = search_text_in_model(
            Project,
            "titl",
            "title,subtitle",
            return_fields="title,subtitle",
            page_size=2,
            page=0,
        )
        expected_result = {
            "result": [
                {"title": "title first project", "subtitle": "subtitle first project", "score": 1.0},
                {"title": "title second project", "subtitle": "subtitle second project", "score": 1.0},
            ],
            "page": {"number": 1, "size": 2, "totalElements": 2, "totalPages": 1},
        }

        self.assertDictEqual(result, expected_result)

    def test_search_paginated(self):
        """test text search paginated result"""
        result = search_text_in_model(
            Project,
            "titl",
            "title,subtitle",
            return_fields="title,subtitle",
            page_size=1,
            page=1,
        )
        expected_result = {
            "result": [{"title": "title second project", "subtitle": "subtitle second project", "score": 1.0}],
            "page": {"number": 2, "size": 1, "totalElements": 2, "totalPages": 2},
        }

        self.assertDictEqual(result, expected_result)

    def test_search_2_letters(self):
        """test text search 2 char"""
        result = search_text_in_model(
            Project,
            "ti",
            "title,subtitle",
            return_fields="title,subtitle",
            page_size=2,
            page=0,
        )
        expected_result = {"page": [], "pages": 0}

        self.assertDictEqual(result, expected_result)
