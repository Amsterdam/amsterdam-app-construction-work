import uuid
import datetime
from django.db import models
from django.contrib.postgres.fields import ArrayField

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
    project_type = models.CharField(max_length=100, default='', blank=False, unique=False)
    url = models.CharField(max_length=1000, blank=True, default='')
    title = models.CharField(max_length=1000, blank=True, default='')
    publication_date = models.CharField(max_length=10, blank=True, default='')
    body = models.JSONField(null=True, default=dict)
    images = models.JSONField(null=True, default=list)
    assets = models.JSONField(null=True, default=list)
    last_seen = models.DateTimeField(auto_now=True, blank=True)
    active = models.BooleanField(default=True, blank=True)


""" Model for ProjectManagers

    The ProjectManagers model is used to add an project-manager to a set of projects. An identifier (UUIDv4) is 
    assigned to the project-manager alongside its assigned projects (list) and email-address of the project-manager

    Json produced by ProjectManagers model:

    {
        "email": "<string>@amsterdam.nl",
        "identifier": "string UUID-v4",
        "projects": ["project id", ...]
    }
"""


class ProjectManager(models.Model):
    identifier = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=60, unique=True)
    projects = ArrayField(models.CharField(max_length=40, blank=False), blank=False)

    def validate_email(self):
        if self.email.split('@')[1] != 'amsterdam.nl':
            raise ValueError('Invalid email, should be <username>@amsterdam.nl')

    def save(self, *args, **kwargs):
        self.validate_email()
        super(ProjectManager, self).save(*args, **kwargs)


""" Model for Mobile Devices

    The MobileDevices model is used for sending a push-notification towards a mobile device. It holds a device
    identifier (unique token for sending push-notifications via a push-notification-broker (e.g. APN)
    
    Json produced by ModelDevices model:

    {
        "identifier": "device identifier for either Android or IOS",
        "os_type": "android of ios"
        "projects": ["project id", ...]
    }
"""


class MobileDevices(models.Model):
    device_token = models.CharField(max_length=1000, unique=True, primary_key=True)
    os_type = models.CharField(max_length=7, unique=False, null=False)
    projects = ArrayField(models.CharField(max_length=40, blank=False), blank=False)


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
        "body": {
            "preface": "short text",
            "content": "longer text"
        },
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
    body = models.JSONField(null=False, blank=False, default=dict)
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


class CityContacts(models.Model):
    contact = models.JSONField(null=True, default=dict)
    city_counters = models.JSONField(null=True, default=dict)

    def save(self, *args, **kwargs):
        self.id = 1  # Allow only 1 row in table
        super().save(*args, **kwargs)


class CityCounter(models.Model):
    identifier = models.CharField(max_length=100, blank=False, unique=True, primary_key=True)
    location = models.CharField(max_length=100, blank=False, unique=True)
    contact = models.JSONField(null=True, default=dict)
    images = models.JSONField(null=True, default=dict)
    info = models.JSONField(null=True, default=dict)
    address = models.JSONField(null=True, default=dict)
    last_seen = models.DateTimeField(auto_now=True, blank=True)
    active = models.BooleanField(default=True, blank=True)
