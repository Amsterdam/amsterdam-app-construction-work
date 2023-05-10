""" Model for ProjectManagers

    The ProjectManagers model is used to add an project-manager to a set of projects. An identifier (UUIDv4) is
    assigned to the project-manager alongside its assigned projects (list) and email-address of the project-manager
"""

import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from amsterdam_app_api.models.projects import Projects


class ProjectManager(models.Model):
    """ Project manager db model """
    identifier = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=60, unique=True)
    projects = ArrayField(models.CharField(max_length=40, blank=False), blank=False)

    def validate_email(self):
        """ Validate email constraint """
        if self.email.split('@')[1] != 'amsterdam.nl':
            raise ValueError('Invalid email, should be <username>@amsterdam.nl')

    def save(self, *args, **kwargs):
        self.validate_email()
        super(ProjectManager, self).save(*args, **kwargs)


@receiver(pre_delete, sender=Projects)
def remove_project_from_managers(sender, instance, **kwargs):
    """ This code adds a signal receiver function remove_project_from_managers that listens for the pre_delete signal of
        the Projects model. When a project is about to be deleted, the remove_project_from_managers function is called
        with the instance parameter being the project being deleted.

        The function then gets the identifier of the project and finds all ProjectManager instances that have this
        project in their projects array field using the projects__contains query lookup. It then uses the remove method
        to remove the project from the projects array field of all the matching ProjectManager instances. This will
        automatically update the projects array of all the affected ProjectManager instances in the database.
    """
    identifier = str(instance.identifier)
    project_managers = list(ProjectManager.objects.all())
    for project_manager in project_managers:
        if identifier in project_manager.projects:
            project_manager.projects.remove(identifier)
            project_manager.save()
