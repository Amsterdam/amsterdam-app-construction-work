""" UNITTEST TEST DATA """
# pylint: disable=line-too-long, too-many-lines
import datetime


class TestData:
    """Unittest test data"""

    def __init__(self):
        self.assets = [
            {
                "identifier": "0000000000",
                "url": "https://localhost/test0.pdf",
                "mime_type": "application/pdf",
                "data": b"",
            },
            {
                "identifier": "0000000001",
                "url": "https://localhost/test1.pdf",
                "mime_type": "application/pdf",
                "data": b"",
            },
        ]

        self.images = [
            {
                "data": b"",
                "description": "square image",
                "width": 10,
                "height": 10,
                "aspect_ratio": 1,
                "coordinates": {"lat": 0.0, "lon": 0.0},
                "mime_type": "image/jpg",
            },
            {
                "data": b"",
                "description": "landscape image",
                "width": 100,
                "height": 10,
                "aspect_ratio": 0.1,
                "coordinates": {"lat": 1.0, "lon": 1.0},
                "mime_type": "image/jpg",
            },
            {
                "data": b"",
                "description": "portrait image",
                "width": 10,
                "height": 100,
                "aspect_ratio": 10,
                "coordinates": {"lat": 2.0, "lon": 2.0},
                "mime_type": "image/jpg",
            },
        ]

        self.projects = [
            {
                "foreign_id": 2048,
                "active": True,
                "title": "title first project",
                "subtitle": "subtitle first project",
                "coordinates": {"lat": 1.0, "lon": 1.0},
                "sections": {},
                "contacts": {},
                "timeline": {},
                "image": {},
                "images": [],
                "url": "https://www.amsterdam.nl/foobar",
                "creation_date": "2023-01-01T00:00:00+00:00",
                "modification_date": "2023-01-20T00:00:00+00:00",
                "publication_date": "2023-01-01T00:00:00+00:00",
                "expiration_date": "2023-02-01T00:00:00+00:00",
            },
            {
                "foreign_id": 4096,
                "active": True,
                "title": "title second project",
                "subtitle": "subtitle second project",
                "coordinates": None,
                "sections": {},
                "contacts": {},
                "timeline": {},
                "image": {},
                "images": [],
                "url": "https://www.amsterdam.nl/fizzbuzz",
                "creation_date": "2023-01-01T00:00:00+00:00",
                "modification_date": "2023-01-20T00:00:00+00:00",
                "publication_date": "2023-01-01T00:00:00+00:00",
                "expiration_date": "2023-02-01T00:00:00+00:00",
            },
        ]

        self.articles = [
            {
                "foreign_id": 128,
                "active": True,
                "last_seen": datetime.datetime.strptime(
                    "2023-01-01T00:00:00", "%Y-%d-%mT%H:%M:%S"
                ),
                "title": "title of first article",
                "intro": "intro for first article",
                "body": {
                    "content": {"html": "html content", "text": "text content"},
                    "preface": {"html": "html content", "text": "text content"},
                    "summary": {"html": "html content", "text": "text content"},
                },
                "image": {},
                "type": "work",
                "url": "https://www.amsterdam.nl/foobar-article",
                "creation_date": "2023-01-01T00:00:00+00:00",
                "modification_date": "2023-01-20T00:00:00+00:00",
                "publication_date": "2023-01-01T00:00:00+00:00",
                "expiration_date": "2023-02-01T00:00:00+00:00",
            },
            {
                "foreign_id": 256,
                "active": True,
                "last_seen": datetime.datetime.strptime(
                    "2023-01-01T12:00:00", "%Y-%d-%mT%H:%M:%S"
                ),
                "title": "title of second article",
                "intro": "intro for second article",
                "body": {
                    "content": {"html": "html content", "text": "text content"},
                    "preface": {"html": "html content", "text": "text content"},
                    "summary": {"html": "html content", "text": "text content"},
                },
                "image": {},
                "type": "work",
                "url": "https://www.amsterdam.nl/fizzbuzz-article",
                "creation_date": "2023-01-01T00:00:00+00:00",
                "modification_date": "2023-01-20T00:00:00+00:00",
                "publication_date": "2023-01-01T00:00:00+00:00",
                "expiration_date": "2023-02-01T00:00:00+00:00",
            },
        ]

        self.ingest_projects = [
            {
                "foreign_id": 2048,
                "active": True,
                "title": "title first project: subtitle first project",
                "coordinates": {"lat": -1.0, "lon": 1.0},
                "sections": {},
                "contacts": {},
                "timeline": {},
                "image": {},
                "images": [],
                "url": "https://www.amsterdam.nl/foobar",
                "created": "2021-07-14 10:46:00.000000 +00:00",
                "modified": "2023-06-01 11:08:00.000000 +00:00",
                "publicationDate": "2023-04-25 15:19:00.000000 +00:00",
                "expirationDate": "2024-04-25 15:19:00.000000 +00:00",
            },
            {
                "foreign_id": 4096,
                "active": True,
                "title": "title second project: subtitle second project",
                "coordinates": None,
                "sections": {},
                "contacts": {},
                "timeline": {},
                "image": {},
                "images": [],
                "url": "https://www.amsterdam.nl/fizzbuzz",
                "created": "2021-07-14 10:46:00.000000 +00:00",
                "modified": "2023-06-01 11:08:00.000000 +00:00",
                "publicationDate": "2023-04-25 15:19:00.000000 +00:00",
                "expirationDate": "2024-04-25 15:19:00.000000 +00:00",
            },
        ]

        self.ingest_articles = [
            {
                "foreign_id": 128,
                "title": "New title of first article",
                "intro": "New intro for first article",
                "body": "New body for first article",
                "image": {},
                "projectIds": [2048],
                "type": "work",
                "url": "https://www.amsterdam.nl/foobar-article",
                "created": "2023-01-01T00:00:00+00:00",
                "modified": "2023-01-20T00:00:00+00:00",
                "publicationDate": "2023-01-01T00:00:00+00:00",
                "expirationDate": "2023-02-01T00:00:00+00:00",
            },
            {
                "foreign_id": 256,
                "title": "title of second article",
                "intro": "intro for second article",
                "body": "body for second article",
                "image": {},
                "projectIds": [4096],
                "type": "work",
                "url": "https://www.amsterdam.nl/fizzbuzz-article",
                "created": "2023-01-01T00:00:00+00:00",
                "modified": "2023-01-20T00:00:00+00:00",
                "publicationDate": "2023-01-01T00:00:00+00:00",
                "expirationDate": "2023-02-01T00:00:00+00:00",
            },
        ]

        self.image_download_jobs = [
            {
                "url": "valid_url",
                "image_id": "0",
                "filename": "mock0.jpg",
                "description": "",
                "size": "orig",
            },
            {
                "url": "invalid_url",
                "image_id": "1",
                "filename": "mock1.jpg",
                "description": "",
                "size": "orig",
            },
        ]

        self.project_managers = [
            {
                "manager_key": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                "email": "mock0@amsterdam.nl",
            },
            {
                "manager_key": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
                "email": "mock1@amsterdam.nl",
            },
        ]

        self.devices = [
            {
                "device_id": "foobar_device1",
                "firebase_token": "foobar_token1",
                "os": "ios",
            },
            {
                "device_id": "foobar_device2",
                "firebase_token": "foobar_token2",
                "os": "android",
            },
        ]

        self.followed_projects = [
            {"deviceid": "0", "projectid": "0000000000"},
            {"deviceid": "0", "projectid": "0000000001"},
            {"deviceid": "1", "projectid": "0000000000"},
        ]

        self.warning_message = {
            "title": "warning message title",
            "body": "warning message body",
            "publication_date": "2023-10-10",
            "modification_date": "2023-10-11",
        }
