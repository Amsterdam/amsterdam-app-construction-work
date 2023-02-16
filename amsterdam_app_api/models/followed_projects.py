""" FollowedProjects: Keeps track of a device following a project
"""

from django.db import models


class FollowedProjects(models.Model):
    """ Follow projects db model """
    deviceid = models.CharField(max_length=200, blank=False)
    projectid = models.CharField(max_length=100, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['deviceid', 'projectid'], name='deviceid_and_projectid')
        ]
