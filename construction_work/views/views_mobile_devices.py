""" Views for mobile device routes """
from django.db import IntegrityError
from django.forms import model_to_dict
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from construction_work.api_messages import Messages
from construction_work.generic_functions.request_must_come_from_app import (
    RequestMustComeFromApp,
)
from construction_work.models.device import Device
from construction_work.serializers import DeviceSerializer
from construction_work.swagger.swagger_views_devices import (
    as_device_register_delete,
    as_device_register_post,
)

message = Messages()


@swagger_auto_schema(**as_device_register_post)
@swagger_auto_schema(**as_device_register_delete)
@api_view(["POST", "DELETE"])
@RequestMustComeFromApp
def device_register(request):
    """Device register"""
    device_id = request.META.get("HTTP_DEVICEID", None)
    if device_id is None:
        return Response(
            data=message.invalid_headers,
            status=status.HTTP_400_BAD_REQUEST,
        )

    device = Device.objects.filter(device_id=device_id).first()

    if request.method == "POST":
        firebase_token = request.data.get("firebase_token", None)
        if firebase_token is None:
            return Response(
                data=message.invalid_query,
                status=status.HTTP_400_BAD_REQUEST,
            )

        os = request.data.get("os", None)
        if os is None:
            return Response(
                data=message.invalid_query,
                status=status.HTTP_400_BAD_REQUEST,
            )

        device_serializer = DeviceSerializer(
            instance=device,
            data={"device_id": device_id, "firebase_token": firebase_token, "os": os},
        )
        if not device_serializer.is_valid():
            return Response(
                device_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        device_serializer.save()
        return Response(device_serializer.data, status=status.HTTP_200_OK)

    # request.method == 'DELETE':
    if device is None:
        return Response(
            data=message.no_record_found,
            status=status.HTTP_404_NOT_FOUND,
        )

    device.firebase_token = None
    device.save()

    return Response("Registration removed", status=200)
