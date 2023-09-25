"""A device represent a mobile device that is running the Amsterdam App frontend"""

from django.db import models

from construction_work.models.project import Project


class Device(models.Model):
    """Mobile device running the mobile app"""
    device_id = models.CharField(max_length=200, blank=False, unique=True)
    followed_projects = models.ManyToManyField(Project)
