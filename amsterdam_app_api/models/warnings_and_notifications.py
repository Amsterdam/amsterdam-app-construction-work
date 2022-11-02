import datetime
import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField
from .project_managers import ProjectManager
from .news import News

""" Model for Warning messages

    Notes: 
    The project manager writes and article. We’re only sending the text content to start
    with, to not burden the request with lots of image data. We expect a warning identifier in the
    response, with which we can relate the notification content and the images we’re sending next.

    Post body by API:

    {
        "title": "title",
        "body": {
          "preface": "short text",
          "content": "longer text"
        },
        "project_id": "8ac7ed07fc76a0812b3afbd5f0182aeb",
        "project_manager_id": "UUIDv4"
        "publication_date": DateTimefield,
        "modification_date": DateTimefield
    }

    Produced json:

    {
        "identifier": "UUIDv4",
        "title": "Title",
        "body": "text",
        "project_identifier": "8ac7ed07fc76a0812b3afbd5f0182aeb",
        "project_manager_id": "UUIDv4",
        "publication_date": DateTimefield,
        "modification_date": DateTimefield,
        "author_email": "p.puk@amsterdam.nl"
        "images": [{
            "type": "header",
            "sources": {
                "orig": {
                    "url": None,
                    "filename": None,
                    "image_id": "af53bcc112bed15d233befd67077ab3a",
                    "description": "description text"
                }
            }
        }, ...]
    }
"""


class WarningMessages(models.Model):
    identifier = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=1000, unique=False)
    body = models.CharField(max_length=1000, unique=False)
    project_identifier = models.CharField(max_length=100, blank=False, unique=False)
    project_manager_id = models.CharField(max_length=100, blank=False, unique=False)
    images = ArrayField(models.JSONField(null=True, default=dict), blank=False)
    publication_date = models.DateTimeField(auto_now_add=True, blank=True)
    modification_date = models.DateTimeField(auto_now_add=True, blank=True)
    author_email = models.EmailField(null=True, blank=True)

    def save(self, *args, **kwargs):
        project_manager = ProjectManager.objects.filter(pk=self.project_manager_id).first()
        self.author_email = project_manager.email if project_manager is not None else 'redactieprojecten@amsterdam.nl'
        self.modification_date = datetime.datetime.now()
        super(WarningMessages, self).save(*args, **kwargs)


class Notification(models.Model):
    identifier = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=1000, unique=False)
    body = models.CharField(max_length=1000, unique=False)
    project_identifier = models.CharField(null=True, max_length=100, unique=False)
    news_identifier = models.CharField(null=True, max_length=100, unique=False)
    warning_identifier = models.UUIDField(null=True, unique=False)
    publication_date = models.DateTimeField(auto_now_add=True, blank=True)

    def save(self, *args, **kwargs):
        if self.warning_identifier is not None:
            message = WarningMessages.objects.filter(pk=self.warning_identifier).first()
        else:
            message = News.objects.filter(pk=self.news_identifier).first()

        if message is not None:
            self.project_identifier = message.project_identifier
            super(Notification, self).save(*args, **kwargs)
