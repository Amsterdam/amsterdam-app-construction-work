""" UNITTESTS """

import uuid
from django.test import TestCase
from amsterdam_app_api.UNITTESTS.mock_data import TestData
from amsterdam_app_api.models import Assets
from amsterdam_app_api.models import Image
from amsterdam_app_api.models import Projects
from amsterdam_app_api.models import ProjectDetails
from amsterdam_app_api.models import News
from amsterdam_app_api.models import ProjectManager
from amsterdam_app_api.models import WarningMessages
from amsterdam_app_api.models import FirebaseTokens
from amsterdam_app_api.serializers import ImageSerializer
from amsterdam_app_api.serializers import AssetsSerializer
from amsterdam_app_api.serializers import ProjectsSerializer
from amsterdam_app_api.serializers import ProjectDetailsSerializer
from amsterdam_app_api.serializers import NewsSerializer
from amsterdam_app_api.serializers import ProjectManagerSerializer
from amsterdam_app_api.serializers import WarningMessagesInternalSerializer
from amsterdam_app_api.serializers import WarningMessagesExternalSerializer
from amsterdam_app_api.serializers import Notification


class TestAssetsModel(TestCase):
    """ UNITTESTS """
    def __init__(self, *args, **kwargs):
        super(TestAssetsModel, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        """ UNITTEST DB setup """
        Assets.objects.all().delete()
        for asset in self.data.assets:
            Assets.objects.create(**asset)

    def test_asset_delete(self):
        """ test delete """
        Assets.objects.get(pk='0000000000').delete()
        asset_objects = Assets.objects.all()
        serializer = AssetsSerializer(asset_objects, many=True)

        self.assertEqual(len(serializer.data), 1)

    def test_asset_get_all(self):
        """ test retrieve """
        asset_objects = Assets.objects.all()
        self.assertEqual(len(asset_objects), 2)

    def test_asset_exists(self):
        """ test exist """
        asset = Assets.objects.get(pk='0000000000')

        self.assertEqual(asset.identifier, '0000000000')
        self.assertEqual(asset.url, 'https://localhost/test0.pdf')
        self.assertEqual(asset.mime_type, 'application/pdf')
        self.assertEqual(asset.data, b'')

    def test_asset_does_not_exist(self):
        """ test not exist """
        asset = Assets.objects.filter(pk='not-there').first()

        self.assertEqual(asset, None)


class TestImageModel(TestCase):
    """ UNITTESTS """
    def __init__(self, *args, **kwargs):
        super(TestImageModel, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        """ UNITTESTS setup """
        Image.objects.all().delete()
        for image in self.data.images:
            Image.objects.create(**image)

    def test_image_delete(self):
        """ test delete """
        Image.objects.get(pk='0000000000').delete()
        image_objects = Image.objects.all()
        serializer = ImageSerializer(image_objects, many=True)

        self.assertEqual(len(serializer.data), 1)

    def test_image_get_all(self):
        """ test retrieve """
        image_objects = Image.objects.all()

        self.assertEqual(len(image_objects), 2)

    def test_image_exists(self):
        """ test exist """
        image_object = Image.objects.get(pk='0000000000')

        self.assertEqual(image_object.identifier, '0000000000')
        self.assertEqual(image_object.size, 'orig')
        self.assertEqual(image_object.url, 'https://localhost/image0.jpg')
        self.assertEqual(image_object.filename, 'image.jpg')
        self.assertEqual(image_object.description, '')
        self.assertEqual(image_object.mime_type, 'image/jpg')
        self.assertEqual(image_object.data, b'')

    def test_image_does_not_exist(self):
        """ test not exist """
        image = Image.objects.filter(pk='does not exist').first()

        self.assertEqual(image, None)


class TestProjectsModel(TestCase):
    """ UNITTESTS """
    def __init__(self, *args, **kwargs):
        super(TestProjectsModel, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        """ UNITTESTS db setup """
        Projects.objects.all().delete()
        for project in self.data.projects:
            Projects.objects.create(**project)

    def test_projects_delete(self):
        """ test delete """
        Projects.objects.filter(pk='0000000000').delete()
        project_objects = Projects.objects.all()
        serializer = ProjectsSerializer(project_objects, many=True)

        self.assertEqual(len(serializer.data), 1)

    def test_projects_get_all(self):
        """ test retrieve """
        project_objects = Projects.objects.all()
        serializer = ProjectsSerializer(project_objects, many=True)
        for i in range(0, len(serializer.data), 1):
            self.data.projects[i]['last_seen'] = serializer.data[i]['last_seen']

        self.assertEqual(serializer.data, self.data.projects)

    def test_projects_does_exist(self):
        """ test exist """
        projects_objects = Projects.objects.filter(pk='0000000000').first()
        serializer = ProjectsSerializer(projects_objects)
        self.data.projects[0]['last_seen'] = serializer.data['last_seen']

        self.assertEqual(serializer.data, self.data.projects[0])

    def test_projects_does_not_exist(self):
        """ test not exist """
        projects_objects = Projects.objects.filter(pk='does not exist').first()

        self.assertEqual(projects_objects, None)


class TestProjectDetailsModel(TestCase):
    """ UNITTESTS """
    def __init__(self, *args, **kwargs):
        super(TestProjectDetailsModel, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        """ UNITTESTS db setup """
        Projects.objects.all().delete()
        for project in self.data.projects:
            Projects.objects.create(**project)

        ProjectDetails.objects.all().delete()
        for project_detail in self.data.project_details:
            project_detail['identifier'] = Projects.objects.filter(
                pk=project_detail['identifier']
            ).first()
            ProjectDetails.objects.create(**project_detail)

    def test_projects_delete(self):
        """ test delete """
        ProjectDetails.objects.filter(pk='0000000000').delete()
        project_objects = ProjectDetails.objects.all()
        serializer = ProjectDetailsSerializer(project_objects, many=True)

        self.assertEqual(len(serializer.data), 1)

    def test_project_details_get_all(self):
        """ test retrieve """
        project_objects = ProjectDetails.objects.all()
        data = ProjectDetailsSerializer(project_objects, many=True).data
        for i in range(0, len(data), 1):
            self.data.project_details[i]['last_seen'] = data[i]['last_seen']
        self.data.project_details = ProjectDetailsSerializer(self.data.project_details, many=True).data

        self.assertEqual(data, self.data.project_details)

    def test_project_details_does_exist(self):
        """ test exist """
        project_objects = ProjectDetails.objects.filter(pk='0000000000').first()
        data = ProjectDetailsSerializer(project_objects, many=False).data
        self.data.project_details[0]['last_seen'] = data['last_seen']
        original_data = ProjectDetailsSerializer(self.data.project_details[0], many=False).data
        self.assertEqual(data, original_data)

    def test_project_details_does_not_exist(self):
        """ test not exist """
        project_objects = ProjectDetails.objects.filter(pk='does not exist').first()

        self.assertEqual(project_objects, None)


class TestNewsModel(TestCase):
    """ UNITTESTS """
    def __init__(self, *args, **kwargs):
        super(TestNewsModel, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        """ UNITTESTS db setup """
        Projects.objects.all().delete()
        for project in self.data.projects:
            Projects.objects.create(**project)

        News.objects.all().delete()
        for news in self.data.news:
            news['project_identifier'] = Projects.objects.filter(pk=news['project_identifier']).first()
            News.objects.create(**news)

    def test_news_delete(self):
        """ test delete """
        News.objects.get(identifier='0000000000', project_identifier='0000000000').delete()
        news_objects = News.objects.all()
        serializer = NewsSerializer(news_objects, many=True)

        self.assertEqual(len(serializer.data), 1)

    def test_news_get_all(self):
        """ test retrieve """
        news_objects = News.objects.all()
        serializer = NewsSerializer(news_objects, many=True)

        self.assertEqual(len(serializer.data), 2)

    def test_news_exists(self):
        """ test exist """
        news_object = News.objects.get(identifier='0000000000', project_identifier='0000000000')
        serializer = NewsSerializer(news_object)
        self.data.news[0]['last_seen'] = serializer.data['last_seen']

        self.assertEqual(self.data.news[0]['active'], True)

    def test_news_does_not_exist(self):
        """ test not exist """
        news_object = News.objects.filter(identifier='does not exist', project_identifier='0000000000').first()

        self.assertEqual(news_object, None)


class TestProjectManagerModel(TestCase):
    """ UNITTESTS """
    def __init__(self, *args, **kwargs):
        super(TestProjectManagerModel, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        """ UNITTESTS db setup """
        ProjectManager.objects.all().delete()
        for pm in self.data.project_manager:
            ProjectManager.objects.create(**pm)

    def test_pm_delete(self):
        """ test delete """
        ProjectManager.objects.get(pk=uuid.UUID('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa')).delete()
        pm_objects = ProjectManager.objects.all()
        serializer = ProjectManagerSerializer(pm_objects, many=True)

        self.assertEqual(len(serializer.data), 1)

    def test_pm_get_all(self):
        """ test retrieve """
        pm_objects = ProjectManager.objects.all()

        self.assertEqual(len(pm_objects), 2)

    def test_pm_exists(self):
        """ test exist """
        pm_objects = ProjectManager.objects.get(pk=uuid.UUID('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'))

        self.assertEqual(pm_objects.identifier, uuid.UUID('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'))
        self.assertEqual(pm_objects.email, 'mock0@amsterdam.nl')
        self.assertEqual(pm_objects.projects, ["0000000000"])

    def test_pm_does_not_exist(self):
        """ test not exist """
        pm_object = ProjectManager.objects.filter(pk=uuid.UUID('00000000-0000-0000-0000-000000000000')).first()

        self.assertEqual(pm_object, None)

    def test_pm_has_invalid_email(self):
        """ test email """
        with self.assertRaises(Exception) as context:
            ProjectManager.objects.create(**self.data.project_manager_invalid)

        self.assertEqual(context.exception.args, ('Invalid email, should be <username>@amsterdam.nl',))


class TestFirebaseTokenModel(TestCase):
    """ UNITTESTS """
    def __init__(self, *args, **kwargs):
        super(TestFirebaseTokenModel, self).__init__(*args, **kwargs)
        self.data = [{'deviceid': '0', 'firebasetoken': '0', 'os': 'ios'},
                     {'deviceid': '1', 'firebasetoken': '1', 'os': 'ios'}]

    def setUp(self):
        """ UNITTESTS db setup """
        FirebaseTokens.objects.all().delete()
        for token in self.data:
            FirebaseTokens.objects.create(**token)

    def test_fb_delete(self):
        """ test delete """
        FirebaseTokens.objects.get(pk='0').delete()
        fb_objects = FirebaseTokens.objects.all()

        self.assertEqual(len(fb_objects), 1)

    def test_fb_get_all(self):
        """ test retrieve """
        fb_objects = FirebaseTokens.objects.all()

        self.assertEqual(len(fb_objects), 2)

    def test_fb_exists(self):
        """ test exist """
        fb_objects = FirebaseTokens.objects.get(pk='0')

        self.assertEqual(fb_objects.firebasetoken, '0')
        self.assertEqual(fb_objects.os, 'ios')
        self.assertEqual(fb_objects.deviceid, '0')

    def test_fb_does_not_exist(self):
        """ test not exist """
        fb_object = FirebaseTokens.objects.filter(pk='00000000-0000-0000-0000-000000000000').first()

        self.assertEqual(fb_object, None)


class TestWarningMessagesModel(TestCase):
    """ UNITTESTS """
    def __init__(self, *args, **kwargs):
        super(TestWarningMessagesModel, self).__init__(*args, **kwargs)
        self.data = TestData()

    def setUp(self):
        """ Setup test db """
        Projects.objects.all().delete()
        for project in self.data.projects:
            Projects.objects.create(**project)

        WarningMessages.objects.all().delete()
        ProjectManager.objects.all().delete()
        for project_manager in self.data.project_manager:
            ProjectManager.objects.create(**project_manager)

    def test_create_message(self):
        """ Test create warning message """
        self.data.warning_message['project_identifier'] = Projects.objects.filter(
            pk=self.data.warning_message['project_identifier']
        ).first()
        warning_message = WarningMessages.objects.create(**self.data.warning_message)

        self.assertEqual(type(warning_message.identifier), type(uuid.uuid4()))
        self.assertEqual(warning_message.author_email, self.data.project_manager[0]['email'])
        self.assertNotEqual(warning_message.publication_date, None)
        self.assertNotEqual(warning_message.modification_date, None)

    def test_default_email(self):
        """ Test default email on creation """
        data = dict(self.data.warning_message)
        data['project_manager_id'] = uuid.uuid4()
        data['project_identifier'] = Projects.objects.filter(
            pk=data['project_identifier']
        ).first()
        warning_message = WarningMessages.objects.create(**data)

        self.assertEqual(warning_message.author_email, 'redactieprojecten@amsterdam.nl')

    def test_modification_date(self):
        """ test modification date on changing a message """
        self.data.warning_message['project_identifier'] = Projects.objects.filter(
            pk=self.data.warning_message['project_identifier']
        ).first()
        warning_message = WarningMessages.objects.create(**self.data.warning_message)
        date = warning_message.modification_date
        warning_message.save()

        self.assertNotEqual(warning_message.modification_date, date)

    def test_serializer_internal(self):
        """ Purpose: test if project_manager_id is present in serializer
        """
        self.data.warning_message['project_identifier'] = Projects.objects.filter(
            pk=self.data.warning_message['project_identifier']
        ).first()
        warning_message = WarningMessages.objects.create(**self.data.warning_message)
        serializer = WarningMessagesInternalSerializer(warning_message, many=False)
        data = dict(serializer.data)
        expected_result = {
            'identifier': data['identifier'],
            'title': 'title',
            'body': 'Body text',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'images': [],
            'publication_date': data['publication_date'],
            'modification_date': data['modification_date'],
            'author_email': 'mock0@amsterdam.nl'
        }

        self.assertDictEqual(data, expected_result)

    def test_serializer_external(self):
        """ Purpose: test if project_manager_id is NOT present in serializer
        """
        self.data.warning_message['project_identifier'] = Projects.objects.filter(
            pk=self.data.warning_message['project_identifier']
        ).first()
        warning_message = WarningMessages.objects.create(**self.data.warning_message)
        serializer = WarningMessagesExternalSerializer(warning_message, many=False)
        data = dict(serializer.data)
        expected_result = {
            'identifier': data['identifier'],
            'title': 'title',
            'body': 'Body text',
            'project_identifier': '0000000000',
            'images': [],
            'publication_date': data['publication_date'],
            'modification_date': data['modification_date'],
            'author_email': 'mock0@amsterdam.nl'
        }

        self.assertDictEqual(data, expected_result)


class TestNotificationModel(TestCase):
    """ UNITTESTS """
    def __init__(self, *args, **kwargs):
        super(TestNotificationModel, self).__init__(*args, **kwargs)
        self.data = TestData()
        self.warning_identifier = None

    def setUp(self):
        """ Setup test db """
        Projects.objects.all().delete()
        for project in self.data.projects:
            Projects.objects.create(**project)

        WarningMessages.objects.all().delete()
        self.data.warning_message['project_identifier'] = Projects.objects.filter(
            pk=self.data.warning_message['project_identifier']
        ).first()
        warning_message = WarningMessages.objects.create(**self.data.warning_message)
        self.warning_identifier = warning_message.identifier

    def test_create_notification(self):
        """ Create a notification """
        data = {'title': 'test', 'body': 'test', 'warning_identifier': self.warning_identifier}
        notification = Notification.objects.create(**data)
        notification.save()
        data = NewsSerializer(notification, many=False).data

        self.assertEqual(data['project_identifier'], '0000000000')

    def test_serializer(self):
        """ Test the serializer for notification messages """
        data = {'title': 'test', 'body': 'test', 'warning_identifier': self.warning_identifier}
        notification = Notification.objects.create(**data)
        serializer = NewsSerializer(notification, many=False)
        serializer_data = dict(serializer.data)

        expected_result = {
            'identifier': str(notification.identifier),
            'project_identifier': '0000000000',
            'title': 'test',
            'publication_date': str(notification.publication_date),
            'body': 'test',
            'images': None,
            'assets': None,
            'last_seen': None
        }

        self.assertDictEqual(serializer_data, expected_result)
