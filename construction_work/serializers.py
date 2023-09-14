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
from construction_work.models.project import DISTRICTS


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


class ProjectSerializer(serializers.ModelSerializer):
    """Project pages serializer"""

    # NOTE: remove when frontend has implemented project_id
    identifier = serializers.SerializerMethodField()
    district_name = serializers.SerializerMethodField()
    source_url = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = "__all__"

    def get_identifier(self, obj):
        """Set identifier value for frontend"""
        return obj.project_id

    def get_district_name(self, obj):
        """Find district name by id"""
        return DISTRICTS.get(obj.district_id)

    def get_source_url(self, obj):
        """Build source URL from project id"""
        return f"https://amsterdam.nl/@{obj.project_id}/page/?AppIdt=app-pagetype&reload=true"

    def get_field_names(self, *args, **kwargs):
        field_names = self.context.get("fields", None)
        if field_names:
            return field_names
        return super(ProjectSerializer, self).get_field_names(*args, **kwargs)


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
