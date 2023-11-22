""" Assets and Images db models """

from django.db import models


class Image(models.Model):
    """Model for storing an image
    Images are identified by their identifier field created from a hash (md5) of its origin
    """

    data = models.BinaryField(blank=False, null=False)
    description = models.CharField(max_length=1000, blank=True, null=True, default=None)
    width = models.IntegerField()
    height = models.IntegerField()
    aspect_ratio = models.FloatField(blank=False)
    # coordinates format: {"lat": 0.0, "lon": 0.0}
    coordinates = models.JSONField(blank=True, null=True, default=None)
    mime_type = models.CharField(max_length=100, blank=False, default="image/jpg")
