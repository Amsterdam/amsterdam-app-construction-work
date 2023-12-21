""" Views for news, articles and warning messages """
import base64

from django.http import HttpResponseForbidden
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from construction_work.api_messages import Messages
from construction_work.generic_functions.image_conversion import ImageConversion
from construction_work.generic_functions.is_authorized import (
    IsAuthorized,
    JWTAuthorized,
    ManagerAuthorized,
)
from construction_work.generic_functions.sort import Sort
from construction_work.generic_functions.static_data import StaticData
from construction_work.models import (
    Notification,
    Project,
    ProjectManager,
    WarningMessage,
)
from construction_work.models.image import Image
from construction_work.push_notifications.send_notification import NotificationService
from construction_work.serializers import (
    WarningImageSerializer,
    WarningMessageCreateSerializer,
    WarningMessagePublicSerializer,
)
from construction_work.swagger.swagger_views_messages import (
    as_notification_post,
    as_warning_message_delete,
    as_warning_message_get,
    as_warning_message_image_post,
    as_warning_message_patch,
    as_warning_message_post,
    as_warning_messages_get,
)

messages = Messages()


@swagger_auto_schema(**as_warning_messages_get)
@api_view(["GET"])
@IsAuthorized
def warning_messages_get(request):
    """Warning messages"""
    project_id = request.GET.get("project_id", None)
    sort_by = request.GET.get("sort-by", "modification_date")
    sort_order = request.GET.get("sort-order", None)

    if project_id is None:
        warning_messages = WarningMessage.objects.filter(project__active=True).all()
        serializer = WarningMessagePublicSerializer(warning_messages, many=True)
        result = Sort().list_of_dicts(
            serializer.data, key=sort_by, sort_order=sort_order
        )
        return Response(result, status=status.HTTP_200_OK)

    project = Project.objects.filter(pk=project_id, active=True).first()
    if project is None:
        return Response(messages.no_record_found, status=status.HTTP_404_NOT_FOUND)

    warning_messages = WarningMessage.objects.filter(project=project).all()
    serializer = WarningMessagePublicSerializer(warning_messages, many=True)
    result = Sort().list_of_dicts(serializer.data, key=sort_by, sort_order=sort_order)
    return Response(result, status=status.HTTP_200_OK)


@swagger_auto_schema(**as_warning_message_get)
@swagger_auto_schema(**as_warning_message_post)
@swagger_auto_schema(**as_warning_message_patch)
@swagger_auto_schema(**as_warning_message_delete)
@api_view(["GET", "POST", "PATCH", "DELETE"])
def warning_message_crud(request):
    """Warning message CRUD"""
    if request.method == "GET":
        return warning_message_get(request)
    if request.method == "POST":
        return warning_message_post(request)
    if request.method == "PATCH":
        return warning_message_patch(request)
    if request.method == "DELETE":
        return warning_message_delete(request)
    return Response(data=None, status=status.HTTP_400_BAD_REQUEST)


@IsAuthorized
def warning_message_get(request):
    """Warning message get"""
    message_id = request.GET.get("id", None)
    if message_id is None or not message_id.isdigit():
        return Response(messages.invalid_query, status.HTTP_400_BAD_REQUEST)

    message = WarningMessage.objects.filter(pk=message_id, project__active=True).first()
    if message is None:
        return Response(messages.no_record_found, status.HTTP_404_NOT_FOUND)

    # Get hostname for this server
    base_url = StaticData.base_url(request)

    serializer = WarningMessagePublicSerializer(
        message, many=False, context={"base_url": base_url}
    )

    return Response(serializer.data, status.HTTP_200_OK)


@ManagerAuthorized
def warning_message_post(request):
    """Post a warning message. Only warnings by a valid Project manager for a valid project are allowed."""
    title = request.data.get("title", None)
    body = request.data.get("body", None)
    project_id = request.data.get("project_id", None)
    project_manager_key = request.data.get("project_manager_key", None)

    if None in [title, project_id, project_manager_key]:
        return Response(messages.invalid_query, status.HTTP_400_BAD_REQUEST)

    if not isinstance(project_id, int):
        return Response(messages.invalid_query, status.HTTP_400_BAD_REQUEST)

    if not isinstance(body, str):
        return Response(messages.invalid_query, status.HTTP_400_BAD_REQUEST)

    project = Project.objects.filter(pk=project_id).first()
    if project is None:
        return Response(messages.no_record_found, status.HTTP_404_NOT_FOUND)

    # Check if the project manager exists
    project_manager = ProjectManager.objects.filter(
        manager_key=project_manager_key
    ).first()
    if project_manager is None:
        return Response(messages.no_record_found, status.HTTP_404_NOT_FOUND)

    # Check if project manager is entitled for sending a message for this project
    project_manager_project_ids = list(
        project_manager.projects.values_list("id", flat=True)
    )
    if project_id not in project_manager_project_ids:
        return HttpResponseForbidden()

    serializer = WarningMessageCreateSerializer(
        data={
            "title": title,
            "body": body,
            "project": project.pk,
            "project_manager": project_manager.pk,
        }
    )
    if not serializer.is_valid():
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )  # pragma: no cover

    serializer.save()
    return Response(serializer.data, status.HTTP_200_OK)


