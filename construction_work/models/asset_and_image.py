""" Assets and Images db models """

from django.db import models


class Asset(models.Model):
    """Model for storing assets (e.g. PDF documents)
    assets are identifier by their identifier field created from a hash (md5) of its origin
    """

    identifier = models.CharField(max_length=100, blank=False, unique=True, primary_key=True)
    url = models.CharField(max_length=1000, blank=False, unique=True, default="")
    mime_type = models.CharField(max_length=100, blank=False, default="application/pdf")
    data = models.BinaryField()


# NOTE: Could be merged with Asset and called a File
# file type can then be derived by mime_type
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
