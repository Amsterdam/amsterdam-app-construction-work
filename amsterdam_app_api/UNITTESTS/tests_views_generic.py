""" UNITTESTS """
import json
from django.test import Client
from django.test import TestCase
from amsterdam_app_api.GenericFunctions.StaticData import StaticData
from amsterdam_app_api.UNITTESTS.mock_data import TestData
from amsterdam_app_api.models import Assets
from amsterdam_app_api.models import Image
from amsterdam_app_api.api_messages import Messages

messages = Messages()


class SetUp:
    """ Setup test db"""
    def __init__(self):
        self.data = TestData()
        for asset in self.data.assets:
            Assets.objects.create(**asset)

        for image in self.data.images:
            Image.objects.create(**image)


class TestApiImage(TestCase):
    """ UNITTESTS """
    def setUp(self):
        """ Setup test db """
        SetUp()

    def test_invalid_query(self):
        """ Invalid query parameters """
        c = Client()
        response = c.get('/api/v1/image')

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.data, {'status': False, 'result': messages.invalid_query})

    def test_image_does_exist(self):
        """ Request a valid image """
        c = Client()
        response = c.get('/api/v1/image', {'id': '0000000000'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'')

    def test_image_does_not_exist(self):
        """ Image is not existing """
        c = Client()
        response = c.get('/api/v1/image', {'id': 'does not exist'})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, 'Error: file not found')

    def test_method_not_allowed(self):
        """ Invalid http method """
        c = Client()
        response = c.post('/api/v1/image')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertDictEqual(result, {'detail': 'Method "POST" not allowed.'})


class TestApiAsset(TestCase):
    """ UNITTEST """
    def setUp(self):
        """ Setup test db """
        SetUp()

    def test_invalid_query(self):
        """ Invalid query parameters """
        c = Client()
        response = c.get('/api/v1/asset')

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.data, {'status': False, 'result': messages.invalid_query})

    def test_asset_does_exist(self):
        """ A valid request """
        c = Client()
        response = c.get('/api/v1/asset', {'id': '0000000000'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'')

    def test_asset_does_not_exist(self):
        """ The asset doesn't exist """
        c = Client()
        response = c.get('/api/v1/asset', {'id': 'does not exist'})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, 'Error: file not found')

    def test_method_not_allowed(self):
        """ Invalid http method """
        c = Client()
        response = c.post('/api/v1/asset')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertDictEqual(result, {'detail': 'Method "POST" not allowed.'})


class TestApiDistricts(TestCase):
    """ UNITTEST """
    def test_invalid_query(self):
        """ Invalid districts query """
        c = Client()
        response = c.get('/api/v1/districts')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'status': True, 'result': StaticData.districts()})
