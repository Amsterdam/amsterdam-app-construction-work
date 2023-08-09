""" Models for Article for Projects

    An article is either a 'nieuws' item or a 'wegwerkzaamheden' item. Both follow the same scheme but are distinguished
    by the tag 'news' or 'roadworks'
"""

from datetime import datetime

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

    id = models.BigAutoField(primary_key=True)
    identifier = models.CharField(max_length=100, blank=False)
    project_identifier = models.ForeignKey(
        Project, on_delete=models.CASCADE, unique=False, db_column="project_identifier"
    )
    project_type = models.CharField(max_length=100, default="", blank=False, unique=False)
    url = models.CharField(max_length=1000, blank=True, default="")
    title = models.CharField(max_length=1000, blank=True, default="", db_index=True)
    publication_date = models.CharField(max_length=10, blank=True, default="")
    body = models.JSONField(null=True, default=dict)
    images = models.JSONField(null=True, default=list)
    assets = models.JSONField(null=True, default=list)
    last_seen = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True, blank=True)
    type = models.CharField(max_length=30, default="news", blank=False)  # news or work

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["identifier", "project_identifier"], name="identifier_and_project_identifier"
            )
        ]
        ordering = ["publication_date"]

    def save(self, *args, **kwargs):
        self.last_seen = datetime.now()
        super(Article, self).save(*args, **kwargs)
