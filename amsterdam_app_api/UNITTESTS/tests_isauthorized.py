from django.test import RequestFactory
from django.test import TestCase
from amsterdam_app_api.UNITTESTS.mock_data import TestData
from amsterdam_app_api.models import ProjectManager
from amsterdam_app_api.GenericFunctions.IsAuthorized import IsAuthorized
from amsterdam_app_api.GenericFunctions.AESCipher import AESCipher


class TestIsAuthorized(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestIsAuthorized, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        self.factory = RequestFactory()
        ProjectManager.objects.all().delete()
        for project_manager in self.data.project_manager:
            ProjectManager.objects.create(**project_manager)

    def test_valid_token(self):
        @IsAuthorized
        def a_view(request):
            return 'success'

        token = AESCipher('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '6886b31dfe27e9306c3d2b553345d9e5').encrypt()
        headers = {'Accept': 'application/json', 'UserAuthorization': token}
        request = self.factory.post('/', headers=headers)
        resp = a_view(request)
        self.assertEqual(resp, 'success')

    def test_invalid_token(self):
        @IsAuthorized
        def a_view(request):  # pragma: no cover
            return 'success'

        headers = {'Accept': 'application/json', 'UserAuthorization': 'invalid'}
        request = self.factory.post('/', headers=headers)
        resp = a_view(request)
        self.assertEqual(resp, {'result': 'ACCESS DENIED', 'status_code': 403})

    def test_no_token(self):
        @IsAuthorized
        def a_view(request):  # pragma: no cover
            return 'success'

        headers = {'Accept': 'application/json'}
        request = self.factory.post('/', headers=headers)
        resp = a_view(request)
        self.assertEqual(resp, {'result': 'ACCESS DENIED', 'status_code': 403})
