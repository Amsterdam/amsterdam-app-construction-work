import json
from django.test import Client
from django.test import TestCase
from unittest.mock import patch
from amsterdam_app_api.api_messages import Messages

messages = Messages()


def mocked_get_set_projects(*args):
    return {'status': True, 'result': 'mock result'}


class TestApiIngest(TestCase):
    def test_invalid_query(self):
        c = Client()
        response = c.get('/api/v1/ingest')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(result, {'status': False, 'result': messages.invalid_query})

    @patch('amsterdam_app_api.FetchData.IproxIngestion.get_set_projects', mocked_get_set_projects)
    def test_ingestion(self):
        c = Client()
        response = c.get('/api/v1/ingest', {'project-type': 'brug'})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, {"status": True, "result": {"status": True, "result": "mock result"}})
