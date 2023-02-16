""" UNITTESTS """

import os
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.test import TestCase
from amsterdam_app_api.UNITTESTS.mock_data import TestData
from amsterdam_app_api.models import ProjectManager
from amsterdam_app_api.GenericFunctions.IsAuthorized import IsAuthorized
from amsterdam_app_api.GenericFunctions.AESCipher import AESCipher

username = 'mock'
password = 'unsave'
email = 'mock@localhost'


class TestIsAuthorized(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestIsAuthorized, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        # Create user for token
        self.user = get_user_model().objects.create_user(username=username,
                                                         password=password,
                                                         email=email)
        self.user.save()
        response = self.client.post('/api/v1/get-token/', {'username': username, 'password': password})
        self.jwt_token = response.data['access']

        self.factory = RequestFactory()
        ProjectManager.objects.all().delete()
        for project_manager in self.data.project_manager:
            ProjectManager.objects.create(**project_manager)

    def test_valid_token(self):
        @IsAuthorized
        def a_view(request):
            return 'success'

        token = AESCipher('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', os.getenv('AES_SECRET')).encrypt()
        headers = {'Accept': 'application/json', 'UserAuthorization': token}
        request = self.factory.post('/', headers=headers)
        resp = a_view(request)
        self.assertEqual(resp, 'success')

    def test_valid_token_ingest(self):
        @IsAuthorized
        def a_view(request):
            return 'success'

        token = AESCipher('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', os.getenv('AES_SECRET')).encrypt()
        headers = {'Accept': 'application/json', 'HTTP_INGESTAUTHORIZATION': token}
        request = self.factory.post('/', headers=headers)
        resp = a_view(request)
        self.assertEqual(resp, 'success')

    def test_invalid_token_ingest(self):
        @IsAuthorized
        def a_view(request):  # pragma: no cover
            return 'success'

        headers = {'Accept': 'application/json', 'HTTP_INGESTAUTHORIZATION': 'bogus'}
        request = self.factory.post('/', headers=headers)
        result = a_view(request)
        self.assertEqual(result.reason_phrase, 'Forbidden')

    def test_invalid_token(self):
        @IsAuthorized
        def a_view(request):  # pragma: no cover
            return 'success'

        headers = {'Accept': 'application/json', 'UserAuthorization': 'invalid'}
        request = self.factory.post('/', headers=headers)
        result = a_view(request)
        self.assertEqual(result.reason_phrase, 'Forbidden')

    def test_no_token(self):
        @IsAuthorized
        def a_view(request):  # pragma: no cover
            return 'success'

        headers = {'Accept': 'application/json'}
        request = self.factory.post('/', headers=headers)
        result = a_view(request)
        self.assertEqual(result.reason_phrase, 'Forbidden')

    def test_jwt_token_valid(self):
        @IsAuthorized
        def a_view(request):  # pragma: no cover
            return 'success'

        headers = {'Accept': 'application/json', 'HTTP_AUTHORIZATION': self.jwt_token}
        request = self.factory.post('/', headers=headers)
        result = a_view(request)
        self.assertEqual(result, 'success')

    def test_jwt_token_invalid(self):
        @IsAuthorized
        def a_view(request):  # pragma: no cover
            return 'success'

        headers = {'Accept': 'application/json', 'HTTP_AUTHORIZATION': 'bogus'}
        request = self.factory.post('/', headers=headers)
        result = a_view(request)
        self.assertEqual(result.reason_phrase, 'Forbidden')