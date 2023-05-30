""" Views for news, articles and warning messages """
import base64
import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from amsterdam_app_api.GenericFunctions.IsAuthorized import IsAuthorized
from amsterdam_app_api.GenericFunctions.Sort import Sort
from amsterdam_app_api.GenericFunctions.ImageConversion import ImageConversion
from amsterdam_app_api.PushNotifications.SendNotification import SendNotification
from amsterdam_app_api.api_messages import Messages
from amsterdam_app_api.models import WarningMessages
from amsterdam_app_api.models import Projects
from amsterdam_app_api.models import ProjectManager
from amsterdam_app_api.models import Notification
from amsterdam_app_api.models import News
from amsterdam_app_api.models import Image
from amsterdam_app_api.serializers import WarningMessagesExternalSerializer
from amsterdam_app_api.serializers import NotificationSerializer
from amsterdam_app_api.swagger.swagger_views_messages import as_warning_message_post
from amsterdam_app_api.swagger.swagger_views_messages import as_warning_message_patch
from amsterdam_app_api.swagger.swagger_views_messages import as_warning_message_get
from amsterdam_app_api.swagger.swagger_views_messages import as_warning_messages_get
from amsterdam_app_api.swagger.swagger_views_messages import as_warning_message_delete
from amsterdam_app_api.swagger.swagger_views_messages import as_notification_post
from amsterdam_app_api.swagger.swagger_views_messages import as_notification_get
from amsterdam_app_api.swagger.swagger_views_messages import as_warning_message_image_post

messages = Messages()


@swagger_auto_schema(**as_warning_messages_get)
@api_view(['GET'])
def warning_messages_get(request):
    """ Warning messages """
    project_identifier = request.GET.get('id', None)
    sort_by = request.GET.get('sort-by', 'modification_date')
    sort_order = request.GET.get('sort-order', None)

    warning_messages_objects = []
    if project_identifier is None:
        projects = Projects.objects.all()
        for project in projects:
            if project.active is True:
                warning_messages_objects += WarningMessages.objects.filter(project_identifier=project.identifier).all()

        serializer = WarningMessagesExternalSerializer(warning_messages_objects, many=True)
        result = Sort().list_of_dicts(serializer.data, key=sort_by, sort_order=sort_order)
        return Response({'status': True, 'result': result}, 200)

    project = Projects.objects.filter(pk=project_identifier).first()
    if project is None:
        return Response({'status': False, 'result': messages.no_record_found}, 404)

    result = []
    if project.active is True:
        warning_messages_objects = WarningMessages.objects.filter(project_identifier=project_identifier).all()
        serializer = WarningMessagesExternalSerializer(warning_messages_objects, many=True)
        result = Sort().list_of_dicts(serializer.data, key=sort_by, sort_order=sort_order)
    return Response({'status': True, 'result': result}, 200)


@swagger_auto_schema(**as_warning_message_get)
@swagger_auto_schema(**as_warning_message_post)
@swagger_auto_schema(**as_warning_message_patch)
@swagger_auto_schema(**as_warning_message_delete)
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def warning_message_crud(request):
    """ Warning message CRUD """
    if request.method == 'GET':
        data = warning_message_get(request)
        return Response(data['result'], status=data['status_code'])

    if request.method == 'POST':
        data = None
        try:
            data = warning_message_post(request)
            return Response(data['result'], status=data['status_code'])
        except Exception:
            return data

    if request.method == 'PATCH':
        data = None
        try:
            data = warning_message_patch(request)
            return Response(data['result'], status=data['status_code'])
        except Exception:
            return data

    # request.method == 'DELETE'
    data = None
    try:
        data = warning_message_delete(request)
        return Response(data['result'], status=data['status_code'])
    except Exception:
        return data


