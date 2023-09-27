""" Model for Device registration

    The MobileDevices model is used for sending a push-notification towards a mobile device. It holds a device
    identifier (unique token for sending push-notifications via a push-notification-broker (e.g. APN)
"""

from django.db import models

from construction_work.models.device import Device


class FirebaseToken(models.Model):
    """Firebase tokens db model"""

    firebase_token = models.CharField(max_length=1000, unique=True)
    os = models.CharField(max_length=7, unique=False, null=False)
    device = models.OneToOneField(Device, on_delete=models.CASCADE)
