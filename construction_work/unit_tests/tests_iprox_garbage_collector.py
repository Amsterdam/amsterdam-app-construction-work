""" unit_tests """

import datetime

from django.test import TestCase

from construction_work.garbage_collector.garbage_collector import GarbageCollector
from construction_work.models import Article, Project, ProjectDetail, ProjectManager
from construction_work.unit_tests.mock_data import TestData


class TestGarbageCollector(TestCase):
    """test for garbage collector"""

    def __init__(self, *args, **kwargs):
        super(TestGarbageCollector, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        """setup test db"""
        Project.objects.all().delete()
        for project in self.data.projects:
            Project.objects.create(**project)

        ProjectDetail.objects.all().delete()
        for project_detail in self.data.project_details:
            try:
                project = Project.objects.filter(pk=project_detail["identifier"]).first()
                project_detail["identifier"] = project
                ProjectDetail.objects.create(**project_detail)
            except Exception as error:
                print(error)

        Article.objects.all().delete()
        for news in self.data.article:
            project = Project.objects.filter(pk=news["project_identifier"]).first()
            news["project_identifier"] = project
            Article.objects.create(**news)

        ProjectManager.objects.all().delete()
        for project_manager in self.data.project_manager:
            ProjectManager.objects.create(**project_manager)

    def test_no_objects_changed(self):
        """test with no objects changed"""
        gc = GarbageCollector(last_scrape_time=(datetime.datetime.now() - datetime.timedelta(hours=1)))
        gc.collect_iprox(project_type="brug")
        projects = list(Project.objects.all())
        project_details = list(ProjectDetail.objects.all())
        news_items = list(Article.objects.all())

        for project in projects:
            self.assertEqual(project.active, True)

        for project in project_details:
            self.assertEqual(project.active, True)

        for item in news_items:
            self.assertEqual(item.active, True)

    def test_all_objects_inactive(self):
        """test if all objects are inactive"""
        gc = GarbageCollector(last_scrape_time=datetime.datetime.now())
        gc.collect_iprox(project_type="brug")
        gc.collect_iprox(project_type="kade")
        projects = list(Project.objects.all())
        project_details = list(ProjectDetail.objects.all())
        news_items = list(Article.objects.all())

        for project in projects:
            self.assertEqual(project.active, False)

        for project in project_details:
            self.assertEqual(project.active, False)

        for item in news_items:
            self.assertEqual(item.active, False)

    def test_all_objects_deleted(self):
        """test that all objects are deleted"""
        gc = GarbageCollector(last_scrape_time=(datetime.datetime.now() + datetime.timedelta(days=7)))
        gc.collect_iprox(project_type="brug")
        gc.collect_iprox(project_type="kade")
        projects = list(Project.objects.all())
        project_details = list(ProjectDetail.objects.all())
        news_items = list(Article.objects.all())

        self.assertEqual(len(projects), 0)
        self.assertEqual(len(project_details), 0)
        self.assertEqual(len(news_items), 0)
