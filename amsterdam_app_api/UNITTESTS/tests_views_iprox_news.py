""" UNITTESTS """

import json
import os
from django.test import Client
from django.test import TestCase
from amsterdam_app_api.UNITTESTS.mock_data import TestData
from amsterdam_app_api.models import News, WarningMessages, Projects, ProjectManager
from amsterdam_app_api.views.views_messages import Messages
from amsterdam_app_api.GenericFunctions.AESCipher import AESCipher

message = Messages()


class SetUp:
    """ Setup test db """
    def __init__(self):
        self.data = TestData()
        self.identifiers = []

        Projects.objects.all().delete()
        for project in self.data.projects:
            Projects.objects.create(**project)

        for news in self.data.news:
            news['project_identifier'] = Projects.objects.filter(pk=news['project_identifier']).first()
            news_item = News.objects.create(**news)
            news_item.save()
            self.identifiers.append(news_item.identifier)

        WarningMessages.objects.all().delete()

        ProjectManager.objects.all().delete()
        for project_manager in self.data.project_manager:
            ProjectManager.objects.create(**project_manager)

        self.url = '/api/v1/project/warning'
        self.client = Client()
        self.token = AESCipher('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', os.getenv('AES_SECRET')).encrypt()
        self.headers = {"UserAuthorization": self.token}
        self.content_type = "application/json"
        for title in ['title0', 'title1']:
            data = {
                'title': title,
                'project_identifier': '0000000000',
                'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
                'body': 'Body text'
            }
        self.client.post(self.url, json.dumps(data), headers=self.headers, content_type=self.content_type)


class TestArticles(TestCase):
    """ UNITTESTS """
    def __init__(self, *args, **kwargs):
        super(TestArticles, self).__init__(*args, **kwargs)
        self.data = TestData()
        self.url = '/api/v1/articles'
        self.client = Client()

    def setUp(self):
        """ Setup test db """
        self.setup = SetUp()

    def test_get_all(self):
        """ Test get all articles """
        result = self.client.get(self.url)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.data['result']), 3)

    def test_get_limit_one(self):
        """ Test limiting the result to one article """
        result = self.client.get(self.url, {'limit': 1})
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.data['result']), 1)

    def test_get_limit_project_ids(self):
        """ Test limiting amount of projects """
        result = self.client.get(self.url, {'project-ids': '0000000000,0000000001', 'sort-order': 'asc', 'limit': 4})

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.data['result']), 3)

    def test_get_limit_error(self):
        """ Test false limit query """
        result = self.client.get(self.url, {'project-ids': '0000000000,0000000001',
                                            'sort-order': 'asc', 'limit': 'error'})

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.data['result']), 3)


class TestNews(TestCase):
    """ UNITTEST """
    def __init__(self, *args, **kwargs):
        super(TestNews, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        """ Setup test db """
        self.setup = SetUp()

    def test_get_news(self):
        """ Test get news """
        c = Client()
        for i in range(0, len(self.setup.identifiers)):
            response = c.get('/api/v1/project/news?id={identifier}'.format(identifier=self.setup.identifiers[i]))
            result = json.loads(response.content)
            self.data.news[i]['last_seen'] = result['result']['last_seen']
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(result, {'status': True, 'result': self.data.news[i]})

    def test_invalid_query(self):
        """ Test invalid news query """
        c = Client()
        response = c.get('/api/v1/project/news')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(result, {'status': False, 'result': message.invalid_query})

    def test_no_record(self):
        """ Test for 404 result """
        c = Client()
        response = c.get('/api/v1/project/news?id=unknown')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertDictEqual(result, {'status': False, 'result': message.no_record_found})

    def test_method_not_allowed(self):
        """ Test invalid http method """
        c = Client()
        response = c.post('/api/v1/project/news')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertDictEqual(result, {'detail': 'Method "POST" not allowed.'})


class TestNewsItemsByProjectId(TestCase):
    """ UNITTEST """
    def __init__(self, *args, **kwargs):
        super(TestNewsItemsByProjectId, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        """ Setup test db """
        SetUp()

    def test_get_all_news(self):
        """ Test get all news items """
        c = Client()
        response = c.get('/api/v1/project/news_by_project_id')
        results = json.loads(response.content)
        for result in results['result']:
            for i in range(0, len(self.data.news), 1):
                if result['identifier'] == self.data.news[i]['identifier']:
                    self.data.news[i]['last_seen'] = result['last_seen']

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(results, {'status': True, 'result': self.data.news[::-1]})

    def test_get_news_by_project_identifier_exists(self):
        """ Test get news by existing identifier """
        c = Client()
        response = c.get('/api/v1/project/news_by_project_id', {'project-identifier': '0000000000'})
        result = json.loads(response.content)
        self.data.news[0]['last_seen'] = result['result'][0]['last_seen']
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, {'status': True, 'result': [self.data.news[0]]})

    def test_get_news_sorted_by_publication_date_desc(self):
        """ Get news and sort descending by publication date """
        c = Client()
        response = c.get('/api/v1/project/news_by_project_id', {'sort-by': 'publication_date'})
        results = json.loads(response.content)
        for result in results['result']:
            for i in range(0, len(self.data.news), 1):
                if result['identifier'] == self.data.news[i]['identifier']:
                    self.data.news[i]['last_seen'] = result['last_seen']

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(results, {'status': True, 'result': self.data.news[::-1]})

    def test_get_news_sorted_by_publication_date_asc(self):
        """ Get news and sort ascending by publication date """
        c = Client()
        response = c.get('/api/v1/project/news_by_project_id', {'sort-by': 'publication_date', 'sort-order': 'asc'})
        results = json.loads(response.content)
        for result in results['result']:
            for i in range(0, len(self.data.news), 1):
                if result['identifier'] == self.data.news[i]['identifier']:
                    self.data.news[i]['last_seen'] = result['last_seen']

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(results, {'status': True, 'result': self.data.news})

    def test_get_news_by_project_identifier_does_not_exists(self):
        """ Get news with invalid identifier """
        c = Client()
        response = c.get('/api/v1/project/news_by_project_id', {'project-identifier': 'does not exist'})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, {'status': True, 'result': []})

    def test_method_not_allowed(self):
        """ Test invalid http method """
        c = Client()
        response = c.post('/api/v1/project/news_by_project_id')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertDictEqual(result, {'detail': 'Method "POST" not allowed.'})
