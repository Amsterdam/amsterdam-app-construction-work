""" UNITTESTS """

import datetime
from django.test import TestCase
from amsterdam_app_api.UNITTESTS.mock_data import TestData
from amsterdam_app_api.GarbageCollector.GarbageCollector import GarbageCollector
from amsterdam_app_api.models import Projects
from amsterdam_app_api.models import ProjectDetails
from amsterdam_app_api.models import News
from amsterdam_app_api.models import ProjectManager


class TestGarbageCollector(TestCase):
    """ test for garbage collector"""
    def __init__(self, *args, **kwargs):
        super(TestGarbageCollector, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        """ setup test db """
        Projects.objects.all().delete()
        for project in self.data.projects:
            Projects.objects.create(**project)

        ProjectDetails.objects.all().delete()
        for project_detail in self.data.project_details:
            try:
                project = Projects.objects.filter(pk=project_detail['identifier']).first()
                project_detail['identifier'] = project
                ProjectDetails.objects.create(**project_detail)
            except Exception as error:
                print(error)

        News.objects.all().delete()
        for news in self.data.news:
            project = Projects.objects.filter(pk=news['project_identifier']).first()
            news['project_identifier'] = project
            News.objects.create(**news)

        ProjectManager.objects.all().delete()
        for project_manager in self.data.project_manager:
            ProjectManager.objects.create(**project_manager)

    def test_no_objects_changed(self):
        """ test with no objects changed """
        gc = GarbageCollector(last_scrape_time=(datetime.datetime.now() - datetime.timedelta(hours=1)))
        gc.collect_iprox(project_type='brug')
        projects = list(Projects.objects.all())
        project_details = list(ProjectDetails.objects.all())
        news_items = list(News.objects.all())


        for project in projects:
            self.assertEqual(project.active, True)

        for project in project_details:
            self.assertEqual(project.active, True)

        for item in news_items:
            self.assertEqual(item.active, True)

    def test_all_objects_inactive(self):
        """ test if all objects are inactive """
        gc = GarbageCollector(last_scrape_time=datetime.datetime.now())
        gc.collect_iprox(project_type='brug')
        gc.collect_iprox(project_type='kade')
        projects = list(Projects.objects.all())
        project_details = list(ProjectDetails.objects.all())
        news_items = list(News.objects.all())

        for project in projects:
            self.assertEqual(project.active, False)

        for project in project_details:
            self.assertEqual(project.active, False)

        for item in news_items:
            self.assertEqual(item.active, False)

    def test_all_objects_deleted(self):
        """ test that all objects are deleted """
        gc = GarbageCollector(last_scrape_time=(datetime.datetime.now() + datetime.timedelta(days=7)))
        gc.collect_iprox(project_type='brug')
        gc.collect_iprox(project_type='kade')
        projects = list(Projects.objects.all())
        project_details = list(ProjectDetails.objects.all())
        news_items = list(News.objects.all())

        self.assertEqual(len(projects), 0)
        self.assertEqual(len(project_details), 0)
        self.assertEqual(len(news_items), 0)
