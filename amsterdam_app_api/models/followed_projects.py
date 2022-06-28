from django.db import models


""" FollowedProjects: Keeps track of a device following a project
"""


class FollowedProjects(models.Model):
    deviceid = models.CharField(max_length=200, blank=False)
    projectid = models.CharField(max_length=100, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['deviceid', 'projectid'], name='deviceid_and_projectid')
        ]
