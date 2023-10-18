""" Model for Warning message """

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
    project_manager = models.ForeignKey(ProjectManager, blank=True, null=True, on_delete=models.SET_NULL)
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
