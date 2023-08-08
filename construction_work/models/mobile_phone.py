""" Model for Device registration

    The MobileDevices model is used for sending a push-notification towards a mobile device. It holds a device
    identifier (unique token for sending push-notifications via a push-notification-broker (e.g. APN)
"""

import datetime
from datetime import timedelta

from django.db import models

from .followed_project import FollowedProject


class FirebaseToken(models.Model):
    """Firebase tokens db model"""

    deviceid = models.CharField(max_length=200, unique=True, primary_key=True)
    firebasetoken = models.CharField(max_length=1000, unique=True)
    os = models.CharField(max_length=7, unique=False, null=False)

    def save(self, *args, **kwargs):
        # We've seen the device, update its access log
        device_access_log = MobilePhoneAccessLog.objects.filter(pk=self.deviceid).first()
        if device_access_log is not None:
            device_access_log.save()
        else:
            device_access_log = MobilePhoneAccessLog(deviceid=self.deviceid)
            device_access_log.save()
        super(FirebaseToken, self).save(*args, **kwargs)


class MobilePhoneAccessLog(models.Model):
    """Device access log db model"""

    deviceid = models.CharField(max_length=200, unique=True, primary_key=True)
    last_access = models.DateTimeField(auto_now=True, blank=True)

    def save(self, *args, **kwargs):
        self.last_access = datetime.datetime.now()
        super(MobilePhoneAccessLog, self).save(*args, **kwargs)

    @staticmethod
    def prune():
        """Prune devices after 1 year of inactivity"""
        now = datetime.datetime.now()
        prune_date = now - timedelta(days=365)
        devices = MobilePhoneAccessLog.objects.filter(last_access__lte=prune_date).all()
        device_ids = [x.deviceid for x in devices]

        FirebaseToken.objects.filter(deviceid__in=device_ids).delete()
        FollowedProject.objects.filter(deviceid__in=device_ids).delete()
        MobilePhoneAccessLog.objects.filter(deviceid__in=device_ids).delete()
