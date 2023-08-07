""" Generic views (images, assets) """
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from construction_work.api_messages import Messages
from construction_work.generic_functions.static_data import StaticData
from construction_work.models import Assets, Image
from construction_work.swagger.swagger_views_generic import as_asset, as_districts, as_image

message = Messages()


@swagger_auto_schema(**as_image)
@api_view(["GET"])
def image(request):
    """Request image from API by identifier"""
    identifier = request.GET.get("id", None)
    if identifier is None:
        return Response({"status": False, "result": message.invalid_query}, status=422)

    image_object = Image.objects.filter(pk=identifier).first()
    if image_object is not None:
        return HttpResponse(image_object.data, content_type=image_object.mime_type, status=200)
    return Response("Error: file not found", status=404)


@swagger_auto_schema(**as_asset)
@api_view(["GET"])
def asset(request):
    """Request asset from API by identifier (e.g. pdf document)"""
    identifier = request.GET.get("id", None)
    if identifier is None:
        return Response({"status": False, "result": message.invalid_query}, status=422)

    asset_object = Assets.objects.filter(pk=identifier).first()
    if asset_object is not None:
        return HttpResponse(asset_object.data, content_type=asset_object.mime_type, status=200)
    return Response("Error: file not found", status=404)


@swagger_auto_schema(**as_districts)
@api_view(["GET"])
def districts(request):
    """Get district data"""
    districts_data = StaticData.districts()
    return Response({"status": True, "result": districts_data}, status=200)
