""" Serializers for DB models """
from rest_framework import serializers

from amsterdam_app_api.models import (
    Article,
    Assets,
    Image,
    Notification,
    ProjectDetails,
    ProjectManager,
    Projects,
    WarningMessages,
)


class AssetsSerializer(serializers.ModelSerializer):
    """Assets serializer (pdf's)"""

    class Meta:
        model = Assets
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    """Image serializer (iprox images)"""

    class Meta:
        model = Image
        fields = "__all__"


class ProjectsSerializer(serializers.ModelSerializer):
    """Project pages serializer"""

    class Meta:
        model = Projects
        fields = "__all__"

    def get_field_names(self, *args, **kwargs):
        field_names = self.context.get("fields", None)
        if field_names:
            return field_names
        return super(ProjectsSerializer, self).get_field_names(*args, **kwargs)


class ProjectDetailsSerializer(serializers.ModelSerializer):
    """Project details serializer"""

    class Meta:
        model = ProjectDetails
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    """Project news serializer"""

    class Meta:
        model = Article
        exclude = ["id"]


class ProjectManagerSerializer(serializers.ModelSerializer):
    """Project managers serializer"""

    class Meta:
        model = ProjectManager
        fields = "__all__"


class WarningMessagesInternalSerializer(serializers.ModelSerializer):
    """warning messages (internal VUE) serializer"""

    class Meta:
        model = WarningMessages
        fields = "__all__"


class WarningMessagesExternalSerializer(serializers.ModelSerializer):
    """warning messages (external) serializer"""

    class Meta:
        model = WarningMessages
        exclude = ["project_manager_id"]


class NotificationSerializer(serializers.ModelSerializer):
    """notifications serializer"""

    class Meta:
        model = Notification
        fields = "__all__"
