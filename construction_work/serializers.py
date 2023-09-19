""" Serializers for DB models """
from rest_framework import serializers
from rest_framework.fields import empty
from construction_work.generic_functions.distance import GeoPyDistance

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


class ProjectCreateSerializer(serializers.ModelSerializer):
    """Project create serializer"""

    class Meta:
        model = Project
        fields = "__all__"


class ProjectDetailsSerializer(serializers.ModelSerializer):
    """Project details serializer"""

    # NOTE: remove when frontend has implemented project_id
    identifier = serializers.CharField(source="project_id")
    
    district_name = serializers.SerializerMethodField()
    source_url = serializers.SerializerMethodField()
    meter = serializers.SerializerMethodField()
    strides = serializers.SerializerMethodField()

    # TODO: followers, followed, recent_articles > via relationships with other models

    class Meta:
        model = Project
        fields = "__all__"

    def __init__(self, instance=None, data={}, **kwargs):
        super().__init__(instance, data, **kwargs)

        self.distance = None
        lat = self.context.get("lat")
        lon = self.context.get("lon")
        if lat is not None and lon is not None:
            self.distance = self.get_distance_from_project(lat, lon, instance)

    def get_field_names(self, *args, **kwargs):
        field_names = self.context.get("fields", None)
        if field_names:
            return field_names
        return super().get_field_names(*args, **kwargs)

    def get_district_name(self, obj: Project):
        return DISTRICTS.get(obj.district_id)

    def get_source_url(self, obj: Project):
        return f"https://amsterdam.nl/@{obj.project_id}/page/?AppIdt=app-pagetype&reload=true"

    def get_meter(self, _):
        if self.distance:
            return self.distance.meter
        return None

    def get_strides(self, _):
        if self.distance:
            return self.distance.strides
        return None

    def get_distance_from_project(self, lat: float, lon: float, obj: Project):
        cords_1 = (float(lat), float(lon))
        cords_2 = (obj.coordinates.get("lat"), obj.coordinates.get("lon"))
        if None in cords_2:
            cords_2 = (None, None)
        elif (0, 0) == cords_2:
            cords_2 = (None, None)
        distance = GeoPyDistance(cords_1, cords_2)
        return distance


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