def warning_message_get(request):
    """ Warning message get """
    identifier = request.GET.get('id', None)
    if identifier is None:
        return {'result': {'status': False, 'result': messages.invalid_query}, 'status_code': 422}

    warning_messages_object = WarningMessages.objects.filter(pk=identifier).first()
    if warning_messages_object is None:
        return {'result': {'status': False, 'result': messages.no_record_found}, 'status_code': 404}

    project = Projects.objects.filter(pk=warning_messages_object.project_identifier_id).first()
    if project.active is True:
        serializer = WarningMessagesExternalSerializer(warning_messages_object, many=False)
        return {'result': {'status': True, 'result': serializer.data}, 'status_code': 200}
    return {'result': {'status': False, 'result': messages.no_record_found}, 'status_code': 404}


@IsAuthorized
def warning_message_patch(request):
    """ Patch a warning message (most likely by web-redactie)
    """
    title = request.data.get('title', None)
    identifier = request.data.get('identifier', None)
    body = request.data.get('body', None)

    if None in [title, identifier]:
        return {'result': {'status': False, 'result': messages.invalid_query}, 'status_code': 422}

    if not isinstance(body, str):
        return {'result': {'status': False, 'result': messages.invalid_query}, 'status_code': 422}

    if WarningMessages.objects.filter(identifier=identifier).first() is None:
        return {'result': {'status': False, 'result': messages.no_record_found}, 'status_code': 404}

    message_object = WarningMessages.objects.filter(identifier=identifier).first()
    message_object.body = body
    message_object.title = title
    message_object.save()
    return {'result': {'status': True, 'result': 'Message patched'}, 'status_code': 200}


@IsAuthorized
def warning_message_post(request):
    """ Post a warning message. Only warnings by a valid Project manager for a valid project are allowed.
    """
    title = request.data.get('title', None)
    project_identifier = request.data.get('project_identifier', None)
    project_manager_id = request.data.get('project_manager_id', None)
    body = request.data.get('body', None)

    if None in [title, project_identifier, project_manager_id]:
        return {'result': {'status': False, 'result': messages.invalid_query}, 'status_code': 422}

    if not isinstance(body, str):
        return {'result': {'status': False, 'result': messages.invalid_query}, 'status_code': 422}

    if Projects.objects.filter(pk=project_identifier).first() is None:
        return {'result': {'status': False, 'result': messages.invalid_query}, 'status_code': 422}

    # Check if the project manager exists and is entitled for sending a message for this project
    project_manager = ProjectManager.objects.filter(pk=project_manager_id).first()
    if project_manager is None:
        return {'result': {'status': False, 'result': messages.no_record_found}, 'status_code': 404}

    if project_identifier not in project_manager.projects:
        return {'result': {'status': False, 'result': messages.no_record_found}, 'status_code': 404}

    message_object = WarningMessages(title=title,
                                     body=body,
                                     project_identifier=Projects.objects.filter(pk=project_identifier).first(),
                                     project_manager_id=project_manager_id,
                                     images=[])
    message_object.save()
    return {
        'result': {
            'status': True,
            'result': {'warning_identifier': str(message_object.identifier)}
        },
        'status_code': 200
    }


@IsAuthorized
def warning_message_delete(request):
    """ Delete warning message """
    identifier = request.GET.get('id', None)
    if identifier is None:
        return {'result': {'status': False, 'result': messages.invalid_query}, 'status_code': 422}

    WarningMessages.objects.filter(identifier=identifier).delete()
    return {'result': {'status': False, 'result': 'Message deleted'}, 'status_code': 200}


@swagger_auto_schema(**as_notification_post)
@IsAuthorized
@api_view(['POST'])
def notification_post(request):
    """ Post Notification message """
    title = request.data.get('title', None)
    body = request.data.get('body', None)
    news_identifier = request.data.get('news_identifier', None)
    warning_identifier = request.data.get('warning_identifier', None)

    if None in [title, body]:
        return Response({'status': False, 'result': messages.invalid_query}, status=422)

    if news_identifier is None and warning_identifier is None:
        return Response({'status': False, 'result': messages.invalid_query}, status=422)

    if news_identifier is not None and News.objects.filter(identifier=news_identifier).first() is None:
        return Response({'status': False, 'result': messages.no_record_found}, status=404)

    if warning_identifier is not None and WarningMessages.objects.filter(pk=warning_identifier).first() is None:
        return Response({'status': False, 'result': messages.no_record_found}, status=404)

    notification = Notification(title=title,
                                body=body,
                                news_identifier=news_identifier,
                                warning_identifier=warning_identifier)
    notification.save()

    # Trigger the push notification services
    notification_services = SendNotification(notification.identifier)
    if not notification_services.valid_notification:
        return Response(notification_services.setup_result, 422)
    notification_services.send_multicast_and_handle_errors()

    # Send response to end-user
    return Response({'status': True, 'result': 'push-notification accepted'}, status=200)


