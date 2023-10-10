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
from django.utils import timezone

DISTRICTS = {
    5398: "Centrum",
    5520: "Nieuw-West",
    5565: "Noord",
    5399: "Oost",
    7196: "Weesp",
    5397: "West",
    5396: "Zuid",
    5393: "Zuidoost",
}


class Project(models.Model):
    """Projects db model"""

    project_id = models.IntegerField(blank=False, unique=True, null=False)

    active = models.BooleanField(default=True, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)

    title = models.CharField(max_length=1000, blank=True, null=True, default="", db_index=True)
    subtitle = models.CharField(max_length=1000, blank=True, null=True, db_index=True)
    sections = models.JSONField(blank=True, null=True, default=dict)
    contacts = models.JSONField(blank=True, null=True, default=list)
    timeline = models.JSONField(blank=True, null=True, default=dict)
    image = models.JSONField(blank=True, null=True, default=dict)
    images = models.JSONField(blank=True, null=True, default=list)
    url = models.URLField(max_length=2048, blank=True, null=True)
    creation_date = models.DateTimeField(default=timezone.now)  # If no date is provided use the current date
    modification_date = models.DateTimeField(default=timezone.now)  # If no date is provided use the current date
    publication_date = models.DateTimeField(default=None, null=True)
    expiration_date = models.DateTimeField(default=None, null=True)

    class Meta:
        ordering = ["title"]

    def save(self, *args, **kwargs):
        self.last_seen = datetime.now()
        super(Project, self).save(*args, **kwargs)
