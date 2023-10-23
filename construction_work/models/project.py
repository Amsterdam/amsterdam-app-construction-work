""" Models for Project """

from django.db import models
from django.utils import timezone


class Project(models.Model):
    """Projects db model"""

    foreign_id = models.BigIntegerField(blank=False, unique=True, null=False)

    active = models.BooleanField(default=True, blank=True)
    last_seen = models.DateTimeField(blank=True, null=False)

    title = models.CharField(max_length=1000, blank=True, null=True, default="", db_index=True)
    subtitle = models.CharField(max_length=1000, blank=True, null=True, db_index=True)
    coordinates = models.JSONField(blank=True, null=True, default=None)
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
        self.last_seen = timezone.now()
        super(Project, self).save(*args, **kwargs)

    def deactivate(self, *args, **kwargs):
        self.active = False
        super(Project, self).save(*args, **kwargs)
