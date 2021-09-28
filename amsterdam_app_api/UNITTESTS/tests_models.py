import uuid
from django.test import TestCase
from amsterdam_app_api.UNITTESTS.mock_data import TestData
from amsterdam_app_api.models import Assets
from amsterdam_app_api.models import Image
from amsterdam_app_api.models import Projects
from amsterdam_app_api.models import ProjectDetails
from amsterdam_app_api.models import News
from amsterdam_app_api.models import ProjectManager
from amsterdam_app_api.models import MobileDevices
from amsterdam_app_api.serializers import ImageSerializer
from amsterdam_app_api.serializers import AssetsSerializer
from amsterdam_app_api.serializers import ProjectsSerializer
from amsterdam_app_api.serializers import ProjectDetailsSerializer
from amsterdam_app_api.serializers import NewsSerializer
from amsterdam_app_api.serializers import ProjectManagerSerializer
from amsterdam_app_api.serializers import MobileDevicesSerializer


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


class TestProjectManagerModel(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestProjectManagerModel, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        ProjectManager.objects.all().delete()
        for pm in self.data.project_manager:
            ProjectManager.objects.create(**pm)

    def test_pm_delete(self):
        ProjectManager.objects.get(pk=uuid.UUID('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa')).delete()
        pm_objects = ProjectManager.objects.all()
        serializer = ProjectManagerSerializer(pm_objects, many=True)

        self.assertEqual(len(serializer.data), 1)

    def test_pm_get_all(self):
        pm_objects = ProjectManager.objects.all()

        self.assertEqual(len(pm_objects), 2)

    def test_pm_exists(self):
        pm_objects = ProjectManager.objects.get(pk=uuid.UUID('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'))

        self.assertEqual(pm_objects.identifier, uuid.UUID('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'))
        self.assertEqual(pm_objects.email, 'mock0@amsterdam.nl')
        self.assertEqual(pm_objects.projects, ["0000000000", "0000000001"])

    def test_pm_does_not_exist(self):
        pm_object = ProjectManager.objects.filter(pk=uuid.UUID('00000000-0000-0000-0000-000000000000')).first()

        self.assertEqual(pm_object, None)

    def test_pm_has_invalid_email(self):
        with self.assertRaises(Exception) as context:
            ProjectManager.objects.create(**self.data.project_manager_invalid)

        self.assertEqual(context.exception.args, ('Invalid email, should be <username>@amsterdam.nl',))


class TestMobileDevicesModel(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestMobileDevicesModel, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        MobileDevices.objects.all().delete()
        for mobile_device in self.data.mobile_devices:
            MobileDevices.objects.create(**mobile_device)

    def test_md_delete(self):
        MobileDevices.objects.get(pk=uuid.UUID('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa')).delete()
        md_objects = MobileDevices.objects.all()
        serializer = MobileDevicesSerializer(md_objects, many=True)

        self.assertEqual(len(serializer.data), 1)

    def test_md_get_all(self):
        md_objects = MobileDevices.objects.all()

        self.assertEqual(len(md_objects), 2)

    def test_md_exists(self):
        md_objects = MobileDevices.objects.get(pk='aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa')

        self.assertEqual(md_objects.identifier, 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa')
        self.assertEqual(md_objects.os_type, 'android')
        self.assertEqual(md_objects.projects, ["0000000000", "0000000001"])

    def test_md_does_not_exist(self):
        md_object = MobileDevices.objects.filter(pk='00000000-0000-0000-0000-000000000000').first()

        self.assertEqual(md_object, None)
