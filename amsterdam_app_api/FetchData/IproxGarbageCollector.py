import datetime
from amsterdam_app_api.models import Projects, ProjectDetails, News


class IproxGarbageCollector:
    def __init__(self, last_scrape_time=0):
        self.last_scrape_time = last_scrape_time

    def run(self, project_type=None):
        # If there's no path, projects might be de-activated un-rightfully
        if project_type is not None:
            self.garbage_collect(Projects.objects.filter(project_type=project_type).all())
            self.garbage_collect(ProjectDetails.objects.filter(project_type=project_type).all())
            self.garbage_collect(News.objects.filter(project_type=project_type).all())

    def garbage_collect(self, data_objects):
        for data_object in data_objects:
            # Check if we've seen this project anywhere in the last week, if not -> delete!
            if data_object.last_seen + datetime.timedelta(days=7) <= self.last_scrape_time:
                data_object.delete()

            # We've seen the object (again!), mark active=true
            elif data_object.last_seen >= self.last_scrape_time:
                data_object.active = True
                data_object.save()

            # If we haven't seen the object in last scrape, assume it's deleted from iprox and mark inactive
            elif data_object.last_seen < self.last_scrape_time:
                data_object.active = False
                data_object.save()
