from django.db import models


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


class Projects(models.Model):
    project_type = models.CharField(max_length=40, blank=False, default='')
    district_id = models.IntegerField(default=-1)
    district_name = models.CharField(max_length=1000, blank=True, default='')
    title = models.CharField(max_length=1000, blank=True, default='')
    subtitle = models.CharField(max_length=1000, null=True)
    content_html = models.TextField()
    content_text = models.TextField()
    images = models.JSONField(null=True, default=list)
    identifier = models.CharField(max_length=100, blank=False, unique=True, primary_key=True)
    publication_date = models.CharField(max_length=40, blank=False)
    modification_date = models.CharField(max_length=40, blank=False)
    source_url = models.CharField(max_length=1000, blank=True, default='')
    last_seen = models.DateTimeField(auto_now=True, blank=True)
    active = models.BooleanField(default=True, blank=True)

    class Meta:
        ordering = ['title']


class ProjectDetails(models.Model):
    identifier = models.CharField(max_length=100, blank=False, unique=True, primary_key=True)
    project_type = models.CharField(max_length=100, default='', blank=False, unique=False)
    body = models.JSONField(null=True, default=list)
    coordinates = models.JSONField(null=True, default=dict)
    district_id = models.IntegerField(default=-1)
    district_name = models.CharField(max_length=1000, blank=True, default='')
    images = models.JSONField(null=True, default=list)
    news = models.JSONField(null=True, default=list)
    page_id = models.IntegerField(default=-1)
    title = models.CharField(max_length=1000, blank=True, default='')
    subtitle = models.CharField(max_length=1000, null=True)
    rel_url = models.CharField(max_length=1000, blank=True, default='')
    url = models.CharField(max_length=1000, blank=True, default='')
    last_seen = models.DateTimeField(auto_now=True, blank=True)
    active = models.BooleanField(default=True, blank=True)
    contacts = models.JSONField(null=True, default=list)

    class Meta:
        ordering = ['district_id', 'title']
