from django.db import models


""" Model for storing assets (e.g. PDF documents)

    assets are identifier by their identifier field created from a hash (md5) of its origin
"""


class Assets(models.Model):
    identifier = models.CharField(max_length=100, blank=False, unique=True, primary_key=True)
    url = models.CharField(max_length=1000, blank=False, unique=True, default='')
    mime_type = models.CharField(max_length=100, blank=False, default='application/pdf')
    data = models.BinaryField()


""" Model for storing an image

    Images are identified by their identifier field created from a hash (md5) of its origin
"""


class Image(models.Model):
    identifier = models.CharField(max_length=100, blank=False, unique=True, primary_key=True)
    size = models.CharField(max_length=10, blank=False, unique=False)
    url = models.CharField(max_length=1000, blank=False, unique=True)
    filename = models.CharField(max_length=1000, blank=False, unique=False)
    description = models.CharField(max_length=1000, blank=True, unique=False, default='')
    mime_type = models.CharField(max_length=100, blank=False, default='image/jpg')
    data = models.BinaryField()