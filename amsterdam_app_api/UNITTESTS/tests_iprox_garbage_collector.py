import datetime
from django.test import TestCase
from amsterdam_app_api.UNITTESTS.mock_data import TestData
from amsterdam_app_api.FetchData.IproxGarbageCollector import IproxGarbageCollector
from amsterdam_app_api.models import Projects
from amsterdam_app_api.models import ProjectDetails
from amsterdam_app_api.models import News


class TestIproxGarbageCollector(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestIproxGarbageCollector, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        Projects.objects.all().delete()
        for project in self.data.projects:
            Projects.objects.create(**project)

        ProjectDetails.objects.all().delete()
        for project in self.data.project_details:
            ProjectDetails.objects.create(**project)

        News.objects.all().delete()
        for news in self.data.news:
            News.objects.create(**news)

    def test_no_objects_changed(self):
        gc = IproxGarbageCollector(datetime.datetime.now() - datetime.timedelta(hours=1))
        gc.run(project_type='brug')
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
        gc = IproxGarbageCollector(datetime.datetime.now())
        gc.run(project_type='brug')
        gc.run(project_type='kade')
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
        gc = IproxGarbageCollector(datetime.datetime.now() + datetime.timedelta(days=7))
        gc.run(project_type='brug')
        gc.run(project_type='kade')
        projects = list(Projects.objects.all())
        project_details = list(ProjectDetails.objects.all())
        news_items = list(News.objects.all())

        self.assertEqual(len(projects), 0)
        self.assertEqual(len(project_details), 0)
        self.assertEqual(len(news_items), 0)
