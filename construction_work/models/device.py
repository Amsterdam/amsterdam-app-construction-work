"""A device represent a mobile device that is running the Amsterdam App frontend"""

from datetime import datetime
from django.db import models

from construction_work.models.project import Project


class Device(models.Model):
    """Mobile device running the mobile app"""
    device_id = models.CharField(max_length=200, blank=False, unique=True)
    followed_projects = models.ManyToManyField(Project, blank=True)
    last_access = models.DateTimeField(auto_now=True, blank=True)

    def save(self, *args, **kwargs):
        # We've seen the device, update its access log
        self.last_access = datetime.now()
        super(Device, self).save(*args, **kwargs)
