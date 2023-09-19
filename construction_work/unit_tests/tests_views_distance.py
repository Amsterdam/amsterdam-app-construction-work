""" unit_tests """
import json
from unittest.mock import patch

from django.test import Client, TestCase

from construction_work.api_messages import Messages
from construction_work.models import Project
from construction_work.unit_tests.mock_data import TestData
from construction_work.unit_tests.mock_functions import address_to_coordinates

messages = Messages()


class TestApiProjectDistance(TestCase):
    """unit_tests"""

    def __init__(self, methodName: str) -> None:
        self.maxDiff = None
        super().__init__(methodName)

    def setUp(self):
        """Setup test db"""
        self.data = TestData()
        for project in self.data.projects:
            Project.objects.create(**project)

    def test_invalid_query(self):
        """Test invalid distance query"""
        c = Client()
        response = c.get("/api/v1/projects/distance", {})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(result, {"status": False, "result": messages.distance_params})

    def test_invalid_lon_lat(self):
        """Test invalid latitude longitude query"""
        c = Client()
        response = c.get("/api/v1/projects/distance", {"lat": "a", "lon": "b"})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 500)
        self.assertDictEqual(result, {"status": False, "result": "could not convert string to float: 'a'"})

    def test_valid_lon_lat(self):
        """Test valid latitude longitude query"""
        c = Client()
        response = c.get("/api/v1/projects/distance", {"lat": "1.0", "lon": "0.0", "fields": "project_id,title"})
        result = json.loads(response.content)
        expected_result = {
            "status": True,
            "result": [
                {"project_id": "0000000001", "title": "title", "meter": 111302, "strides": 150408},
                {"project_id": "0000000000", "title": "title", "meter": None, "strides": None},
            ],
        }
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, expected_result)

    def test_valid_lon_lat_radius(self):
        """Test valid radius"""
        c = Client()
        response = c.get(
            "/api/v1/projects/distance", {"lat": "1.0", "lon": "0.1", "radius": 111000, "fields": "project_id,title"}
        )
        result = json.loads(response.content)
        expected_result = {
            "status": True,
            "result": [{"project_id": "0000000001", "title": "title", "meter": 100172, "strides": 135367}],
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, expected_result)

    @patch("requests.get", side_effect=address_to_coordinates)
    def test_by_street(self, _address_to_coordinates):
        """Address to coordinate test"""
        c = Client()
        response = c.get("/api/v1/projects/distance", {"address": "sesame street 1", "fields": "project_id,title"})
        result = json.loads(response.content)
        expected_result = {
            "status": True,
            "result": [
                {"project_id": "0000000001", "title": "title", "meter": 10112540, "strides": 13665594},
                {"project_id": "0000000000", "title": "title", "meter": None, "strides": None},
            ],
        }
        
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, expected_result)

    @patch("requests.get", side_effect=address_to_coordinates)
    def test_no_fields_filter(self, _address_to_coordinates):
        """Test address to coordinate  test without content filter"""
        c = Client()
        response = c.get("/api/v1/projects/distance", {"address": "sesame street 1"})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result["result"]), 2)
        self.assertEqual(len(result["result"][0]), 19)
        self.assertEqual(len(result["result"][1]), 19)
