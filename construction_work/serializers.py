""" Serializers for DB models """
from rest_framework import serializers

from construction_work.models import (
    Article,
    Asset,
    Image,
    Notification,
    Project,
    ProjectManager,
    WarningMessage,
)


class AssetsSerializer(serializers.ModelSerializer):
    """Assets serializer (pdf's)"""

    class Meta:
        model = Asset
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    """Image serializer (iprox images)"""

    class Meta:
        model = Image
        fields = "__all__"


class ProjectsSerializer(serializers.ModelSerializer):
    """Project pages serializer"""

    class Meta:
        model = Project
        fields = "__all__"

    def get_field_names(self, *args, **kwargs):
        field_names = self.context.get("fields", None)
        if field_names:
            return field_names
        return super(ProjectsSerializer, self).get_field_names(*args, **kwargs)


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
        model = WarningMessage
        fields = "__all__"


class WarningMessagesExternalSerializer(serializers.ModelSerializer):
    """warning messages (external) serializer"""

    class Meta:
        model = WarningMessage
        exclude = ["project_manager_id"]


class NotificationSerializer(serializers.ModelSerializer):
    """notifications serializer"""

    class Meta:
        model = Notification
        fields = "__all__"
