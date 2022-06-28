from amsterdam_app_api.api_messages import Messages
from amsterdam_app_api.models import MobileDevices, Projects
from amsterdam_app_api.models import FirebaseTokens
from amsterdam_app_api.swagger.swagger_views_devices import as_device_register_post, as_device_register_delete
from amsterdam_app_api.swagger.swagger_views_mobile_devices import as_push_notifications_registration_device_post
from amsterdam_app_api.swagger.swagger_views_mobile_devices import as_push_notifications_registration_device_patch
from amsterdam_app_api.swagger.swagger_views_mobile_devices import as_push_notifications_registration_device_delete
from amsterdam_app_api.GenericFunctions.RequestMustComeFromApp import RequestMustComeFromApp
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.db import IntegrityError

message = Messages()

""" Views for CRUD a mobile-device and assign subscriptions for push-notifications
"""


@swagger_auto_schema(**as_push_notifications_registration_device_post)
@swagger_auto_schema(**as_push_notifications_registration_device_patch)
@swagger_auto_schema(**as_push_notifications_registration_device_delete)
@RequestMustComeFromApp
@api_view(['POST', 'PATCH', 'DELETE'])
def crud(request):
    if request.method in ['POST', 'PATCH']:
        data = post_patch(request)
        return Response(data['result'], status=data['status'])
    elif request.method in ['DELETE']:
        data = delete(request)
        return Response(data['result'], status=data['status'])


def post_patch(request):
    """
    Register a mobile device with a set of project identifiers
    """
    def filter(projects):
        all_projects = list(Projects.objects.all())
        inactive = [x.identifier for x in all_projects if x.active is False]
        deleted = [x for x in projects if Projects.objects.filter(pk=x).first() is None] if projects is not None else []
        active = [x for x in projects if x not in inactive + deleted] if projects is not None else []
        return active, inactive, deleted,

    device_token = request.data.get('device_token', None)
    device_refresh_token = request.data.get('device_refresh_token', None)
    os_type = request.data.get('os_type', None)
    projects = request.data.get('projects', None)

    if device_token is not None and device_refresh_token is not None:
        md = MobileDevices.objects.filter(pk=device_token).first()
        if md is not None:
            active, inactive, deleted = filter(md.projects)
            md.device_token = device_refresh_token
            md.projects = active
            md.save()
            return {'result':
                        {
                            'status': True,
                            'result': {
                                'active': active,  # array of identifiers
                                'inactive': inactive,  # array of identifiers
                                'deleted': deleted  # array of identifiers
                            }
                        }, 'status': 200}
        return {'result': {'status': False, 'result': message.no_record_found}, 'status': 404}
    elif device_token is None or os_type is None:
        return {'result': {'status': False, 'result': message.invalid_query}, 'status': 422}
    elif projects == [] or projects is None:
        # remove mobile device because it has no push-notification subscriptions
        MobileDevices.objects.filter(pk=device_token).delete()
        return {'result': {'status': True, 'result': 'Device removed from database'}, 'status': 204}
    else:
        mobile_device_object = MobileDevices.objects.filter(pk=device_token).first()
        active, inactive, deleted = filter(projects)
        # New record
        if mobile_device_object is None:
            mobile_device_object = MobileDevices(device_token=device_token, os_type=os_type, projects=active)
            mobile_device_object.save()

        # Update existing record
        else:
            MobileDevices.objects.filter(pk=device_token).update(device_token=device_token,
                                                                 os_type=os_type,
                                                                 projects=active)

        return {
            'result': {
                'status': True,
                'result': {
                    'active': active,  # array of identifiers
                    'inactive': inactive,  # array of identifiers
                    'deleted': deleted  # array of identifiers
                }
            },
            'status': 200
        }


def delete(request):
    identifier = request.GET.get('id', None)
    if identifier is None:
        return {'result': {'status': False, 'result': message.invalid_query}, 'status': 422}
    else:
        # remove mobile device from database
        MobileDevices.objects.filter(pk=identifier).delete()
        return {'result': {'status': True, 'result': 'Device removed from database'}, 'status': 204}


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
