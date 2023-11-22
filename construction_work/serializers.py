""" Serializers for DB models """
from ast import List

from rest_framework import serializers

from construction_work.generic_functions.gps_utils import get_distance
from construction_work.generic_functions.project_utils import (
    get_recent_articles_of_project,
)
from construction_work.models import (
    Article,
    Image,
    Notification,
    Project,
    ProjectManager,
    WarningMessage,
)
from construction_work.models.device import Device
from construction_work.models.warning_and_notification import WarningImage


class ImageSerializer(serializers.ModelSerializer):
    """Image serializer (iprox images)"""

    class Meta:
        model = Image
        fields = "__all__"


class ImagePublicSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ["url", "width", "height"]

    def get_url(self, obj: Image):
        base_url = self.context.get("base_url")
        if base_url is None:
            return None
        return f"{base_url}image?id={obj.pk}"


class ProjectSerializer(serializers.ModelSerializer):
    """Project create serializer"""

    class Meta:
        model = Project
        fields = "__all__"


class ProjectListSerializer(serializers.ModelSerializer):
    """Project list serializer"""

    meter = serializers.SerializerMethodField()
    strides = serializers.SerializerMethodField()
    followed = serializers.SerializerMethodField()
    recent_articles = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "subtitle",
            "image",
            "followed",
            "meter",
            "strides",
            "recent_articles",
        ]

    def get_distance_from_project(self, lat: float, lon: float, obj: Project):
        """Get distance from project"""
        if obj is None:
            return None

        cords_1 = lat, lon
        project_coordinates = obj.coordinates
        if project_coordinates is None:
            project_coordinates = {"lat": None, "lon": None}
        cords_2 = (project_coordinates.get("lat"), project_coordinates.get("lon"))
        if None in cords_2:
            cords_2 = (None, None)
        elif (0, 0) == cords_2:
            cords_2 = (None, None)
        meter, strides = get_distance(cords_1, cords_2)
        return meter, strides

    def get_meter(self, obj: Project) -> int:
        """Given location away from project in meters"""
        lat = self.context.get("lat")
        lon = self.context.get("lon")

        distance = self.get_distance_from_project(lat, lon, obj)
        return distance[0]

    def get_strides(self, obj: Project) -> int:
        """Given location away from project in strides"""
        lat = self.context.get("lat")
        lon = self.context.get("lon")

        distance = self.get_distance_from_project(lat, lon, obj)
        return distance[1]

    def get_followed(self, obj: Project) -> bool:
        """Check if project is being followed by given device"""
        followed_projects = self.context.get("followed_projects")
        if followed_projects is None:
            return None

        return obj.pk in [x.pk for x in followed_projects]

    def get_recent_articles(self, obj: Project) -> dict:
        project_news_mapping = self.context.get("project_news_mapping")
        if project_news_mapping is None:
            return []

        return project_news_mapping[obj.pk]


class ProjectDetailsSerializer(ProjectListSerializer):
    """Project details serializer"""

    followers = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = "__all__"

    def get_field_names(self, *args, **kwargs):
        field_names = self.context.get("fields", None)
        if field_names:
            return field_names
        return super().get_field_names(*args, **kwargs)

    def get_followers(self, obj: Project) -> int:
        """Get amount of followers of project"""
        return obj.device_set.count()

    def get_recent_articles(self, obj: Project) -> list:
        article_max_age = self.context.get("article_max_age")
        return get_recent_articles_of_project(
            obj, article_max_age, ArticleSerializer, WarningMessagePublicSerializer
        )


class ArticleSerializer(serializers.ModelSerializer):
    """Article serializer"""

    class Meta:
        model = Article
        fields = "__all__"


class ArticleMinimalSerializer(serializers.ModelSerializer):
    """Article serializer with minimal data"""

    meta_id = serializers.DictField(source="get_id_dict")

    class Meta:
        model = Article
        fields = ["meta_id"]


class ProjectManagerSerializer(serializers.ModelSerializer):
    """Project managers serializer"""

    projects = serializers.SerializerMethodField()

    class Meta:
        model = ProjectManager
        fields = "__all__"

    def get_projects(self, obj: ProjectManager) -> list:
        project_ids = [project.id for project in obj.projects.all()]
        return project_ids


class ProjectManagerAugmentedSerializer(serializers.ModelSerializer):
    """Project managers serializer"""

    projects = serializers.SerializerMethodField()

    class Meta:
        model = ProjectManager
        fields = "__all__"

    def get_projects(self, obj: ProjectManager) -> list:
        project_ids = [project.id for project in obj.projects.all()]

        return [
            {
                "foreign_id": x.foreign_id,
                "images": x.images,
                "subtitle": x.subtitle,
                "title": x.title,
            }
            for x in list(Project.objects.filter(pk__in=project_ids, active=True))
        ]


class WarningMessageSerializer(serializers.ModelSerializer):
    """warning messages (internal VUE) serializer"""

    class Meta:
        model = WarningMessage
        fields = "__all__"


class WarningMessageMinimalSerializer(serializers.ModelSerializer):
    """Warning message serializer with minimal data"""

    meta_id = serializers.DictField(source="get_id_dict")

    class Meta:
        model = WarningMessage
        fields = ["meta_id"]


class WarningMessagePublicSerializer(serializers.ModelSerializer):
    """Warning message serializer with extended data"""

    images = serializers.SerializerMethodField()

    class Meta:
        model = WarningMessage
        exclude = ["project", "project_manager"]

    def get_images(self, obj: WarningMessage):
        base_url = self.context.get("base_url")
        warning_images: List(WarningImage) = obj.warningimage_set.all()

        images = []
        for warning_image in warning_images:
            context = {"base_url": base_url}
            image_serializer = ImagePublicSerializer(
                instance=warning_image.images.all(), many=True, context=context
            )
            sources = image_serializer.data

            first_image = warning_image.images.first()
            image = {
                "main": warning_image.is_main,
                "sources": sources,
                "landscape": bool(first_image.width > first_image.height),
                "coordinates": first_image.coordinates,
                "description": first_image.description,
                "aspect_ratio": first_image.aspect_ratio,
            }
            images.append(image)

        return images


class WarningImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarningImage
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    """notifications serializer"""

    class Meta:
        model = Notification
        fields = "__all__"


class DeviceSerializer(serializers.ModelSerializer):
    """Device serializer"""

    class Meta:
        model = Device
        fields = "__all__"
