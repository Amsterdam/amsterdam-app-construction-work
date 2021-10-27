import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "amsterdam_app_backend.settings")
import django
django.setup()
import lorem

from amsterdam_app_api.models import Projects
from amsterdam_app_api.serializers import ProjectsSerializer
from amsterdam_app_api.models import ProjectManager
from amsterdam_app_api.serializers import ProjectManagerSerializer
from amsterdam_app_api.models import WarningMessages
from amsterdam_app_api.models import Notification


class Inject:
    def __init__(self):
        self.projects = self.get_projects()
        self.manager_by_project_id = dict()

    def get_projects(self):
        data = list(Projects.objects.all())
        serializer = ProjectsSerializer(data, many=True)
        return serializer.data

    def project_managers(self):
        num = int(len(self.projects) / 9)
        mod = len(self.projects) % num
        names = [('Angelicus', num), ('Blaesus', num), ('Clarensis', num),
                 ('Eleutherius', num), ('Flavus', num), ('Hermetis', num),
                 ('Octavion', num), ('Franciscus', num), ('Aegidius', num + mod)]

        identifiers = []
        begin = 0
        for name in names:
            end = begin + name[1]
            for i in range(begin, end):
                identifiers.append(self.projects[i]['identifier'])
            payload = {'projects': identifiers, 'email': '{name}@amsterdam.nl'.format(name=name[0])}
            ProjectManager.objects.create(**payload).save()
            identifiers = []
            begin = end

    @staticmethod
    def set_manager_by_project_id():
        data = list(ProjectManager.objects.all())
        serializer = ProjectManagerSerializer(data, many=True)
        result = dict()
        for project_manager in serializer.data:
            for identifier in project_manager['projects']:
                result[identifier] = project_manager['identifier']
        return result

    def warning_messages(self):
        self.manager_by_project_id = self.set_manager_by_project_id()
        for project in self.projects:
            for i in range(5):
                project = dict(project)
                warning = {
                    'title': lorem.sentence(),
                    'project_identifier': project['identifier'],
                    'project_manager_token': self.manager_by_project_id[project['identifier']],
                    'body': {'preface': lorem.paragraph(), 'content': lorem.text()},
                    'images': project['images']
                }
                warn_obj = WarningMessages(**warning)
                warn_obj.save()

                notification = {
                    'title': warning['title'],
                    'body': warning['body']['preface'],
                    'project_identifier': project['identifier'],
                    'warning_identifier': warn_obj.identifier
                }
                not_obj = Notification(**notification)
                not_obj.save()


if __name__ == '__main__':
    inject = Inject()
    inject.project_managers()
    inject.warning_messages()
