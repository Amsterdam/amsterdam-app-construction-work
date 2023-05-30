""" Iprox garbage collector """
from datetime import timedelta
from amsterdam_app_api.models import Projects
from amsterdam_app_api.models import ProjectDetails
from amsterdam_app_api.models import News


class GarbageCollector:
    """ Remove old scraped data from database if upstream has removed it too. """
    def __init__(self, last_scrape_time=None):
        self.last_scrape_time = last_scrape_time

    def collect_iprox(self, project_type=None):
        """ Call all iprox dataset garbage collectors one by one """
        report_projects = {}
        report_project_details = {}
        report_news = {}

        # If there's no path, projects might be de-activated un-rightfully
        if project_type is not None:
            news = list(News.objects.filter(project_type=project_type).all())
            report_news = self.garbage_collect_iprox(news, model=News, model_name='News')

            project_details = list(ProjectDetails.objects.filter(project_type=project_type).all())
            report_project_details = self.garbage_collect_iprox(project_details,
                                                                model=ProjectDetails,
                                                                model_name='ProjectDetails')

            projects = list(Projects.objects.filter(project_type=project_type).all())
            report_projects = self.garbage_collect_iprox(projects, model=Projects, model_name='Projects')

        return {'projects': report_projects, 'project_details': report_project_details, 'news': report_news}

    def garbage_collect_iprox(self, data_objects, model=None, model_name=None):
        """ Generic garbage collections method """
        report = {}
        for data_object in data_objects:
            # Check if we've seen this project anywhere in the last week, if not -> delete!
            if data_object.last_seen + timedelta(days=7) <= self.last_scrape_time:
                report[data_object.identifier] = 'deleted'
                if model_name == 'Projects':
                    # Siblings are cascaded deleted
                    data_object.delete()

            # We've seen the object (again!), mark active=true
            elif data_object.last_seen >= self.last_scrape_time:
                data = {'active': True}
                model.objects.filter(pk=data_object.identifier).update(**data)
                if model_name == 'ProjectDetails':
                    report[data_object.identifier_id] = 'activated'
                else:
                    report[data_object.identifier] = 'activated'

            # If we haven't seen the object in last scrape, assume it's deleted from iprox and mark inactive
            elif data_object.last_seen < self.last_scrape_time:
                data = {'active': False}
                if model_name == 'News':
                    model.objects.filter(identifier=data_object.identifier,
                                         project_identifier=data_object.project_identifier).update(**data)
                else:
                    model.objects.filter(pk=data_object.identifier).update(**data)

                if model_name == 'ProjectDetails':
                    report[data_object.identifier_id] = 'deactivated'
                else:
                    report[data_object.identifier] = 'deactivated'

        return report
