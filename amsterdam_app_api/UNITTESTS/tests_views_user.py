""" UNITTESTS """
from django.contrib.auth import get_user_model
from django.test import TestCase
from amsterdam_app_api.api_messages import Messages

username = 'mock'
password = 'unsave'
email = 'mock@localhost'


messages = Messages()


class SignInTest(TestCase):
    """ Test django jwt signin """
    def setUp(self):
        """ Setup test db """
        self.user = get_user_model().objects.create_user(username=username,
                                                         password=password,
                                                         email=email)
        self.user.save()
        response = self.client.post('/api/v1/get-token/', {'username': username, 'password': password})
        self.headers = {'Accept': 'application/json', 'AUTHORIZATION': response.data['access']}

    def tearDown(self):
        """ Run teardown setup """
        self.user = get_user_model().objects.filter(username=username).first()
        self.user.delete()

    def test_change_password_valid(self):
        """ Test valid password """
        payload = {
            'username': username,
            'old_password': password,
            'password': '012345678',
            'password_verify': '012345678'
        }

        response = self.client.post('/api/v1/user/password', payload, headers=self.headers)
        self.assertEqual(response.data, {'status': True, 'result': 'password updated'})
        self.assertEqual(response.status_code, 200)

    def test_missing_parameter(self):
        """ test missing parameter """
        payload = {
            'old_password': password,
            'password': '012345678',
            'password_verify': '012345678'
        }

        response = self.client.post('/api/v1/user/password', payload, headers=self.headers)
        self.assertEqual(response.data, {'status': False, 'result': messages.invalid_query})
        self.assertEqual(response.status_code, 422)

    def test_password_do_not_match(self):
        """ Test non-matching passwords """
        payload = {
            'username': username,
            'old_password': password,
            'password': '012345678',
            'password_verify': '87654321'
        }

        response = self.client.post('/api/v1/user/password', payload, headers=self.headers)
        self.assertEqual(response.data, {'status': False, 'result': messages.do_not_match})
        self.assertEqual(response.status_code, 401)

    def test_password_invalid_username(self):
        """ test invalid username """
        payload = {
            'username': 'does_not_exist',
            'old_password': password,
            'password': '012345678',
            'password_verify': '012345678'
        }

        response = self.client.post('/api/v1/user/password', payload, headers=self.headers)
        self.assertEqual(response.data, {'status': False, 'result': messages.invalid_username_or_password})
        self.assertEqual(response.status_code, 401)

    def test_password_invalid_password(self):
        """ test invalid password """
        payload = {
            'username': username,
            'old_password': 'invalid_password',
            'password': '012345678',
            'password_verify': '012345678'
        }

        response = self.client.post('/api/v1/user/password', payload, headers=self.headers)
        self.assertEqual(response.data, {'status': False, 'result': messages.invalid_username_or_password})
        self.assertEqual(response.status_code, 401)
