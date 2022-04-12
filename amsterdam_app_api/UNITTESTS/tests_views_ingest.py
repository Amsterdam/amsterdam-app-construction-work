import os
from unittest.mock import patch
from django.test import Client
from django.test import TestCase
from amsterdam_app_api.GarbageCollector.GarbageCollector import GarbageCollector
from amsterdam_app_api.GenericFunctions.AESCipher import AESCipher
from amsterdam_app_api.UNITTESTS.mock_data import TestData
from amsterdam_app_api.models import Assets
from amsterdam_app_api.models import Image
from amsterdam_app_api.models import CityOffice, CityOffices, CityContact
from amsterdam_app_api.models import Projects, ProjectDetails
from amsterdam_app_api.models import News
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
        token = AESCipher('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', os.getenv('AES_SECRET')).encrypt()
        self.header = {'HTTP_INGESTAUTHORIZATION': token}
        self.content_type = "application/json"
        self.client = Client()

    def test_image_exist(self):
        c = Client()
        response = c.get('/api/v1/ingest/image?identifier=0000000000', headers=self.header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'status': True, 'result': {'identifier': '0000000000'}})

    def test_image_not_exist(self):
        c = Client()
        response = c.get('/api/v1/ingest/image?identifier=bogus', headers=self.header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'status': False, 'result': None})

    def test_image_ingest_valid(self):
        data = {
            'identifier': '0000000000',
            'size': 'orig',
            'url': 'mock',
            'filename': 'mock',
            'description': 'mock',
            'mime_type': 'mock',
            'data': 'MHgwMA=='
        }

        result = self.client.post('/api/v1/ingest/image', data=data, headers=self.header, content_type='application/json')

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, {'status': True, 'result': True})

    def test_image_ingest_invalid(self):
        data = {
            'identifier': '0000000000',
            'size': 'orig',
            'url': 'mock',
            'filename': 'mock',
            'description': 'mock',
            'mime_type': 'mock',
            'data': 'BOGUS'
        }

        result = self.client.post('/api/v1/ingest/image', data=data, headers=self.header, content_type='application/json')

        self.assertEqual(result.status_code, 500)
        self.assertEqual(result.data, {'status': False, 'result': 'Invalid base64-encoded string: number of data characters (5) cannot be 1 more than a multiple of 4'})

    def test_asset_exist(self):
        c = Client()
        response = c.get('/api/v1/ingest/asset?identifier=0000000000', headers=self.header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'status': True, 'result': {'identifier': '0000000000'}})

    def test_asset_not_exist(self):
        c = Client()
        response = c.get('/api/v1/ingest/asset?identifier=bogus', headers=self.header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'status': False, 'result': None})

    def test_asset_ingest_valid(self):
        data = {
            'identifier': '0000000000',
            'url': 'mock',
            'mime_type': 'mock',
            'data': 'MHgwMA=='
        }

        result = self.client.post('/api/v1/ingest/asset', data=data, headers=self.header, content_type='application/json')

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, {'status': True, 'result': True})

    def test_asset_ingest_invalid(self):
        data = {
            'identifier': '0000000000',
            'url': 'mock',
            'mime_type': 'mock',
            'data': 'BOGUS'
        }

        result = self.client.post('/api/v1/ingest/asset', data=data, headers=self.header, content_type='application/json')

        self.assertEqual(result.status_code, 500)
        self.assertEqual(result.data, {'status': False, 'result': 'Invalid base64-encoded string: number of data characters (5) cannot be 1 more than a multiple of 4'})

    def test_city_office_valid(self):
        data = {
            "identifier": "0000000000",
            "title": "mock",
            "contact": {
                "Bellen": {
                    "html": "<div>mock</div>",
                    "text": "mock"
                },
                "Mailen": {
                    "html": "<div>mock</div>",
                    "text": "mock"
                },
                "Openingstijden": {
                    "html": "<div>mock</div>",
                    "text": "mock"
                }
            },
            "images": {
                "type": "",
                "sources": {
                    "orig": {
                        "url": "mock.jpg",
                        "filename": "mock.jpg",
                        "image_id": "00000000",
                        "description": "mock"
                    }
               }
            },
            "info": {
                "html": "<div>mock</div>",
                "text": "mock"
            },
            "address": {
                "html": "<div>mock</div>",
                "text": "mock"
            }
        }

        result = self.client.post('/api/v1/ingest/cityoffice', data=data, headers=self.header, content_type='application/json')
        db_objects = list(CityOffice.objects.filter(pk='0000000000').all())

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, {'status': True, 'result': True})
        self.assertEqual(len(db_objects), 1)

        # Test update same record
        result = self.client.post('/api/v1/ingest/cityoffice', data=data, headers=self.header, content_type='application/json')
        db_objects = list(CityOffice.objects.filter(pk='0000000000').all())

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, {'status': True, 'result': True})
        self.assertEqual(len(db_objects), 1)

    def test_city_office_not_unique(self):
        data = {'title': 'mock'}

        result = self.client.post('/api/v1/ingest/cityoffice', data=data, headers=self.header, content_type='application/json')
        db_objects = list(CityOffice.objects.all())

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, {'status': True, 'result': True})
        self.assertEqual(len(db_objects), 1)

        # Should fail, not unique
        result = self.client.post('/api/v1/ingest/cityoffice', data=data, headers=self.header, content_type='application/json')
        db_objects = list(CityOffice.objects.all())

        self.assertEqual(result.status_code, 500)
        self.assertEqual(result.data, {'status': False, 'result': 'duplicate key value violates unique constraint "amsterdam_app_api_cityoffice_pkey"\nDETAIL:  Key (identifier)=() already exists.\n'})
        self.assertEqual(len(db_objects), 1)

    def test_city_offices_valid(self):
        data = [{"url": "https://mock", "title": "mock", "identifier": "00000000"}]

        result = self.client.post('/api/v1/ingest/cityoffices', data=data, headers=self.header, content_type='application/json')
        db_objects = list(CityOffices.objects.all())

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, {'status': True, 'result': True})
        self.assertEqual(len(db_objects), 1)

        # 'Extra' call should still yield a single db record
        data = [{"url": "https://mock", "title": "mock", "identifier": "00000000"},
                {"url": "https://mock2", "title": "mock1", "identifier": "00000001"}]

        result = self.client.post('/api/v1/ingest/cityoffices', data=data, headers=self.header, content_type='application/json')
        db_objects = list(CityOffices.objects.all())

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, {'status': True, 'result': True})
        self.assertEqual(len(db_objects), 1)

    def test_city_offices_invalid(self):
        data = 'bogus'

        result = self.client.post('/api/v1/ingest/cityoffices', data=data, headers=self.header, content_type='application/json')
        db_objects = list(CityOffices.objects.all())

        self.assertEqual(result.status_code, 500)
        self.assertEqual(result.data, {'status': False, 'result': 'Caught error ingesting city offices'})
        self.assertEqual(len(db_objects), 0)

    def test_city_contacts_valid(self):
        data = [{"html": "<div>mock</div>", "text": "mock", "title": "mock"}]

        result = self.client.post('/api/v1/ingest/citycontact', data=data, headers=self.header, content_type='application/json')
        db_objects = list(CityContact.objects.all())

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, {'status': True, 'result': True})
        self.assertEqual(len(db_objects), 1)

    def test_city_contacts_invalid(self):
        data = 'bogus'

        result = self.client.post('/api/v1/ingest/citycontact', data=data, headers=self.header, content_type='application/json')
        db_objects = list(CityContact.objects.all())

        self.assertEqual(result.status_code, 500)
        self.assertEqual(result.data, {'status': False, 'result': 'Caught error ingesting city contacts'})
        self.assertEqual(len(db_objects), 0)

    def test_project_valid(self):
        data = {
            "identifier": "acf4d3879bbba27bf66fedb792549163",
            "project_type": "kade",
            "body": {
                "what": [{"html": "<div>mock</div>", "text": "mock", "title": "mock"}],
                "when": [{"html": "<div>mock</div>", "text": "mock", "title": "mock"}],
                "work": [{"html": "<div>mock</div>", "text": "mock", "title": "mock"}],
                "where": [{"html": "<div>mock</div>", "text": "mock", "title": "mock"}],
                "notice": [{"html": "<div>mock</div>", "text": "mock", "title": "mock"}],
                "contact": [{"html": "<div>mock</div>", "text": "mock", "title": "mock"}],
                "timeline": {},
                "more-info": [{"html": "<div>mock</div>", "text": "mock", "title": "mock"}],
            },
            "coordinates": {"lat": 0.0, "lon": 0.0},
            "district_id": 1,
            "district_name": "mockl",
            "images": [{
                "type": "",
                "sources": {
                    "orig": {
                        "url": "https://mock.jpg",
                        "filename": "mock.jpg",
                        "image_id": "00000000",
                        "description": "mock"
                    }
                }
            }],
            "news": [{"url": "https://mock", "identifier": "mock", "project_identifier": "00000000"}],
            "page_id": 957308,
            "title": "mock",
            "subtitle": "mock",
            "rel_url": "mock",
            "url": "https://mock"
        }

        result = self.client.post('/api/v1/ingest/project', data=data, headers=self.header, content_type='application/json')
        db_objects = list(ProjectDetails.objects.all())

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, {'status': True, 'result': True})
        self.assertEqual(len(db_objects), 1)

        # Update record
        result = self.client.post('/api/v1/ingest/project', data=data, headers=self.header, content_type='application/json')
        db_objects = list(ProjectDetails.objects.all())

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, {'status': True, 'result': True})
        self.assertEqual(len(db_objects), 1)

    def test_project_invalid(self):
        data = {'bogus': 'bogus'}

        result = self.client.post('/api/v1/ingest/project', data=data, headers=self.header, content_type='application/json')
        db_objects = list(ProjectDetails.objects.all())

        self.assertEqual(result.status_code, 500)
        self.assertEqual(result.data, {'status': False, 'result': "ProjectDetails() got an unexpected keyword argument 'bogus'"})
        self.assertEqual(len(db_objects), 0)

    def test_projects_get(self):
        test_data = TestData()
        project_object = Projects(**test_data.projects[0])
        project_object.save()

        result = self.client.get('/api/v1/ingest/projects?identifier=0000000000', headers=self.header, content_type='application/json')
        self.assertEqual(result.status_code, 200)
        assert isinstance(result.data['result'], dict)

        result = self.client.get('/api/v1/ingest/projects?identifier=0000000001', headers=self.header, content_type='application/json')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, {'status': True, 'result': None})

    def test_projects_post_valid(self):
        test_data = TestData()
        result = self.client.post('/api/v1/ingest/projects', data=test_data.projects[0], headers=self.header, content_type='application/json')
        project_objects = list(Projects.objects.all())

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, {'status': True, 'result': True})
        self.assertEqual(len(project_objects), 1)

        # Update record
        result = self.client.post('/api/v1/ingest/projects', data=test_data.projects[0], headers=self.header, content_type='application/json')
        project_objects = list(Projects.objects.all())

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, {'status': True, 'result': True})
        self.assertEqual(len(project_objects), 1)

    def test_projects_post_invalid(self):
        data = {'bogus': 'bogus'}

        result = self.client.post('/api/v1/ingest/projects', data=data, headers=self.header, content_type='application/json')
        project_objects = list(Projects.objects.all())

        self.assertEqual(result.status_code, 500)
        self.assertEqual(result.data, {'status': False, 'result': "Projects() got an unexpected keyword argument 'bogus'"})
        self.assertEqual(len(project_objects), 0)

    def test_projects_delete_valid(self):
        test_data = TestData()
        project_object = Projects(**test_data.projects[0])
        project_object.save()

        data = {'identifier': '0000000000'}
        result = self.client.delete('/api/v1/ingest/projects', data=data, headers=self.header, content_type='application/json')
        project_objects = list(Projects.objects.all())

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, {'status': True, 'result': True})
        self.assertEqual(len(project_objects), 0)

        data = 'bogus'
        result = self.client.delete('/api/v1/ingest/projects', data=data, headers=self.header, content_type='application/json')

        self.assertEqual(result.status_code, 500)
        self.assertEqual(result.data, {'status': False, 'result': 'JSON parse error - Expecting value: line 1 column 1 (char 0)'})

    def test_news_valid(self):
        test_data = TestData()

        result = self.client.post('/api/v1/ingest/news', data=test_data.news[0], headers=self.header, content_type='application/json')
        news_objects = list(News.objects.all())

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, {'status': True, 'result': True})
        self.assertEqual(len(news_objects), 1)

        # Update existing record
        result = self.client.post('/api/v1/ingest/news', data=test_data.news[0], headers=self.header, content_type='application/json')
        news_objects = list(News.objects.all())

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, {'status': True, 'result': True})
        self.assertEqual(len(news_objects), 1)

    def test_news_invalid(self):
        data = 'bogus'

        result = self.client.post('/api/v1/ingest/news', data=data, headers=self.header, content_type='application/json')
        news_objects = list(News.objects.all())

        self.assertEqual(result.status_code, 500)
        self.assertEqual(result.data, {'status': False, 'result': 'JSON parse error - Expecting value: line 1 column 1 (char 0)'})
        self.assertEqual(len(news_objects), 0)


    def test_garbage_collection(self):
        def mock(*args, **kwargs):
            pass

        with patch.object(GarbageCollector, 'collect_iprox', side_effect=mock):
            result = self.client.get('/api/v1/ingest/garbagecollector?project_type=kade', headers=self.header, content_type='application/json')

            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.data, {'status': True, 'result': 'Garbage collection done'})
