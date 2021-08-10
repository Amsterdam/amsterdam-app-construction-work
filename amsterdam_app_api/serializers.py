from rest_framework import serializers
from amsterdam_app_api.models import ProjectenBruggen, ProjectenKademuren


class ProjectenBruggenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectenBruggen
        fields = '__all__'


class ProjectenKademurenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectenKademuren
        fields = '__all__'
