import json
from django.test import Client
from django.test import TestCase
from amsterdam_app_api.UNITTESTS.mock_data import TestData
from amsterdam_app_api.models import Assets
from amsterdam_app_api.models import Image
from amsterdam_app_api.api_messages import Messages

messages = Messages()


class SetUp:
    def __init__(self):
        self.data = TestData()
        for asset in self.data.assets:
            Assets.objects.create(**asset)

        for image in self.data.images:
            Image.objects.create(**image)


class TestApiImage(TestCase):
    def setUp(self):
        SetUp()

    def test_invalid_query(self):
        c = Client()
        response = c.get('/api/v1/image')

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.data, {'status': False, 'result': messages.invalid_query})

    def test_image_does_exist(self):
        c = Client()
        response = c.get('/api/v1/image', {'id': '0000000000'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'')

    def test_image_does_not_exist(self):
        c = Client()
        response = c.get('/api/v1/image', {'id': 'does not exist'})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, 'Error: file not found')

    def test_method_not_allowed(self):
        c = Client()
        response = c.post('/api/v1/image')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertDictEqual(result, {'detail': 'Method "POST" not allowed.'})


class TestApiAsset(TestCase):
    def setUp(self):
        SetUp()

    def test_invalid_query(self):
        c = Client()
        response = c.get('/api/v1/asset')

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.data, {'status': False, 'result': messages.invalid_query})

    def test_asset_does_exist(self):
        c = Client()
        response = c.get('/api/v1/asset', {'id': '0000000000'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'')

    def test_asset_does_not_exist(self):
        c = Client()
        response = c.get('/api/v1/asset', {'id': 'does not exist'})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, 'Error: file not found')

    def test_method_not_allowed(self):
        c = Client()
        response = c.post('/api/v1/asset')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertDictEqual(result, {'detail': 'Method "POST" not allowed.'})