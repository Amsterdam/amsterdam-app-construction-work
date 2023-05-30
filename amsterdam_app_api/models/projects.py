""" Models for Projects 'kademuren' and 'bruggen'

    The 'Projects' model is used for a summary of all projects.
    The 'ProjectsDetails' model is used to get all details regarding a specific project.
    A single project from the 'Projects' model is linked to the 'ProjectDetails' via the identifier field.

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


class Projects(models.Model):
    """ Projects db model """
    project_type = models.CharField(max_length=40, blank=False, default='')
    district_id = models.IntegerField(default=-1)
    district_name = models.CharField(max_length=1000, blank=True, default='')
    title = models.CharField(max_length=1000, blank=True, default='', db_index=True)
    subtitle = models.CharField(max_length=1000, null=True, db_index=True)
    content_html = models.TextField()
    content_text = models.TextField()
    images = models.JSONField(null=True, default=list)
    identifier = models.CharField(max_length=100, blank=False, unique=True, primary_key=True)
    publication_date = models.CharField(max_length=40, blank=False)
    modification_date = models.CharField(max_length=40, blank=False)
    source_url = models.CharField(max_length=1000, blank=True, default='')
    last_seen = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True, blank=True, db_index=True)

    class Meta:
        ordering = ['title']

    def save(self, *args, **kwargs):
        self.last_seen = datetime.now()
        super(Projects, self).save(*args, **kwargs)


class ProjectDetails(models.Model):
    """ ProjectsDetails db model

        Note on 'identifier': (fields.W342) Setting unique=True on a ForeignKey has the same effect as using a
        OneToOneField. ForeignKey(unique=True) is usually better served by a OneToOneField.

        Note on 'on_delete=Models.CASCADE' When the referenced object is deleted, also delete the objects that have
        references to it (when you remove a Project for instance, you might want to delete ProjectDetails as well). SQL
        equivalent: CASCADE.
    """
    identifier = models.OneToOneField(Projects, on_delete=models.CASCADE, unique=True, primary_key=True,
                                      db_column='identifier')
    project_type = models.CharField(max_length=100, default='', blank=False, unique=False)
    body = models.JSONField(null=True, default=list)
    coordinates = models.JSONField(null=True, default=dict)
    district_id = models.IntegerField(default=-1)
    district_name = models.CharField(max_length=1000, blank=True, default='')
    images = models.JSONField(null=True, default=list)
    news = models.JSONField(null=True, default=list)
    page_id = models.IntegerField(default=-1)
    title = models.CharField(max_length=1000, blank=True, default='', db_index=True)
    subtitle = models.CharField(max_length=1000, null=True, db_index=True)
    rel_url = models.CharField(max_length=1000, blank=True, default='')
    url = models.CharField(max_length=1000, blank=True, default='')
    last_seen = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True, blank=True, db_index=True)
    contacts = models.JSONField(null=True, default=list)

    class Meta:
        ordering = ['district_id', 'title']

    def save(self, *args, **kwargs):
        self.last_seen = datetime.now()
        super(ProjectDetails, self).save(*args, **kwargs)
