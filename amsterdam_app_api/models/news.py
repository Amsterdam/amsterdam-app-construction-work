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

from datetime import datetime
from django.db import models
from amsterdam_app_api.models.projects import Projects


class News(models.Model):
    """ News db model

        Note on 'project_identifier': (fields.W342) Setting unique=True on a ForeignKey has the same effect as using a
        OneToOneField. ForeignKey(unique=True) is usually better served by a OneToOneField.

        Note on 'on_delete=Models.CASCADE' When the referenced object is deleted, also delete the objects that have
        references to it (when you remove a Project for instance, you might want to delete ProjectDetails as well). SQL
        equivalent: CASCADE.
    """
    id = models.BigAutoField(primary_key=True)
    identifier = models.CharField(max_length=100, blank=False)
    project_identifier = models.ForeignKey(Projects,
                                           on_delete=models.CASCADE,
                                           unique=False,
                                           db_column='project_identifier')
    project_type = models.CharField(max_length=100, default='', blank=False, unique=False)
    url = models.CharField(max_length=1000, blank=True, default='')
    title = models.CharField(max_length=1000, blank=True, default='', db_index=True)
    publication_date = models.CharField(max_length=10, blank=True, default='')
    body = models.JSONField(null=True, default=dict)
    images = models.JSONField(null=True, default=list)
    assets = models.JSONField(null=True, default=list)
    last_seen = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['identifier', 'project_identifier'],
                                    name='identifier_and_project_identifier')
        ]
        ordering = ['publication_date']

    def save(self, *args, **kwargs):
        self.last_seen = datetime.now()
        super(News, self).save(*args, **kwargs)
