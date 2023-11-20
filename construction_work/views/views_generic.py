""" Generic views (images, assets) """
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from construction_work.api_messages import Messages
from construction_work.models import Image
from construction_work.swagger.swagger_views_generic import as_image

message = Messages()


@swagger_auto_schema(**as_image)
@api_view(["GET"])
def image(request):
    """Request image from API by identifier"""
    image_id = request.GET.get("id", None)
    if image_id is None:
        return Response(message.invalid_query, status=status.HTTP_400_BAD_REQUEST)

    image_obj = Image.objects.filter(pk=image_id).first()
    if image_obj is None:
        return Response(message.no_record_found, status=status.HTTP_404_NOT_FOUND)

    return HttpResponse(
        image_obj.data, content_type=image_obj.mime_type, status=status.HTTP_200_OK
    )
