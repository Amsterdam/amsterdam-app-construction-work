""" Models for Article for Projects

    An article is either a 'nieuws' item or a 'wegwerkzaamheden' item. Both follow the same scheme but are distinguished
    by the tag 'news' or 'roadworks'
"""

from django.db import models

from construction_work.models.project import Project


class Article(models.Model):
    """Article db model

    Note on 'project_identifier': (fields.W342) Setting unique=True on a ForeignKey has the same effect as using a
    OneToOneField. ForeignKey(unique=True) is usually better served by a OneToOneField.

    Note on 'on_delete=Models.CASCADE' When the referenced object is deleted, also delete the objects that have
    references to it (when you remove a Project for instance, you might want to delete ProjectDetails as well). SQL
    equivalent: CASCADE.
    """ 

    article_id = models.BigIntegerField(blank=False, null=False, unique=True)
    projects = models.ManyToManyField(Project, blank=False)
    title = models.TextField(blank=True, null=True, default=None)
    intro = models.TextField(blank=True, null=True, default=None)
    body = models.TextField(blank=True, null=True, default=None)
    image = models.JSONField(blank=True, null=True, default=None)
    # To be expected e.g.: news or work
    type = models.CharField(max_length=30, blank=True, null=True, default=None)
    url = models.CharField(max_length=1000, blank=True, null=True, default=None)

    creation_date = models.DateTimeField(blank=True, null=True, default=None)
    modification_date = models.DateTimeField(blank=True, null=True, default=None)
    publication_date = models.DateTimeField(blank=True, null=True, default=None)
    expiration_date = models.DateTimeField(blank=True, null=True, default=None)
    
    last_seen = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