@JWTAuthorized
def warning_message_patch(request):
    """Patch a warning message (most likely by web-redactie)"""
    title = request.data.get("title", None)
    body = request.data.get("body", None)
    message_id = request.data.get("id", None)

    if None in [title, message_id] or not isinstance(message_id, int):
        return Response(messages.invalid_query, status.HTTP_400_BAD_REQUEST)

    if not isinstance(body, str) or len(body) == 0:
        return Response(messages.invalid_query, status.HTTP_400_BAD_REQUEST)

    message = WarningMessage.objects.filter(pk=message_id).first()
    if message is None:
        return Response(messages.no_record_found, status.HTTP_404_NOT_FOUND)

    serializer = WarningMessageCreateSerializer(
        instance=message, partial=True, data={"title": title, "body": body}
    )
    if not serializer.is_valid():
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )  # pragma: no cover

    serializer.save()
    return Response(serializer.data, status.HTTP_200_OK)


@JWTAuthorized
def warning_message_delete(request):
    """Delete warning message"""
    message_id = request.GET.get("id", None)
    if message_id is None:
        return Response(messages.invalid_query, status.HTTP_400_BAD_REQUEST)

    WarningMessage.objects.filter(pk=message_id).delete()

    return Response("Message deleted", status.HTTP_200_OK)


@swagger_auto_schema(**as_notification_post)
@api_view(["POST"])
@ManagerAuthorized
def notification_post(request):
    """Post Notification message"""
    title = request.data.get("title", None)
    body = request.data.get("body", None)
    warning_id = request.data.get("warning_id", None)

    if None in [title, body, warning_id]:
        return Response(
            data=messages.invalid_query,
            status=status.HTTP_400_BAD_REQUEST,
        )

    warning_message = WarningMessage.objects.filter(pk=warning_id).first()
    if warning_message is None:
        return Response(
            data=messages.no_record_found,
            status=status.HTTP_404_NOT_FOUND,
        )

    # Store notification in database
    notification_data = {"title": title, "body": body, "warning": warning_message}
    notification_object = Notification.objects.create(**notification_data)

    # Trigger the push notification services
    notification_service = NotificationService(notification_object)
    result = notification_service.setup()
    if result is False:
        # Remove notification, since it was not send
        notification_object.delete()
        return Response(
            data=notification_service.setup_result,
            status=status.HTTP_200_OK,
        )

    notification_service.send_multicast_and_handle_errors()

    return Response(
        data="Push notifications sent",
        status=status.HTTP_200_OK,
    )


@swagger_auto_schema(**as_warning_message_image_post)
@api_view(["POST"])
@ManagerAuthorized
def warning_messages_image_upload(request):
    """Upload image for warning message"""
    image_data = request.data.get("image", None)
    warning_id = request.data.get("warning_id", None)

    if None in [image_data, warning_id] or not isinstance(warning_id, int):
        return Response(messages.invalid_query, status=status.HTTP_400_BAD_REQUEST)

    warning_message = WarningMessage.objects.filter(pk=warning_id).first()
    if warning_message is None:
        return Response(messages.no_record_found, status=status.HTTP_404_NOT_FOUND)

    if "main" not in image_data:
        return Response(messages.invalid_query, status=status.HTTP_400_BAD_REQUEST)

    # Make sure we've got a boolean not a string
    image_data["main"] = bool(image_data["main"] in ["True", "true", True])

    if image_data.get("data") is None:
        return Response(messages.invalid_query, status=status.HTTP_400_BAD_REQUEST)

    # Get description
    description = image_data.get("description", f"Warning Message {warning_id}")

    # Get image data and run ImageConversion
    data = base64.b64decode(image_data.get("data"))
    image_conversion = ImageConversion(data, description)
    result = image_conversion.run()
    if result is False:
        return Response(
            messages.unsupported_image_format, status=status.HTTP_400_BAD_REQUEST
        )

    # Store images into DB and build warning-messages images list
    sources = []
    for key in image_conversion.images:  # pylint: disable=consider-using-dict-items
        # Build image object and save to database
        image = image_conversion.images[key]
        image_object = Image(
            data=image["data"],
            description=description,
            width=image["width"],
            height=image["height"],
            aspect_ratio=image_conversion.aspect_ratio,
            coordinates=image_conversion.gps_info,
            mime_type=image["mime_type"],
        )
        image_object.save()
        sources.append(image_object)

    image_ids = [image.pk for image in sources]
    warning_image_serializer = WarningImageSerializer(
        data={
            "warning": warning_message.pk,
            "is_main": image_data["main"],
            "images": image_ids,
        }
    )

    if not warning_image_serializer.is_valid():
        return Response(
            warning_image_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )  # pragma: no cover
    warning_image_serializer.save()

    return Response(warning_image_serializer.data, status=status.HTTP_200_OK)
