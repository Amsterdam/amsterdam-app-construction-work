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
from construction_work.models import FirebaseToken
from construction_work.models.device import Device
from construction_work.serializers import DeviceSerializer, FirebaseTokenSerializer
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
            {"status": False, "result": message.invalid_headers},
            status=status.HTTP_400_BAD_REQUEST,
        )

    device = Device.objects.filter(device_id=device_id).first()

    if request.method == "POST":
        firebase_token = request.data.get("firebase_token", None)
        if firebase_token is None:
            return Response(
                {"status": False, "result": message.invalid_query},
                status=status.HTTP_400_BAD_REQUEST,
            )

        os = request.data.get("os", None)
        if os is None:
            return Response(
                {"status": False, "result": message.invalid_query},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if device is None:
            device_serializer = DeviceSerializer(data={"device_id": device_id})
            if not device_serializer.is_valid():
                return Response(device_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            device_serializer.save()
            device = Device.objects.get(device_id=device_serializer.data.get("device_id"))

        # TODO: discuss with Robert, what to do when device already has token?
        token = FirebaseToken.objects.filter(device=device).first()
        if token:
            return Response(model_to_dict(token), status=status.HTTP_409_CONFLICT)

        token_serializer = FirebaseTokenSerializer(data={"firebase_token": firebase_token, "device": device.pk, "os": os})
        if not token_serializer.is_valid():
            return Response(token_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        token_serializer.save()
        token = FirebaseToken.objects.get(id=token_serializer.data.get("id"))
        return Response(token_serializer.data, status=status.HTTP_200_OK)

    # request.method == 'DELETE':
    if device is None:
        return Response(
            {"status": False, "result": message.no_record_found},
            status=status.HTTP_404_NOT_FOUND,
        )

    token = FirebaseToken.objects.filter(device=device).first()
    if token:
        token.delete()

    return Response({"status": False, "result": "Registration removed"}, status=200)
