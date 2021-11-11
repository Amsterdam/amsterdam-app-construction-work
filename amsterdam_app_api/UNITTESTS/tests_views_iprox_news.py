import json
from django.test import Client
from django.test import TestCase
from amsterdam_app_api.UNITTESTS.mock_data import TestData
from amsterdam_app_api.models import News
from amsterdam_app_api.views.views_messages import Messages

message = Messages()


class SetUp:
    def __init__(self):
        self.data = TestData()
        self.identifiers = []
        for news in self.data.news:
            news_item = News.objects.create(**news)
            news_item.save()
            self.identifiers.append(news_item.identifier)


class TestNews(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestNews, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        self.setup = SetUp()

    def test_get_news(self):
        c = Client()
        for i in range(0, len(self.setup.identifiers)):
            response = c.get('/api/v1/project/news?id={identifier}'.format(identifier=self.setup.identifiers[i]))
            result = json.loads(response.content)

            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(result, {'status': True, 'result': self.data.news[i]})

    def test_invalid_query(self):
        c = Client()
        response = c.get('/api/v1/project/news')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(result, {'status': False, 'result': message.invalid_query})

    def test_no_record(self):
        c = Client()
        response = c.get('/api/v1/project/news?id=unknown')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertDictEqual(result, {'status': False, 'result': message.no_record_found})

    def test_method_not_allowed(self):
        c = Client()
        response = c.post('/api/v1/project/news')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertDictEqual(result, {'detail': 'Method "POST" not allowed.'})


class TestNewsItemsByProjectId(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestNewsItemsByProjectId, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        SetUp()

    def test_get_all_news(self):
        c = Client()
        response = c.get('/api/v1/project/news_by_project_id')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, {'status': True, 'result': self.data.news[::-1]})

    def test_get_news_by_project_identifier_exists(self):
        c = Client()
        response = c.get('/api/v1/project/news_by_project_id', {'project-identifier': '0000000000'})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, {'status': True, 'result': [self.data.news[0]]})

    def test_get_news_sorted_by_publication_date_desc(self):
        c = Client()
        response = c.get('/api/v1/project/news_by_project_id', {'sort-by': 'publication_date'})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, {'status': True, 'result': self.data.news[::-1]})

    def test_get_news_sorted_by_publication_date_asc(self):
        c = Client()
        response = c.get('/api/v1/project/news_by_project_id', {'sort-by': 'publication_date', 'sort-order': 'asc'})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, {'status': True, 'result': self.data.news})

    def test_get_news_by_project_identifier_does_not_exists(self):
        c = Client()
        response = c.get('/api/v1/project/news_by_project_id', {'project-identifier': 'does not exist'})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, {'status': True, 'result': []})

    def test_method_not_allowed(self):
        c = Client()
        response = c.post('/api/v1/project/news_by_project_id')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertDictEqual(result, {'detail': 'Method "POST" not allowed.'})
