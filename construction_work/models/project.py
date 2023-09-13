""" Models for Project 'kademuren' and 'bruggen'

    The 'Project' model is used for a summary of all projects.
    The 'ProjectsDetail' model is used to get all details regarding a specific project.
    A single project from the 'Project' model is linked to the 'ProjectDetail' via the identifier field.

    Json produced by Projects model:

      [{
        "identifier": string (md5 hash),
        "project_type": string,
        "district_id": integer,
        "district_name": string,
        "title": string,
        "subtitle": string,
        "content_html": string,
        "content_text": string,
        "images": [{
          "type": string,
          "sources": {
            "220px": {"url": string, "image_id": string (md5 hash), "filename": string, "description": string},
            "700px": {"url": string, "image_id": string (md5 hash), "filename": string, "description": string},
            "460px": {"url": string, "image_id": string (md5 hash), "filename": string, "description": string},
            "80px": {"url": string, "image_id": string (md5 hash), "filename": string, "description": string},
            "orig": {"url": string, "image_id": string (md5 hash), "filename": string, "description": string}
          }
        }, ...],
        "publication_date": string,
        "modification_date": string,
        "source_url": string
      }, ...]

    Json produced by ProjectDetails model:

      {
        "identifier": string (md5 hash),
        "body": {
          "contact": [{"title": string, "html": string, "text": string}, ...],
          "what": [{"title": string, "html": string, "text": string}, ...],
          "when": [{"title": string, "html": string, "text": string}, ...],
          "where": [{"title": string, "html": string, "text": string}, ...],
          "work": [{"title": string, "html": string, "text": string}, ...],
          "more-info": [{"title": string, "html": string, "text": string}, ...],
          "coordinates": {"lon": float, "lat": float}
        },
        "district_id": integer,
        "district_name": string,
        "news": [{
          "source_identifier": string,
          "identifier": string,
          "url": string
        }, ...],
        "images": [{
          "type": string,
          "sources": {
            "220px": {"url": string, "image_id": string (md5 hash), "filename": string, "description": string},
            "700px": {"url": string, "image_id": string (md5 hash), "filename": string, "description": string},
            "460px": {"url": string, "image_id": string (md5 hash), "filename": string, "description": string},
            "80px": {"url": string, "image_id": string (md5 hash), "filename": string, "description": string},
            "orig": {"url": string, "image_id": string (md5 hash), "filename": string, "description": string}
          }
        }, ...],
        "page_id": integer,
        "title": string,
        "subtitle": string,
        "rel_url": string,
        "url": string,
        "contacts": [{
            'name': None,
            'position': None,
            'email': None,
            'phone': None,
            'address': None
            }, ...
        ]
      }
"""

from datetime import datetime

from django.db import models


class Project(models.Model):
    """Projects db model"""

    project_id = models.CharField(
        max_length=100, blank=False, unique=True, primary_key=True
    )
    active = models.BooleanField(default=True, blank=True, db_index=True)
    source_url = models.CharField(max_length=1000, blank=False)

    title = models.CharField(max_length=1000, blank=True, default="", db_index=True)
    subtitle = models.CharField(max_length=1000, null=True, db_index=True)
    district_id = models.IntegerField(default=None)
    content_html = models.TextField()
    body = models.JSONField(null=True, default=list)
    coordinates = models.JSONField(null=True, default=dict)
    images = models.JSONField(null=True, default=list)

    publication_date = models.DateField(default=None)
    modification_date = models.DateField(default=None)
    last_seen = models.DateTimeField(null=True, blank=True)

    news = models.JSONField(null=True, default=list)
    # TODO: setup relation with Article model?
    # news = models.ManyToManyField(Article)

    page_id = models.IntegerField(default=None)
    url = models.CharField(max_length=1000, blank=True, default="")
    rel_url = models.CharField(max_length=1000, blank=True, default="")

    contacts = models.JSONField(null=True, default=list)

    class Meta:
        ordering = ["title"]

    def save(self, *args, **kwargs):
        self.last_seen = datetime.now()
        super(Project, self).save(*args, **kwargs)
