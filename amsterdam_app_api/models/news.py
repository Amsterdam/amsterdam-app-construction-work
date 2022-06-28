from django.db import models


""" Models for news about Projects 'kademuren' and 'bruggen'

    The News model is used to store the news items belonging to projects 'kademuren' or 'bruggen'.

    Json produced by News model:

    {
        "source_identifier": "string",
        "publication_date": "string",
        "modification_date": "string",
        "images": {
            "banner": {"url": "string", "identifier": "string"},
            "other": [{"url": "string", "identifier": "string"}, ...]
        },
        "title": "string",
        "body": {
            "summary": {"html": string, "text": string},
            "preface": {"html": string, "text": string},
            "content": {"html": string, "text": string}
        }
        "url": "string"
    }


"""


class News(models.Model):
    identifier = models.CharField(max_length=100, blank=False, unique=True, primary_key=True)
    project_identifier = models.CharField(max_length=100, blank=False, unique=False)
    project_type = models.CharField(max_length=100, default='', blank=False, unique=False)
    url = models.CharField(max_length=1000, blank=True, default='')
    title = models.CharField(max_length=1000, blank=True, default='')
    publication_date = models.CharField(max_length=10, blank=True, default='')
    body = models.JSONField(null=True, default=dict)
    images = models.JSONField(null=True, default=list)
    assets = models.JSONField(null=True, default=list)
    last_seen = models.DateTimeField(auto_now=True, blank=True)
    active = models.BooleanField(default=True, blank=True)
