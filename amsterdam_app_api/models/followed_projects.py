""" FollowedProjects: Keeps track of a device following a project
"""

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from amsterdam_app_api.models.projects import Projects


class FollowedProjects(models.Model):
    """ Follow projects db model
    """
    deviceid = models.CharField(max_length=200, blank=False)
    projectid = models.CharField(max_length=20, blank=False, default='', unique=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['deviceid', 'projectid'], name='deviceid_and_projectid')
        ]


@receiver(pre_delete, sender=Projects)
def remove_project_from_followed_projects(sender, instance, **kwargs):
    """ This code adds a signal receiver function remove_project_from_followed_projects that listens for the pre_delete
        signal of the Projects model. When a project is about to be deleted, the remove_project_from_managers function
        is called with the instance parameter being the project being deleted.

        The function then gets the identifier of the project and finds all ProjectManager instances that have this
        project in their projects array field using the projects__contains query lookup. It then uses the remove method
        to remove the project from the projects array field of all the matching ProjectManager instances. This will
        automatically update the projects array of all the affected ProjectManager instances in the database.
    """
    for followed_project in FollowedProjects.objects.filter(projectid__contains=instance.identifier):
        followed_project.delete()
