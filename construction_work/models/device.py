"""A device represent a mobile device that is running the Amsterdam App frontend"""

from django.db import IntegrityError
from django.db import models

from construction_work.models.project import Project


class Device(models.Model):
    """Mobile device running the mobile app"""

    device_id = models.CharField(max_length=200, blank=False, unique=True)
    firebase_token = models.CharField(max_length=1000, unique=True, null=True)
    os = models.CharField(max_length=7, blank=True, null=True, unique=False)
    followed_projects = models.ManyToManyField(Project, blank=True)
    last_access = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            # The firebase_token field should be null
            # or not an empty unique string
            models.CheckConstraint(
                name="firebase_token_unique_or_null",
                check=models.Q(firebase_token__isnull=True)
                | ~models.Q(firebase_token=""),
            ),
        ]

    def save(self, *args, **kwargs):
        if (
            self.firebase_token is not None
            and self.__class__.objects.exclude(pk=self.pk)
            .filter(firebase_token=self.firebase_token)
            .exists()
        ):
            raise IntegrityError("The 'firebase_token' field must be unique or null.")
        super().save(*args, **kwargs)
