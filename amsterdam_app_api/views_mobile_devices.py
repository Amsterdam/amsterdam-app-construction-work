from amsterdam_app_api.views_messages import Messages
from amsterdam_app_api.models import MobileDevices
from amsterdam_app_api.swagger_views_mobile_devices import as_push_notifications_registration
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

message = Messages()


@swagger_auto_schema(**as_push_notifications_registration)
@api_view(['POST', 'PATCH', 'DELETE'])
def registration(request):
    """
    Register a mobile device with a set of project identifiers
    """
    if request.method in ['POST', 'PATCH']:
        identifier = request.data.get('identifier', None)
        os_type = request.data.get('os-type', None)
        projects = request.data.get('projects', None)

        if identifier is None or os_type is None:
            return Response({'status': False, 'result': message.invalid_query}, status=422)
        elif projects == [] or projects is None:
            # remove mobile device because it has no push-notification subscriptions
            MobileDevices.objects.filter(pk=identifier).delete()
            return Response({'status': True, 'result': 'Device registration updated'}, status=200)
        else:
            mobile_device_object = MobileDevices.objects.filter(pk=identifier).first()

            # New record
            if mobile_device_object is None:
                mobile_device_object = MobileDevices(identifier=identifier, os_type=os_type, projects=projects)
                mobile_device_object.save()

            # Update existing record
            else:
                mobile_device_object = MobileDevices.objects.filter(pk=identifier).first()
                mobile_device_object(identifier=identifier, os_type=os_type, projects=projects)
                mobile_device_object.save()

            return Response({'status': True, 'result': 'Device registration updated'}, status=200)

    elif request.method == 'DELETE':
        identifier = request.data.get('identifier', None)
        if identifier is None:
            return Response({'status': False, 'result': message.invalid_query}, status=422)
        else:
            # remove mobile device from database
            MobileDevices.objects.filter(pk=identifier).delete()
            return Response({'status': True, 'result': 'Device registration updated'}, status=200)
