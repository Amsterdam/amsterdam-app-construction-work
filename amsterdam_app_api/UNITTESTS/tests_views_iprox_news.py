import json
from django.test import Client
from django.test import TestCase
from amsterdam_app_api.UNITTESTS.mock_data import TestData
from amsterdam_app_api.models import News


class SetUp:
    def __init__(self):
        self.data = TestData()

        for news in self.data.news:
            News.objects.create(**news)


class TestNewsImage(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestNewsImage, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        SetUp()

    def test_get_all_news(self):
        c = Client()
        response = c.get('/api/v1/project/news')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, {'status': True, 'result': self.data.news[::-1]})

    def test_get_news_by_project_identifier_exists(self):
        c = Client()
        response = c.get('/api/v1/project/news', {'project-identifier': '0000000000'})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, {'status': True, 'result': [self.data.news[0]]})

    def test_get_news_sorted_by_publication_date_desc(self):
        c = Client()
        response = c.get('/api/v1/project/news', {'sort-by': 'publication_date'})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, {'status': True, 'result': self.data.news[::-1]})

    def test_get_news_sorted_by_publication_date_asc(self):
        c = Client()
        response = c.get('/api/v1/project/news', {'sort-by': 'publication_date', 'sort-order': 'asc'})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, {'status': True, 'result': self.data.news})

    def test_get_news_by_project_identifier_does_not_exists(self):
        c = Client()
        response = c.get('/api/v1/project/news', {'project-identifier': 'does not exist'})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, {'status': True, 'result': []})

    def test_method_not_allowed(self):
        c = Client()
        response = c.post('/api/v1/project/news')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertDictEqual(result, {'detail': 'Method "POST" not allowed.'})
