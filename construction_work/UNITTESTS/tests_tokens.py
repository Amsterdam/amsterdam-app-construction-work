""" UNITTESTS """

import json
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.test import TestCase

username = 'mock'
password = 'unsave'
email = 'mock@localhost'


class SignInTest(TestCase):
    """ Test django signin """
    def setUp(self):
        """ Setup test db """
        self.user = get_user_model().objects.create_user(username=username,
                                                         password=password,
                                                         email=email)
        self.user.save()

    def tearDown(self):
        """ tear down test db """
        self.user.delete()

    def test_correct(self):
        """ test successful signin """
        user = authenticate(username=username, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.is_authenticated)

    def test_wrong_username(self):
        """ test wrong username """
        user = authenticate(username='wrong', password=password)
        self.assertEqual(user, None)

    def test_wrong_password(self):
        """ test wrong password """
        user = authenticate(username=username, password='wrong')
        self.assertEqual(user, None)


class SignInViewTest(TestCase):
    """ Test signin view """
    def setUp(self):
        """ setup test db """
        self.user = get_user_model().objects.create_user(username=username,
                                                         password=password,
                                                         email=email)
        self.user.save()

    def tearDown(self):
        """ tear down test db """
        self.user.delete()

    def test_correct(self):
        """ test correct signin """
        response = self.client.post('/api/v1/get-token/', {'username': username, 'password': password})
        self.assertTrue(len(str(response.data['access']).split('.')) == 3)
        self.assertTrue(len(str(response.data['refresh']).split('.')) == 3)

    def test_wrong_username(self):
        """ test wrong username """
        response = self.client.post('/api/v1/get-token/', {'username': 'wrong', 'password': password})
        result = json.loads(response.content.decode('utf-8'))
        expected_result = {"detail":"No active account found with the given credentials"}
        self.assertDictEqual(result, expected_result)

    def test_wrong_password(self):
        """ test wrong password """
        response = self.client.post('/api/v1/get-token/', {'username': username, 'password': 'wrong'})
        result = json.loads(response.content.decode('utf-8'))
        expected_result = {"detail": "No active account found with the given credentials"}
        self.assertDictEqual(result, expected_result)


class RefreshTokenViewTest(TestCase):
    """ Test refresh token view """
    def setUp(self):
        """ setup test db """
        self.user = get_user_model().objects.create_user(username=username,
                                                         password=password,
                                                         email=email)
        self.user.save()

    def tearDown(self):
        """ tear down test db """
        self.user.delete()

    def test_correct(self):
        """ test correct refresh token """
        credentials = self.client.post('/api/v1/get-token/', {'username': username, 'password': password})
        self.assertTrue(len(str(credentials.data['access']).split('.')) == 3)
        self.assertTrue(len(str(credentials.data['refresh']).split('.')) == 3)

        response = self.client.post('/api/v1/refresh-token/', {'refresh': credentials.data['refresh']})
        self.assertNotEqual(response.data['access'], credentials.data['access'])
        self.assertTrue(len(str(response.data['access']).split('.')) == 3)

    def test_incorrect(self):
        """ test failed refresh token """
        response = self.client.post('/api/v1/refresh-token/', {'refresh': 'invalid'})
        result = json.loads(response.content.decode('utf-8'))
        expected_result = {"detail": "Token is invalid or expired", "code": "token_not_valid"}
        self.assertDictEqual(result, expected_result)
