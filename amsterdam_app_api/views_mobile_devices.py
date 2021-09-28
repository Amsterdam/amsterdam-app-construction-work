from amsterdam_app_api.api_messages import Messages
from amsterdam_app_api.models import MobileDevices
from amsterdam_app_api.swagger_views_mobile_devices import as_push_notifications_registration_device_post_patch
from amsterdam_app_api.swagger_views_mobile_devices import as_push_notifications_registration_device_delete
from amsterdam_app_api.GenericFunctions.RequestMustComeFromApp import RequestMustComeFromApp
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

message = Messages()

""" Views for CRUD a mobile-device and assign subscriptions for push-notifications
"""


@swagger_auto_schema(**as_push_notifications_registration_device_post_patch)
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
    identifier = request.data.get('identifier', None)
    os_type = request.data.get('os_type', None)
    projects = request.data.get('projects', None)

    if identifier is None or os_type is None:
        return {'result': {'status': False, 'result': message.invalid_query}, 'status': 422}
    elif projects == [] or projects is None:
        # remove mobile device because it has no push-notification subscriptions
        MobileDevices.objects.filter(pk=identifier).delete()
        return {'result': {'status': True, 'result': 'Device registration updated'}, 'status': 200}
    else:
        mobile_device_object = MobileDevices.objects.filter(pk=identifier).first()

        # New record
        if mobile_device_object is None:
            mobile_device_object = MobileDevices(identifier=identifier, os_type=os_type, projects=projects)
            mobile_device_object.save()

        # Update existing record
        else:
            MobileDevices.objects.filter(pk=identifier).update(identifier=identifier, os_type=os_type, projects=projects)

        return {'result': {'status': True, 'result': 'Device registration updated'}, 'status': 200}


def delete(request):
    identifier = request.GET.get('id', None)
    if identifier is None:
        return {'result': {'status': False, 'result': message.invalid_query}, 'status': 422}
    else:
        # remove mobile device from database
        MobileDevices.objects.filter(pk=identifier).delete()
        return {'result': {'status': True, 'result': 'Device removed from database'}, 'status': 200}
