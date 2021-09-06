from django.http import HttpResponse
from amsterdam_app_api.swagger_views_generic import as_asset, as_image
from amsterdam_app_api.views_messages import Messages
from amsterdam_app_api.models import Image, Assets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


message = Messages()


@swagger_auto_schema(**as_image)
@api_view(['GET'])
def image(request):
    """
    Request image from API by identifier
    """
    if request.method == 'GET':
        identifier = request.GET.get('id', None)
        if identifier is None:
            return Response({'status': False, 'result': message.invalid_query}, status=422)
        else:
            image_object = Image.objects.filter(pk=identifier).first()
            if image_object is not None:
                return HttpResponse(image_object.data, content_type=image_object.mime_type, status=200)
            else:
                return Response('Error: file not found', status=404)


@swagger_auto_schema(**as_asset)
@api_view(['GET'])
def asset(request):
    """
    Request asset from API by identifier (e.g. pdf document)
    """
    if request.method == 'GET':
        identifier = request.GET.get('id', None)
        if identifier is None:
            return Response({'status': False, 'result': message.invalid_query}, status=422)
        else:
            asset_object = Assets.objects.filter(pk=identifier).first()
            if asset_object is not None:
                return HttpResponse(asset_object.data, content_type=asset_object.mime_type, status=200)
            else:
                return Response('Error: file not found', status=404)
