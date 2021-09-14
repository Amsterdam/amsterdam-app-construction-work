from django.test import TestCase
from amsterdam_app_api.UNITTESTS.mock_data import TestData
from amsterdam_app_api.models import Assets
from amsterdam_app_api.models import Image
from amsterdam_app_api.models import Projects
from amsterdam_app_api.models import ProjectDetails
from amsterdam_app_api.models import News
from amsterdam_app_api.models import OM
from amsterdam_app_api.serializers import ImageSerializer
from amsterdam_app_api.serializers import AssetsSerializer
from amsterdam_app_api.serializers import ProjectsSerializer
from amsterdam_app_api.serializers import ProjectDetailsSerializer
from amsterdam_app_api.serializers import NewsSerializer
from amsterdam_app_api.serializers import OMSerializer


class TestAssetsModel(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestAssetsModel, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        Assets.objects.all().delete()
        for asset in self.data.assets:
            Assets.objects.create(**asset)

    def test_asset_delete(self):
        Assets.objects.get(pk='0000000000').delete()
        asset_objects = Assets.objects.all()
        serializer = AssetsSerializer(asset_objects, many=True)

        self.assertEqual(len(serializer.data), 1)

    def test_asset_get_all(self):
        asset_objects = Assets.objects.all()

        self.assertEqual(len(asset_objects), 2)

    def test_asset_exists(self):
        asset = Assets.objects.get(pk='0000000000')

        self.assertEqual(asset.identifier, '0000000000')
        self.assertEqual(asset.url, 'https://localhost/test0.pdf')
        self.assertEqual(asset.mime_type, 'application/pdf')
        self.assertEqual(asset.data, b'')

    def test_asset_does_not_exist(self):
        asset = Assets.objects.filter(pk='not-there').first()

        self.assertEqual(asset, None)


class TestImageModel(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestImageModel, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        Image.objects.all().delete()
        for image in self.data.images:
            Image.objects.create(**image)

    def test_image_delete(self):
        Image.objects.get(pk='0000000000').delete()
        image_objects = Image.objects.all()
        serializer = ImageSerializer(image_objects, many=True)

        self.assertEqual(len(serializer.data), 1)

    def test_image_get_all(self):
        image_objects = Image.objects.all()

        self.assertEqual(len(image_objects), 2)

    def test_image_exists(self):
        image_object = Image.objects.get(pk='0000000000')

        self.assertEqual(image_object.identifier, '0000000000')
        self.assertEqual(image_object.size, 'orig')
        self.assertEqual(image_object.url, 'https://localhost/image0.jpg')
        self.assertEqual(image_object.filename, 'image.jpg')
        self.assertEqual(image_object.description, '')
        self.assertEqual(image_object.mime_type, 'image/jpg')
        self.assertEqual(image_object.data, b'')

    def test_image_does_not_exist(self):
        image = Image.objects.filter(pk='does not exist').first()

        self.assertEqual(image, None)


class TestProjectsModel(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestProjectsModel, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        Projects.objects.all().delete()
        for project in self.data.projects:
            Projects.objects.create(**project)

    def test_projects_delete(self):
        Projects.objects.filter(pk='0000000000').delete()
        project_objects = Projects.objects.all()
        serializer = ProjectsSerializer(project_objects, many=True)

        self.assertEqual(len(serializer.data), 1)

    def test_projects_get_all(self):
        project_objects = Projects.objects.all()
        serializer = ProjectsSerializer(project_objects, many=True)

        self.assertEqual(serializer.data, self.data.projects)

    def test_projects_does_exist(self):
        projects_objects = Projects.objects.filter(pk='0000000000').first()
        serializer = ProjectsSerializer(projects_objects)

        self.assertEqual(serializer.data, self.data.projects[0])

    def test_projects_does_not_exist(self):
        projects_objects = Projects.objects.filter(pk='does not exist').first()

        self.assertEqual(projects_objects, None)


class TestProjectDetailsModel(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestProjectDetailsModel, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        ProjectDetails.objects.all().delete()
        for project in self.data.project_details:
            ProjectDetails.objects.create(**project)

    def test_projects_delete(self):
        ProjectDetails.objects.filter(pk='0000000000').delete()
        project_objects = ProjectDetails.objects.all()
        serializer = ProjectDetailsSerializer(project_objects, many=True)

        self.assertEqual(len(serializer.data), 1)

    def test_project_details_get_all(self):
        project_objects = ProjectDetails.objects.all()
        serializer = ProjectDetailsSerializer(project_objects, many=True)

        self.assertEqual(serializer.data, self.data.project_details)

    def test_project_details_does_exist(self):
        project_objects = ProjectDetails.objects.filter(pk='0000000000').first()
        serializer = ProjectDetailsSerializer(project_objects)

        self.assertEqual(serializer.data, self.data.project_details[0])

    def test_project_details_does_not_exist(self):
        project_objects = ProjectDetails.objects.filter(pk='does not exist').first()

        self.assertEqual(project_objects, None)


class TestNewsModel(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestNewsModel, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        News.objects.all().delete()
        for news in self.data.news:
            News.objects.create(**news)

    def test_news_delete(self):
        News.objects.get(pk='0000000000').delete()
        news_objects = News.objects.all()
        serializer = NewsSerializer(news_objects, many=True)

        self.assertEqual(len(serializer.data), 1)

    def test_news_get_all(self):
        news_objects = News.objects.all()
        serializer = NewsSerializer(news_objects, many=True)

        self.assertEqual(len(serializer.data), 2)

    def test_news_exists(self):
        news_object = News.objects.get(pk='0000000000')
        serializer = NewsSerializer(news_object)

        self.assertEqual(serializer.data, self.data.news[0])

    def test_news_does_not_exist(self):
        news_object = News.objects.filter(pk='does not exist').first()

        self.assertEqual(news_object, None)


class TestOMModel(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestOMModel, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        OM.objects.all().delete()
        for om in self.data.om:
            OM.objects.create(**om)

    def test_om_delete(self):
        OM.objects.get(pk='56d7f0b9-ac14-424d-8779-615a60c23591').delete()
        om_objects = OM.objects.all()
        serializer = OMSerializer(om_objects, many=True)

        self.assertEqual(len(serializer.data), 1)

    def test_om_get_all(self):
        om_objects = OM.objects.all()

        self.assertEqual(len(om_objects), 2)

    def test_om_exists(self):
        om_objects = OM.objects.get(pk='56d7f0b9-ac14-424d-8779-615a60c23591')

        self.assertEqual(om_objects.identifier, '56d7f0b9-ac14-424d-8779-615a60c23591')
        self.assertEqual(om_objects.email, 'mock0@example.com')
        self.assertEqual(om_objects.projects, ["0000000000", "0000000001"])

    def test_om_does_not_exist(self):
        om_object = OM.objects.filter(pk='does not exist').first()

        self.assertEqual(om_object, None)
