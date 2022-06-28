from amsterdam_app_api.api_messages import Messages
from amsterdam_app_api.models import FirebaseTokens
from amsterdam_app_api.swagger.swagger_views_devices import as_device_register_post, as_device_register_delete
from amsterdam_app_api.GenericFunctions.RequestMustComeFromApp import RequestMustComeFromApp
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.db import IntegrityError

message = Messages()


@swagger_auto_schema(**as_device_register_post)
@swagger_auto_schema(**as_device_register_delete)
@api_view(['POST', 'DELETE'])
@RequestMustComeFromApp
def device_register(request):
    deviceid = request.META.get('HTTP_DEVICEID', None)
    if deviceid is None:
        return Response({'status': False, 'result': message.invalid_headers}, status=422)

    if request.method == 'POST':
        firebase_token = request.data.get('firebase_token', None)
        if firebase_token is None:
            return Response({'status': False, 'result': message.invalid_query}, status=422)

        os = request.data.get('os', None)
        if os is None:
            return Response({'status': False, 'result': message.invalid_query}, status=422)

        try:
            device_registration = FirebaseTokens(deviceid=deviceid, os=os, firebasetoken=firebase_token)
            device_registration.save()
        except IntegrityError:  # Double request with same data, discard...
            pass
        return Response({'status': False, 'result': 'Registration added'}, status=200)

    if request.method == 'DELETE':
        FirebaseTokens(deviceid=deviceid).delete()
        return Response({'status': False, 'result': 'Registration removed'}, status=200)
