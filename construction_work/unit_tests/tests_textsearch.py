""" unit_tests """
from django.db import DEFAULT_DB_ALIAS, connections
from django.test import TestCase

from construction_work.generic_functions.text_search import TextSearch
from construction_work.models import Project
from construction_work.unit_tests.mock_data import TestData


# TODO: fix
ProjectDetail = None

class SetUp:
    """Create needed database extensions"""

    def __init__(self):
        connection = connections[DEFAULT_DB_ALIAS]
        cursor = connection.cursor()
        cursor.execute("CREATE EXTENSION pg_trgm")
        cursor.execute("CREATE EXTENSION unaccent")

        self.data = TestData()
        for project in self.data.projects:
            Project.objects.create(**project)

        for project_detail in self.data.project_details:
            project_detail["identifier"] = Project.objects.filter(pk=project_detail["identifier"]).first()
            ProjectDetail.objects.create(**project_detail)


class TestTextSearch(TestCase):
    """Unittest text search"""

    def __init__(self, *args, **kwargs):
        super(TestTextSearch, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        """Setup test db"""
        SetUp()

    def test_search(self):
        """Test text search"""
        text_search = TextSearch(
            ProjectDetail, "test0", "title,subtitle", return_fields="title,subtitle", page_size=2, page=0
        )
        result = text_search.search()
        expected_result = {
            "result": [
                {"title": "test0", "subtitle": "subtitle", "score": 1.0},
                {"title": "test0", "subtitle": "subtitle", "score": 1.0},
            ],
            "page": {"number": 1, "size": 2, "totalElements": 2, "totalPages": 1},
        }

        self.assertDictEqual(result, expected_result)

    def test_search_paginated(self):
        """test text search paginated result"""
        text_search = TextSearch(
            ProjectDetail, "test0", "title,subtitle", return_fields="title,subtitle", page_size=1, page=1
        )
        result = text_search.search()
        expected_result = {
            "result": [{"title": "test0", "subtitle": "subtitle", "score": 1.0}],
            "page": {"number": 2, "size": 1, "totalElements": 2, "totalPages": 2},
        }

        self.assertDictEqual(result, expected_result)

    def test_search_2_letters(self):
        """test text search 2 char"""
        text_search = TextSearch(
            ProjectDetail, "te", "title,subtitle", return_fields="title,subtitle", page_size=2, page=0
        )
        result = text_search.search()
        expected_result = {"page": [], "pages": 0}

        self.assertDictEqual(result, expected_result)
