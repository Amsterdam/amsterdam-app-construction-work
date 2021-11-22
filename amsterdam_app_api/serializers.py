from rest_framework import serializers
from amsterdam_app_api.models import Assets
from amsterdam_app_api.models import Image
from amsterdam_app_api.models import Projects
from amsterdam_app_api.models import ProjectDetails
from amsterdam_app_api.models import News
from amsterdam_app_api.models import ProjectManager
from amsterdam_app_api.models import MobileDevices
from amsterdam_app_api.models import WarningMessages
from amsterdam_app_api.models import Notification


class AssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assets
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'


class ProjectDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDetails
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class ProjectManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectManager
        fields = '__all__'


class MobileDevicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileDevices
        fields = '__all__'


class WarningMessagesInternalSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarningMessages
        fields = '__all__'


class WarningMessagesExternalSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarningMessages
        exclude = ['project_manager_id']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        exclude = ['identifier']
