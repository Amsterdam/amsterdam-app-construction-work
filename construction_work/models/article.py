# pylint: disable=cyclic-import
""" Models for Article for Projects

    An article is either a 'nieuws' item or a 'wegwerkzaamheden' item. Both follow the same scheme but are distinguished
    by the tag 'news' or 'roadworks'
"""

from django.db import models
from django.utils import timezone

from construction_work.generic_functions.model_utils import create_id_dict
from construction_work.models.project import Project


class Article(models.Model):
    """Article db model"""

    foreign_id = models.BigIntegerField(blank=False, null=False, unique=True)

    active = models.BooleanField(default=True)
    last_seen = models.DateTimeField(auto_now=True)

    title = models.CharField(
        max_length=1000, blank=True, null=True, default="", db_index=True
    )
    intro = models.TextField(blank=True, null=True, default=None)
    body = models.TextField(blank=True, null=True, default=None)
    image = models.JSONField(blank=True, null=True, default=None)
    type = models.CharField(max_length=30, blank=True, null=True, default=None)
    projects = models.ManyToManyField(Project, blank=False)
    url = models.URLField(max_length=2048, blank=True, null=True)
    creation_date = models.DateTimeField(
        default=timezone.now
    )  # If no date is provided use the current date
    modification_date = models.DateTimeField(
        default=timezone.now
    )  # If no date is provided use the current date
    publication_date = models.DateTimeField(default=None, null=True)
    expiration_date = models.DateTimeField(default=None, null=True)

    def get_id_dict(self):
        """Get id dict"""
        return create_id_dict(type(self), self.pk)
