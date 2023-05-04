""" FollowedProjects: Keeps track of a device following a project
"""

from django.db import models
from amsterdam_app_api.models.projects import Projects


class FollowedProjects(models.Model):
    """ Follow projects db model

        Note on 'identifier': (fields.W342) Setting unique=True on a ForeignKey has the same effect as using a
        OneToOneField. ForeignKey(unique=True) is usually better served by a OneToOneField.

        Note on 'on_delete=Models.CASCADE' When the referenced object is deleted, also delete the objects that have
        references to it (when you remove a Project for instance, you might want to delete ProjectDetails as well). SQL
        equivalent: CASCADE.
    """
    deviceid = models.CharField(max_length=200, blank=False)
    projectid = models.ForeignKey(Projects, on_delete=models.CASCADE, unique=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['deviceid', 'projectid'], name='deviceid_and_projectid')
        ]
