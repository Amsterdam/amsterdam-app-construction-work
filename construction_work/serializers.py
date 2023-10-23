""" Serializers for DB models """
from ast import List
from datetime import datetime, timedelta

from rest_framework import serializers

from construction_work.generic_functions.distance import GeoPyDistance
from construction_work.models import Article, Asset, Image, Notification, Project, ProjectManager, WarningMessage
from construction_work.models.device import Device
from construction_work.models.warning_and_notification import WarningImage


class AssetsSerializer(serializers.ModelSerializer):
    """Assets serializer (pdf's)"""

    class Meta:
        model = Asset
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    """Image serializer (iprox images)"""

    # TODO: url, size, landscape

    class Meta:
        model = Image
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    """Project create serializer"""

    class Meta:
        model = Project
        fields = "__all__"


class ProjectListSerializer(serializers.ModelSerializer):
    """Project list serializer"""

    followed = serializers.SerializerMethodField()
    recent_articles = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = "__all__"

    def get_followed(self, obj: Project) -> bool:
        """Check if project is being followed by given device"""
        device_id = self.context.get("device_id")
        project_followed = False
        if device_id is not None:
            device = obj.device_set.filter(device_id=device_id).first()
            if device is not None:
                project_followed = True
        return project_followed

    def get_recent_articles(self, obj: Project) -> dict:
        all_articles = []

        articles_max_age = self.context.get("articles_max_age")
        start_date = datetime.now().astimezone() - timedelta(days=int(articles_max_age))
        end_date = datetime.now().astimezone()
        
        articles = obj.article_set.filter(publication_date__range=[start_date, end_date]).all()
        article_serializer = ArticleSerializer(articles, many=True)
        all_articles.extend(article_serializer.data)

        warning_messages = obj.warningmessage_set.filter(publication_date__range=[start_date, end_date]).all()
        warning_message_serializer = WarningMessagePublicSerializer(warning_messages, many=True)
        all_articles.extend(warning_message_serializer.data)

        return all_articles


class ProjectDetailsSerializer(ProjectListSerializer):
    """Project details serializer"""

    meter = serializers.SerializerMethodField()
    strides = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    class Meta:
        model = Project
        exclude = ["id"]

    def __init__(self, instance=None, data=None, **kwargs):
        super().__init__(instance, data, **kwargs)

        if data is None:
            data = {}
        self.distance = None
        lat = self.context.get("lat")
        lon = self.context.get("lon")
        self.distance = self.get_distance_from_project(lat, lon, instance)

    def get_field_names(self, *args, **kwargs):
        field_names = self.context.get("fields", None)
        if field_names:
            return field_names
        return super().get_field_names(*args, **kwargs)

    def get_meter(self, _) -> int:
        """Get meters from distance obj"""
        return self.distance.meter

    def get_strides(self, _) -> int:
        """Get strides from distance obj"""
        return self.distance.strides

    def get_followers(self, obj: Project) -> int:
        """Get amount of followers of project"""
        return obj.device_set.count()

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


class WarningMessageSerializer(serializers.ModelSerializer):
    """warning messages (internal VUE) serializer"""

    class Meta:
        model = WarningMessage
        fields = "__all__"


class WarningMessagePublicSerializer(serializers.ModelSerializer):
    """warning messages (external) serializer"""

    # project_foreign_id = serializers.CharField(source="project.foreign_id")
    # project_manager_key = serializers.CharField(source="project_manager.manager_key")

    images = serializers.SerializerMethodField()

    class Meta:
        model = WarningMessage
        exclude = ["project", "project_manager"]

    def get_images(self, obj: WarningMessage):
        base_url = self.context.get("base_url")
        warning_images: List[WarningImage] = obj.warningimage_set.all()

        images = []
        for warning_image in warning_images:
            sources = []
            first_image = warning_image.images.first()
            for source_image in warning_image.images.all():
                source = {
                    "width": source_image.width,
                    "height": source_image.height,
                    "image_id": source_image.pk,
                    "mime_type": source_image.mime_type,
                    "url": f"{base_url}image?id={source_image.pk}",
                }
                sources.append(source)

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
