from django.db import models

""" Model for storing assets (e.g. PDF documents)

    assets are identifier by threir identifier field created from a hash (md5) of its origin
"""


class Assets(models.Model):
    identifier = models.CharField(max_length=100, blank=False, unique=True, primary_key=True)
    url = models.CharField(max_length=1000, blank=False, unique=True, default='')
    mime_type = models.CharField(max_length=100, blank=False, default='application/pdf')
    data = models.BinaryField()


""" Model for storing an image

    Images are identified by their identifier field created from a hash (md5) of its origin
"""


class Image(models.Model):
    identifier = models.CharField(max_length=100, blank=False, unique=True, primary_key=True)
    size = models.CharField(max_length=10, blank=False, unique=False)
    url = models.CharField(max_length=1000, blank=False, unique=True)
    filename = models.CharField(max_length=1000, blank=False, unique=False)
    description = models.CharField(max_length=1000, blank=True, unique=False, default='')
    mime_type = models.CharField(max_length=100, blank=False, default='image/jpg')
    data = models.BinaryField()


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
        "url": string
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

    class Meta:
        ordering = ['title']


class ProjectDetails(models.Model):
    identifier = models.CharField(max_length=100, blank=False, unique=True, primary_key=True)
    body = models.JSONField(null=True, default=list)
    district_id = models.IntegerField(default=-1)
    district_name = models.CharField(max_length=1000, blank=True, default='')
    images = models.JSONField(null=True, default=list)
    news = models.JSONField(null=True, default=list)
    page_id = models.IntegerField(default=-1)
    title = models.CharField(max_length=1000, blank=True, default='')
    subtitle = models.CharField(max_length=1000, null=True)
    rel_url = models.CharField(max_length=1000, blank=True, default='')
    url = models.CharField(max_length=1000, blank=True, default='')

    class Meta:
        ordering = ['district_id', 'title']


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
    url = models.CharField(max_length=1000, blank=True, default='')
    title = models.CharField(max_length=1000, blank=True, default='')
    publication_date = models.CharField(max_length=10, blank=True, default='')
    body = models.JSONField(null=True, default=dict)
    images = models.JSONField(null=True, default=list)
    assets = models.JSONField(null=True, default=list)


""" Models for 'Omgevings-managers'

    The Omgevings-manager is used to add an 'OM' to a set of projects. An identifier (UUIDv4) is assigned to
    the OM alongside its assigned projects (list) and email-address of the OM

    Json produced by OM model:

    {
        "email": "string",
        "identifier": "string UUIDv4",
        "projects": ["project id", ...]
    }
"""


class OM(models.Model):
    identifier = models.CharField(max_length=36, blank=False, unique=True, primary_key=True)
    email = models.EmailField(blank=False, unique=True)
    projects = models.JSONField(null=True, default=list)
