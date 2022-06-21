import datetime
from datetime import timedelta
from django.db import models
from django.contrib.postgres.fields import ArrayField
from .followed_projects import FollowedProjects

""" Model for Device registration

    The MobileDevices model is used for sending a push-notification towards a mobile device. It holds a device
    identifier (unique token for sending push-notifications via a push-notification-broker (e.g. APN)
"""


class MobileDevices(models.Model):
    device_token = models.CharField(max_length=1000, unique=True, primary_key=True)
    os_type = models.CharField(max_length=7, unique=False, null=False)
    projects = ArrayField(models.CharField(max_length=40, blank=False), blank=False)


class FirebaseTokens(models.Model):
    deviceid = models.CharField(max_length=200, unique=True, primary_key=True)
    firebasetoken = models.CharField(max_length=1000, unique=True)
    os = models.CharField(max_length=7, unique=False, null=False)

    def save(self, *args, **kwargs):
        # We've seen the device, update its access log
        device_access_log = DeviceAccessLog.objects.filter(pk=self.deviceid).first()
        if device_access_log is not None:
            device_access_log.save()
        else:
            device_access_log = DeviceAccessLog(deviceid=self.deviceid)
            device_access_log.save()
        super(FirebaseTokens, self).save(*args, **kwargs)


class DeviceAccessLog(models.Model):
    deviceid = models.CharField(max_length=200, unique=True, primary_key=True)
    last_access = models.DateTimeField(auto_now=True, blank=True)

    def save(self, *args, **kwargs):
        self.last_access = datetime.datetime.now()
        super(DeviceAccessLog, self).save(*args, **kwargs)

    @staticmethod
    def prune():
        now = datetime.datetime.now()
        prune_date = now - timedelta(days=365)
        devices = DeviceAccessLog.objects.filter(last_access__lte=prune_date).all()
        device_ids = [x.deviceid for x in devices]

        FirebaseTokens.objects.filter(deviceid__in=device_ids).delete()
        FollowedProjects.objects.filter(deviceid__in=device_ids).delete()
        DeviceAccessLog.objects.filter(deviceid__in=device_ids).delete()
