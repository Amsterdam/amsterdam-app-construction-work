import datetime
from amsterdam_app_api.models import Projects
from amsterdam_app_api.models import ProjectDetails
from amsterdam_app_api.models import News
from amsterdam_app_api.models import Notification
from amsterdam_app_api.models import WarningMessages
from amsterdam_app_api.models import ProjectManager


class GarbageCollector:
    def __init__(self, last_scrape_time=0):
        self.last_scrape_time = last_scrape_time

    def collect_iprox(self, project_type=None):
        # If there's no path, projects might be de-activated un-rightfully
        if project_type is not None:
            self.garbage_collect_iprox(Projects.objects.filter(project_type=project_type).all(), siblings=True)
            self.garbage_collect_iprox(ProjectDetails.objects.filter(project_type=project_type).all())
            self.garbage_collect_iprox(News.objects.filter(project_type=project_type).all())

    def garbage_collect_iprox(self, data_objects, siblings=False):
        for data_object in data_objects:
            # Check if we've seen this project anywhere in the last week, if not -> delete!
            if data_object.last_seen + datetime.timedelta(days=7) <= self.last_scrape_time:
                if siblings is True:
                    # Remove ProjectDetails, News, Notifications, Warning-messages
                    ProjectDetails.objects.filter(identifier=data_object.identifier).delete()
                    News.objects.filter(project_identifier=data_object.identifier).delete()
                    Notification.objects.filter(project_identifier=data_object.identifier).delete()
                    WarningMessages.objects.filter(project_identifier=data_object.identifier).delete()
                    project_managers = list(ProjectManager.objects.all())

                    # Cleanup authorizations
                    for project_manager in project_managers:
                        if data_object.identifier in project_manager.projects:
                            project_manager.projects.remove(data_object.identifier)
                            project_manager.save()

                data_object.delete()

            # We've seen the object (again!), mark active=true
            elif data_object.last_seen >= self.last_scrape_time:
                data_object.active = True
                data_object.save()

            # If we haven't seen the object in last scrape, assume it's deleted from iprox and mark inactive
            elif data_object.last_seen < self.last_scrape_time:
                data_object.active = False
                data_object.save()
