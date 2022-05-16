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
from amsterdam_app_api.models import CityContact
from amsterdam_app_api.models import CityOffice
from amsterdam_app_api.models import CityOffices
from amsterdam_app_api.models import Modules
from amsterdam_app_api.models import ModulesByApp
from amsterdam_app_api.models import ModuleOrder


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

    def get_field_names(self, *args, **kwargs):
        field_names = self.context.get('fields', None)
        if field_names:
            return field_names
        return super(ProjectsSerializer, self).get_field_names(*args, **kwargs)


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
        fields = '__all__'


class CityContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityContact
        exclude = ['id']


class CityOfficesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityOffices
        exclude = ['id']


class CityOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityOffice
        fields = '__all__'


class ModulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modules
        fields = '__all__'


class ModulesByAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModulesByApp
        fields = '__all__'


class ModuleOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleOrder
        fields = '__all__'
