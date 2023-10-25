""" unit_tests """
import json

from django.test import Client, TestCase

from construction_work.api_messages import Messages
from construction_work.generic_functions.static_data import StaticData
from construction_work.models import Asset, Image
from construction_work.unit_tests.mock_data import TestData

messages = Messages()


class SetUp:
    """Setup test db"""

    def __init__(self):
        self.data = TestData()
        for asset in self.data.assets:
            Asset.objects.create(**asset)

        for image in self.data.images:
            Image.objects.create(**image)


class TestApiImage(TestCase):
    """unit_tests"""

    def setUp(self):
        """Setup test db"""
        SetUp()

    def test_invalid_query(self):
        """Invalid query parameters"""
        c = Client()
        response = c.get("/api/v1/image")

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.data, {"status": False, "result": messages.invalid_query})

    def test_image_does_exist(self):
        """Request a valid image"""
        c = Client()
        response = c.get("/api/v1/image", {"id": "0000000000"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"")

    def test_image_does_not_exist(self):
        """Image is not existing"""
        c = Client()
        response = c.get("/api/v1/image", {"id": "does not exist"})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, "Error: file not found")

    def test_method_not_allowed(self):
        """Invalid http method"""
        c = Client()
        response = c.post("/api/v1/image")
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertDictEqual(result, {"detail": 'Method "POST" not allowed.'})
