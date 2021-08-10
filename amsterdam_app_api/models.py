from django.db import models

# Models for storing/formatting data from various data end-point of the 'gemeente-amsterdam'


class ProjectenBruggen(models.Model):
    districts_id = models.IntegerField(default=-1)
    title = models.CharField(max_length=1000, blank=True, default='')
    content_html = models.TextField()
    content_text = models.TextField()
    images = models.JSONField(null=True, default=list)
    identifier = models.CharField(max_length=100, blank=False, unique=True, primary_key=True)
    publication_date = models.CharField(max_length=40, blank=False)
    modification_date = models.CharField(max_length=40, blank=False)
    source_url = models.CharField(max_length=1000, blank=True, default='')

    class Meta:
        ordering = ['title']


class ProjectenKademuren(models.Model):
    districts_id = models.IntegerField(default=-1)
    title = models.CharField(max_length=1000, blank=True, default='')
    content_html = models.TextField()
    content_text = models.TextField()
    images = models.JSONField(null=True, default=list)
    identifier = models.CharField(max_length=100, blank=False, unique=True, primary_key=True)
    publication_date = models.CharField(max_length=40, blank=False)
    modification_date = models.CharField(max_length=40, blank=False)
    source_url = models.CharField(max_length=1000, blank=True, default='')

    class Meta:
        ordering = ['title']