@swagger_auto_schema(**as_notification_get)
@api_view(['GET'])
def notification_get(request):
    """ Get notification  """
    query_params = request.GET.get('project-ids', None)
    sort_by = request.GET.get('sort-by', 'publication_date')
    sort_order = request.GET.get('sort-order', 'desc')

    if query_params is None:
        return Response({'status': False, 'result': messages.invalid_query}, status=422)
    project_identifiers = query_params.split(',')
    notifications = []
    for project_identifier in project_identifiers:
        project = Projects.objects.filter(pk=project_identifier).first()
        if project is not None and project.active is True:
            notifications += list(Notification.objects.filter(project_identifier=project_identifier).all())

    serializer = NotificationSerializer(notifications, many=True)
    if len(serializer.data) != 0:
        result = Sort().list_of_dicts(serializer.data, key=sort_by, sort_order=sort_order)
        return Response({'status': True, 'result': result}, status=200)
    return Response({'status': False, 'result': messages.no_record_found}, status=404)


@swagger_auto_schema(**as_warning_message_image_post)
@IsAuthorized
@api_view(['POST'])
def warning_messages_image_upload(request):
    """ Upload image for warning message
    """
    image_data = request.data.get('image', None)
    project_warning_id = request.data.get('project_warning_id', None)
    if None in [image_data, project_warning_id]:
        return Response({'status': False, 'result': messages.invalid_query}, status=422)

    if WarningMessages.objects.filter(pk=project_warning_id).first() is None:
        return Response({'status': False, 'result': messages.no_record_found}, status=404)

    if 'main' not in image_data:
        return Response({'status': False, 'result': messages.invalid_query}, status=422)

    if image_data.get('data', None) is None:
        return Response({'status': False, 'result': messages.invalid_query}, status=422)

    # Make sure we've got a boolean not a string
    image_data['main'] = bool(image_data['main'] in ['True', 'true', True])

    # Get description
    description = image_data.get('description', 'Warning Message')

    # Get image data and run ImageConversion
    data = base64.b64decode(image_data.get('data'))
    image_conversion = ImageConversion(data, description)
    result = image_conversion.run()
    if result is False:
        return Response({'status': False, 'result': messages.unsupported_image_format}, status=422)

    # Store images into DB and build warning-messages images list
    sources = []
    for key in image_conversion.images:  # pylint: disable=consider-using-dict-items
        # Build image object and save to database
        image = image_conversion.images[key]
        identifier = uuid.uuid4().hex
        image_object = Image(identifier=identifier,
                             size='{width}x{height}'.format(width=image['width'], height=image['height']),
                             url='db://amsterdam_app_api.warning_message/{identifier}'.format(identifier=identifier),
                             filename=image['filename'],
                             description=description,
                             mime_type=image['mime_type'],
                             data=image['data'])
        image_object.save()
        sources.append({
            "image_id": identifier,
            "mime_type": image['mime_type'],
            "width": image['width'],
            "height": image['height'],
        })

    # Update warning-message with new images
    warning_message_image = {
        "main": image_data.get('main'),
        "aspect_ratio": image_conversion.aspect_ratio,
        "description": description,
        "coordinates": image_conversion.gps_info,
        "landscape": image_conversion.landscape,
        "sources": sources  # list; created earlier
    }

    warning_message = WarningMessages.objects.filter(pk=project_warning_id).first()
    warning_message.images.append(warning_message_image)
    warning_message.save()

    return Response({'status': True, 'result': 'Images stored in database'}, status=200)
