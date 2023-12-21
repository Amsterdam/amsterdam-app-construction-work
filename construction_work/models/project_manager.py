""" Model for ProjectManagers

    The ProjectManagers model is used to add a project-manager to a set of projects. An identifier (UUIDv4) is
    assigned to the project-manager alongside its assigned projects (list) and email-address of the project-manager
"""

import uuid

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db import models

from construction_work.models.project import Project


class AmsterdamEmailValidator(EmailValidator):
    """Amsterdam email validator"""

    def __call__(self, value):
        """Custom email validator"""

        super().__call__(value)
        if not value.endswith("@amsterdam.nl"):
            raise ValidationError(
                "Email must belong to 'amsterdam.nl'", code="invalid_email"
            )


class ProjectManager(models.Model):
    """Project manager db model"""

    manager_key = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(validators=[AmsterdamEmailValidator()])
    projects = models.ManyToManyField(Project, blank=True)
