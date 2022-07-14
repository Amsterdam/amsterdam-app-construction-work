import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField

""" Model for ProjectManagers

    The ProjectManagers model is used to add an project-manager to a set of projects. An identifier (UUIDv4) is 
    assigned to the project-manager alongside its assigned projects (list) and email-address of the project-manager
"""


class ProjectManager(models.Model):
    identifier = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=60, unique=True)
    projects = ArrayField(models.CharField(max_length=40, blank=False), blank=False)

    def validate_email(self):
        if self.email.split('@')[1] != 'amsterdam.nl':
            raise ValueError('Invalid email, should be <username>@amsterdam.nl')

    def save(self, *args, **kwargs):
        self.validate_email()
        super(ProjectManager, self).save(*args, **kwargs)
