from amsterdam_app_api.api_messages import Messages
from amsterdam_app_api.models import MobileDevices
from amsterdam_app_api.swagger_views_mobile_devices import as_push_notifications_registration_device_post
from amsterdam_app_api.swagger_views_mobile_devices import as_push_notifications_registration_device_patch
from amsterdam_app_api.swagger_views_mobile_devices import as_push_notifications_registration_device_delete
from amsterdam_app_api.GenericFunctions.RequestMustComeFromApp import RequestMustComeFromApp
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

messages = Messages()

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
    device_token = request.data.get('device_token', None)
    device_refresh_token = request.data.get('device_refresh_token', None)
    os_type = request.data.get('os_type', None)
    projects = request.data.get('projects', None)

    if device_token is None or os_type is None:
        return {'result': {'status': False, 'result': messages.invalid_query}, 'status': 422}
    elif projects == [] or projects is None:
        # remove mobile device because it has no push-notification subscriptions
        MobileDevices.objects.filter(pk=device_token).delete()
        return {'result': {'status': True, 'result': 'Device registration updated'}, 'status': 200}
    else:
        mobile_device_object = MobileDevices.objects.filter(pk=device_token).first()

        # New record
        if mobile_device_object is None:
            mobile_device_object = MobileDevices(device_token=device_token, os_type=os_type, projects=projects)
            mobile_device_object.save()

        # Update existing record
        else:
            if device_refresh_token is not None:
                MobileDevices.objects.filter(pk=device_token).update(device_token=device_refresh_token,
                                                                     os_type=os_type,
                                                                     projects=projects)
            else:
                MobileDevices.objects.filter(pk=device_token).update(device_token=device_token,
                                                                     os_type=os_type,
                                                                     projects=projects)

        return {'result': {'status': True, 'result': 'Device registration updated'}, 'status': 200}


def delete(request):
    identifier = request.GET.get('id', None)
    if identifier is None:
        return {'result': {'status': False, 'result': messages.invalid_query}, 'status': 422}
    else:
        # remove mobile device from database
        MobileDevices.objects.filter(pk=identifier).delete()
        return {'result': {'status': True, 'result': 'Device removed from database'}, 'status': 200}
