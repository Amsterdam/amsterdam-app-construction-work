""" Views for news, articles and warning messages """
import base64
import uuid

from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from construction_work.api_messages import Messages
from construction_work.generic_functions.image_conversion import ImageConversion
from construction_work.generic_functions.is_authorized import IsAuthorized
from construction_work.generic_functions.sort import Sort
from construction_work.generic_functions.static_data import StaticData
from construction_work.models import (
    Article,
    Image,
    Notification,
    Project,
    ProjectManager,
    WarningMessage,
)
from construction_work.push_notifications.send_notification import SendNotification
from construction_work.serializers import (
    NotificationSerializer,
    WarningMessageSerializer,
    WarningMessagesExternalSerializer,
)
from construction_work.swagger.swagger_views_messages import (
    as_notification_get,
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
def warning_messages_get(request):
    """Warning messages"""
    project_id = request.GET.get("id", None)
    sort_by = request.GET.get("sort-by", "modification_date")
    sort_order = request.GET.get("sort-order", None)

    warning_messages = []
    if project_id is None:
        projects = Project.objects.all()
        for project in projects:
            if project.active is True:
                warning_messages += WarningMessage.objects.filter(
                    project_identifier=project.project_id
                ).all()

        serializer = WarningMessagesExternalSerializer(
            warning_messages, many=True
        )
        result = Sort().list_of_dicts(
            serializer.data, key=sort_by, sort_order=sort_order
        )
        return Response({"status": True, "result": result}, 200)

    project = Project.objects.filter(pk=project_id).first()
    if project is None:
        return Response({"status": False, "result": messages.no_record_found}, 404)

    result = []
    if project.active is True:
        warning_messages = WarningMessage.objects.filter(
            project_identifier=project_id
        ).all()
        serializer = WarningMessagesExternalSerializer(
            warning_messages, many=True
        )
        result = Sort().list_of_dicts(
            serializer.data, key=sort_by, sort_order=sort_order
        )
    return Response({"status": True, "result": result}, 200)


@swagger_auto_schema(**as_warning_message_get)
@swagger_auto_schema(**as_warning_message_post)
@swagger_auto_schema(**as_warning_message_patch)
@swagger_auto_schema(**as_warning_message_delete)
@api_view(["GET", "POST", "PATCH", "DELETE"])
def warning_message_crud(request):
    """Warning message CRUD"""
    if request.method == "GET":
        data = warning_message_get(request)
        return Response(data["result"], status=data["status_code"])

    if request.method == "POST":
        data = None
        try:
            data = warning_message_post(request)
            return Response(data["result"], status=data["status_code"])
        except Exception:
            return data

    if request.method == "PATCH":
        data = None
        try:
            data = warning_message_patch(request)
            return Response(data["result"], status=data["status_code"])
        except Exception:
            return data

    # request.method == 'DELETE'
    data = None
    try:
        data = warning_message_delete(request)
        return Response(data["result"], status=data["status_code"])
    except Exception:
        return data


def warning_message_get(request):
    """Warning message get"""
    message_id = request.GET.get("id", None)
    if message_id is None:
        return {
            "result": {"status": False, "result": messages.invalid_query},
            "status_code": status.HTTP_400_BAD_REQUEST,
        }

    message = WarningMessage.objects.filter(pk=message_id).first()
    if message is None:
        return {
            "result": {"status": False, "result": messages.no_record_found},
            "status_code": status.HTTP_404_NOT_FOUND,
        }

    # Get hostname for this server
    base_url = StaticData.base_url(request)

    if message.project.active is False:
        return {
            "result": {"status": False, "result": messages.no_record_found},
            "status_code": status.HTTP_404_NOT_FOUND,
        }

    serializer = WarningMessagesExternalSerializer(message, many=False)
    message_data = serializer.data

    # TODO: move this to serializer
    for i in range(0, len(message_data["images"])):
        for j in range(0, len(message_data["images"][i]["sources"])):
            if "url" not in message_data["images"][i]["sources"][j]:
                image_id = message_data["images"][i]["sources"][j]["image_id"]
                message_data["images"][i]["sources"][j][
                    "url"
                ] = f"{base_url}image?id={image_id}"
    
    return {
        "result": serializer.data,
        "status_code": status.HTTP_200_OK,
    }


@IsAuthorized
def warning_message_patch(request):
    """Patch a warning message (most likely by web-redactie)"""
    title = request.data.get("title", None)
    body = request.data.get("body", None)
    message_id = request.data.get("identifier", None)

    if None in [title, message_id]:
        return {
            "result": {"status": False, "result": messages.invalid_query},
            "status_code": status.HTTP_400_BAD_REQUEST,
        }

    if not isinstance(body, str):
        return {
            "result": {"status": False, "result": messages.invalid_query},
            "status_code": status.HTTP_400_BAD_REQUEST,
        }

    message = WarningMessage.objects.filter(pk=message_id).first()
    if message is None:
        return {
            "result": {"status": False, "result": messages.no_record_found},
            "status_code": status.HTTP_404_NOT_FOUND,
        }

    serializer = WarningMessageSerializer(instance=message, partial=True, data={
        "title": title,
        "body": body,
    })
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@IsAuthorized
def warning_message_post(request):
    """Post a warning message. Only warnings by a valid Project manager for a valid project are allowed."""
    title = request.data.get("title", None)
    body = request.data.get("body", None)
    project_id = request.data.get("project_identifier", None)
    project_manager_id = request.data.get("project_manager_id", None)

    if None in [title, project_id, project_manager_id]:
        return {
            "result": {"status": False, "result": messages.invalid_query},
            "status_code": status.HTTP_400_BAD_REQUEST,
        }

    if not isinstance(body, str):
        return {
            "result": {"status": False, "result": messages.invalid_query},
            "status_code": status.HTTP_400_BAD_REQUEST,
        }

    project = Project.objects.filter(pk=project_id).first()
    if project is None:
        return {
            "result": {"status": False, "result": messages.no_record_found},
            "status_code": status.HTTP_404_NOT_FOUND,
        }

    # Check if the project manager exists and is entitled for sending a message for this project
    project_manager = ProjectManager.objects.filter(pk=project_manager_id).first()
    if project_manager is None:
        return {
            "result": {"status": False, "result": messages.no_record_found},
            "status_code": status.HTTP_404_NOT_FOUND,
        }

    if project_id not in project_manager.projects:
        return {
            "result": {"status": False, "result": messages.no_record_found},
            "status_code": status.HTTP_403_FORBIDDEN,
        }

    serializer = WarningMessageSerializer(
        data={
            "title": title,
            "body": body,
            "project": project.pk,
            "project_manager": project_manager.pk,
        }
    )
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@IsAuthorized
def warning_message_delete(request):
    """Delete warning message"""
    identifier = request.GET.get("id", None)
    if identifier is None:
        return {
            "result": {"status": False, "result": messages.invalid_query},
            "status_code": 422,
        }

    WarningMessage.objects.filter(identifier=identifier).delete()
    return {
        "result": {"status": False, "result": "Message deleted"},
        "status_code": 200,
    }


@swagger_auto_schema(**as_notification_post)
@IsAuthorized
@api_view(["POST"])
def notification_post(request):
    """Post Notification message"""
    title = request.data.get("title", None)
    body = request.data.get("body", None)
    news_identifier = request.data.get("news_identifier", None)
    warning_identifier = request.data.get("warning_identifier", None)

    if None in [title, body]:
        return Response({"status": False, "result": messages.invalid_query}, status=422)

    if news_identifier is None and warning_identifier is None:
        return Response({"status": False, "result": messages.invalid_query}, status=422)

    if (
        news_identifier is not None
        and Article.objects.filter(identifier=news_identifier).first() is None
    ):
        return Response(
            {"status": False, "result": messages.no_record_found}, status=404
        )

    if (
        warning_identifier is not None
        and WarningMessage.objects.filter(pk=warning_identifier).first() is None
    ):
        return Response(
            {"status": False, "result": messages.no_record_found}, status=404
        )

    notification = Notification(
        title=title,
        body=body,
        news_identifier=news_identifier,
        warning_identifier=warning_identifier,
    )
    notification.save()

    # Trigger the push notification services
    notification_services = SendNotification(notification.identifier)
    if not notification_services.valid_notification:
        return Response(notification_services.setup_result, 422)
    notification_services.send_multicast_and_handle_errors()

    # Send response to end-user
    return Response(
        {"status": True, "result": "push-notification accepted"}, status=200
    )


@swagger_auto_schema(**as_notification_get)
@api_view(["GET"])
def notification_get(request):
    """Get notification"""
    query_params = request.GET.get("project-ids", None)
    sort_by = request.GET.get("sort-by", "publication_date")
    sort_order = request.GET.get("sort-order", "desc")

    if query_params is None:
        return Response({"status": False, "result": messages.invalid_query}, status=422)
    project_identifiers = query_params.split(",")
    notifications = []
    for project_identifier in project_identifiers:
        project = Project.objects.filter(pk=project_identifier).first()
        if project is not None and project.active is True:
            notifications += list(
                Notification.objects.filter(project_identifier=project_identifier).all()
            )

    serializer = NotificationSerializer(notifications, many=True)
    if len(serializer.data) != 0:
        result = Sort().list_of_dicts(
            serializer.data, key=sort_by, sort_order=sort_order
        )
        return Response({"status": True, "result": result}, status=200)
    return Response({"status": False, "result": messages.no_record_found}, status=404)


@swagger_auto_schema(**as_warning_message_image_post)
@IsAuthorized
@api_view(["POST"])
def warning_messages_image_upload(request):
    """Upload image for warning message"""
    image_data = request.data.get("image", None)
    warning_id = request.data.get("project_warning_id", None)

    if None in [image_data, warning_id]:
        return Response({"status": False, "result": messages.invalid_query}, status=status.HTTP_400_BAD_REQUEST)

    warning_message = WarningMessage.objects.filter(pk=warning_id).first()
    if warning_message is None:
        return Response(
            {"status": False, "result": messages.no_record_found}, status=status.HTTP_404_NOT_FOUND
        )

    if "main" not in image_data:
        return Response({"status": False, "result": messages.invalid_query}, status=status.HTTP_400_BAD_REQUEST)

    # Make sure we've got a boolean not a string
    image_data["main"] = bool(image_data["main"] in ["True", "true", True])

    if image_data.get("data") is None:
        return Response({"status": False, "result": messages.invalid_query}, status=status.HTTP_400_BAD_REQUEST)

    # Get description
    description = image_data.get("description", f"Warning Message {warning_id}")

    # Get image data and run ImageConversion
    data = base64.b64decode(image_data.get("data"))
    image_conversion = ImageConversion(data, description)
    result = image_conversion.run()
    if result is False:
        return Response(
            {"status": False, "result": messages.unsupported_image_format}, status=422
        )

    # Store images into DB and build warning-messages images list
    sources = []
    for key in image_conversion.images:  # pylint: disable=consider-using-dict-items
        # Build image object and save to database
        image = image_conversion.images[key]
        identifier = uuid.uuid4().hex
        image_object = Image(
            identifier=identifier,
            size="{width}x{height}".format(
                width=image["width"], height=image["height"]
            ),
            url="db://construction_work.warning_message/{identifier}".format(
                identifier=identifier
            ),
            filename=image["filename"],
            description=description,
            mime_type=image["mime_type"],
            data=image["data"],
        )
        image_object.save()
        sources.append(
            {
                "image_id": identifier,
                "mime_type": image["mime_type"],
                "width": image["width"],
                "height": image["height"],
            }
        )

    # Update warning-message with new images
    warning_message_image = {
        "main": image_data.get("main"),
        "aspect_ratio": image_conversion.aspect_ratio,
        "description": description,
        "coordinates": image_conversion.gps_info,
        "landscape": image_conversion.landscape,
        "sources": sources,  # list; created earlier
    }

    warning_message = WarningMessage.objects.filter(pk=warning_id).first()
    warning_message.images.append(warning_message_image)
    warning_message.save()

    return Response({"status": True, "result": "Images stored in database"}, status=200)
