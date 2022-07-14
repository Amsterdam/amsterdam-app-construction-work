from django.db import models
from django.contrib.postgres.fields import ArrayField


class CityContact(models.Model):
    sections = ArrayField(models.JSONField(null=True, default=dict), blank=False)

    def save(self, *args, **kwargs):
        self.id = 1  # Allow only 1 row in table
        super().save(*args, **kwargs)


class CityOffices(models.Model):
    offices = ArrayField(models.JSONField(null=True, default=dict), blank=False)

    def save(self, *args, **kwargs):
        self.id = 1  # Allow only 1 row in table
        super().save(*args, **kwargs)


class CityOffice(models.Model):
    identifier = models.CharField(max_length=100, blank=False, unique=True, primary_key=True)
    title = models.CharField(max_length=100, blank=False, unique=True)
    contact = models.JSONField(null=True, default=dict)
    images = models.JSONField(null=True, default=dict)
    info = models.JSONField(null=True, default=dict)
    address = models.JSONField(null=True, default=dict)
    last_seen = models.DateTimeField(auto_now=True, blank=True)
    active = models.BooleanField(default=True, blank=True)
