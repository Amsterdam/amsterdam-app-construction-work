""" Model for Warning message

    Notes:
    The project manager writes and article. We’re only sending the text content to start
    with, to not burden the request with lots of image data. We expect a warning identifier in the
    response, with which we can relate the notification content and the images we’re sending next.

    Post body by API:

    {
        "title": "title",
        "body": {
          "preface": "short text",
          "content": "longer text"
        },
        "project_id": "8ac7ed07fc76a0812b3afbd5f0182aeb",
        "project_manager_id": "UUIDv4"
        "publication_date": DateTimefield,
        "modification_date": DateTimefield
    }

    Produced json:

    {
        "identifier": "UUIDv4",
        "title": "Title",
        "body": "text",
        "project_identifier": "8ac7ed07fc76a0812b3afbd5f0182aeb",
        "project_manager_id": "UUIDv4",
        "publication_date": DateTimefield,
        "modification_date": DateTimefield,
        "author_email": "p.puk@amsterdam.nl"
        "images": [{
            "type": "header",
            "sources": {
                "orig": {
                    "url": None,
                    "filename": None,
                    "image_id": "af53bcc112bed15d233befd67077ab3a",
                    "description": "description text"
                }
            }
        }, ...]
    }
"""

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from construction_work.generic_functions.static_data import DEFAULT_WARNING_MESSAGE_EMAIL
from construction_work.models.asset_and_image import Image
from construction_work.models.project import Project

from .project_manager import ProjectManager


class WarningMessage(models.Model):
    """Warning message db model"""

    title = models.CharField(max_length=1000, db_index=True)
    body = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    project_manager = models.ForeignKey(ProjectManager, blank=True, null=True, on_delete=models.PROTECT)
    publication_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    author_email = models.EmailField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.author_email = DEFAULT_WARNING_MESSAGE_EMAIL
        if self.project_manager is not None:
            self.author_email = self.project_manager.email

        super().save(*args, **kwargs)


class WarningImage(models.Model):
    """Warning image db model"""

    warning = models.ForeignKey(WarningMessage, on_delete=models.CASCADE)
    is_main = models.BooleanField(default=False)
    images = models.ManyToManyField(Image)


@receiver(pre_delete, sender=WarningImage)
def remove_images_for_warning_message(sender, instance, **kwargs):
    """Delete images for warning messages"""
    for image in instance.images.all():
        image.delete()


class Notification(models.Model):
    """Notifications db model"""

    title = models.CharField(max_length=1000, blank=False, null=False)
    body = models.TextField(blank=True, null=True)
    warning = models.ForeignKey(WarningMessage, on_delete=models.CASCADE, blank=False, null=False)
    publication_date = models.DateTimeField(auto_now_add=True, blank=True)
