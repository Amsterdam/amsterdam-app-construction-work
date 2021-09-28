import base64
import io
import uuid
from PIL import Image as PILImage
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from functools import reduce
from drf_yasg.utils import swagger_auto_schema
from amsterdam_app_api.GenericFunctions.IsAuthorized import IsAuthorized
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
from amsterdam_app_api.swagger_views_messages import as_warning_message_post
from amsterdam_app_api.swagger_views_messages import as_warning_message_get
from amsterdam_app_api.swagger_views_messages import as_notification_post
from amsterdam_app_api.swagger_views_messages import as_notification_get
from amsterdam_app_api.swagger_views_messages import as_warning_message_image_post

message = Messages()


@swagger_auto_schema(**as_warning_message_get)
@swagger_auto_schema(**as_warning_message_post)
@api_view(['GET', 'POST'])
def warning_message_crud(request):
    if request.method == 'POST':
        data = warning_message_post(request)
        return Response(data['result'], status=data['status_code'])
    elif request.method == 'GET':
        data = warning_message_get(request)
        return Response(data['result'], status=data['status_code'])


@IsAuthorized
def warning_message_post(request):
    """ Post a warning message. Only warnings by a valid Project manager for a valid project are allowed.
    """
    title = request.data.get('title', None)
    project_identifier = request.data.get('project_identifier', None)
    project_manager_token = request.data.get('project_manager_token', None)
    body = request.data.get('body', {})

    if None in [title, project_identifier, project_manager_token]:
        return {'result': {'status': False, 'result': message.invalid_query}, 'status_code': 422}
    elif not isinstance(body.get('preface', None), str):
        return {'result': {'status': False, 'result': message.invalid_query}, 'status_code': 422}
    elif not isinstance(body.get('content', None), str):
        return {'result': {'status': False, 'result': message.invalid_query}, 'status_code': 422}
    elif Projects.objects.filter(pk=project_identifier).first() is None:
        return {'result': {'status': False, 'result': message.invalid_query}, 'status_code': 422}

    # Check if the project manager exists and is entitled for sending a message for this project
    project_manager = ProjectManager.objects.filter(pk=project_manager_token).first()
    if project_manager is None:
        return {'result': {'status': False, 'result': message.no_record_found}, 'status_code': 404}
    elif project_identifier not in project_manager.projects:
        return {'result': {'status': False, 'result': message.no_record_found}, 'status_code': 404}

    message_object = WarningMessages(title=title,
                                     body=body,
                                     project_identifier=project_identifier,
                                     project_manager_token=project_manager_token,
                                     images=[])
    message_object.save()
    return {'result': {'status': True, 'result': {'warning_identifier': message_object.identifier}}, 'status_code': 200}


def warning_message_get(request):
    project_identifier = request.GET.get('id', None)
    if project_identifier is None:
        return {'result': {'status': False, 'result': message.invalid_query}, 'status_code': 422}
    elif Projects.objects.filter(pk=project_identifier).first() is None:
        return {'result': {'status': False, 'result': message.no_record_found}, 'status_code': 404}
    else:
        warning_messages_objects = WarningMessages.objects.filter(project_identifier=project_identifier).all()
        serializer = WarningMessagesExternalSerializer(warning_messages_objects, many=True)
        return {'result': {'status': True, 'result': serializer.data}, 'status_code': 200}


@swagger_auto_schema(**as_notification_post)
@IsAuthorized
@api_view(['POST'])
def notification_post(request):
    title = request.data.get('title', None)
    body = request.data.get('body', None)
    news_identifier = request.data.get('news_identifier', None)
    warning_identifier = request.data.get('warning_identifier', None)

    if None in [title, body, warning_identifier]:
        Response({'status': False, 'result': message.invalid_query}, status=422)
    elif news_identifier is None and warning_identifier is None:
        Response({'status': False, 'result': message.invalid_query}, status=422)
    elif news_identifier is not None and News.objects.filter(pk=news_identifier).first() is None:
        Response({'status': False, 'result': message.no_record_found}, status=404)
    elif WarningMessages.objects.filter(pk=warning_identifier).first() is None:
        Response({'status': False, 'result': message.no_record_found}, status=404)

    notification = Notification(title=title,
                                body=body,
                                news_identifier=news_identifier,
                                warning_identifier=warning_identifier)
    notification.save()

    # Trigger the push notification services
    notification_services = SendNotification(notification.identifier)
    notification_services.send()
    Response({'status': True, 'result': 'push-notification accepted'}, status=200)


@swagger_auto_schema(**as_notification_get)
@api_view(['GET'])
def notification_get(request):
    query_params = request.GET.get('project-ids', None)
    if query_params is None:
        Response({'status': False, 'result': message.invalid_query}, status=422)
    project_identifiers = query_params.split(',')
    query = reduce(lambda q, value: q | Q(project_identifier=value), project_identifiers, Q())
    notifications = Notification.objects.filter(query).all()
    serializer = NotificationSerializer(notifications, many=True)

    Response({'status': True, 'result': serializer.data}, status=200)

@swagger_auto_schema(**as_warning_message_image_post)
@IsAuthorized
@api_view(['POST'])
def warning_messages_image_upload(request):
    """ Upload image for warning message
    """
    image_data = request.data.get('image', None)
    project_warning_id = request.data.get('project_warning_id', None)
    if None in [image_data, project_warning_id]:
        return Response({'status': False, 'result': message.invalid_query}, status=422)
    elif WarningMessages.objects.filter(pk=project_warning_id).first() is None:
        return Response({'status': False, 'result': message.no_record_found}, status=404)
    elif image_data.get('type', None) not in ['header', 'additional']:
        return Response({'status': False, 'result': message.invalid_query}, status=422)
    elif image_data.get('data', None) is None:
        return Response({'status': False, 'result': message.invalid_query}, status=422)

    # Get image meta-data
    data = base64.b64decode(image_data.get('data'))
    buffer = io.BytesIO(data)
    pil_image = PILImage.open(buffer)

    # Create identifier for image object
    identifier = uuid.uuid4().hex

    # Build image object and save to database
    image_object = Image(identifier=identifier,
                         size='{width}px'.format(width=pil_image.width),
                         url='db://amsterdam_app_api.warning_message/{identifier}'.format(identifier=identifier),
                         filename='db://amsterdam_app_api.warning_message/{identifier}'.format(identifier=identifier),
                         description=image_data.get('description', ''),
                         mime_type=pil_image.get_format_mimetype(),
                         data=data)
    image_object.save()

    # Update warning-message with new image
    warning_message_image = {
        "type": image_data.get('type'),
        "sources": {
            "{width}px".format(width=pil_image.width): {
                "url": "db://amsterdam_app_api.warning_message/{identifier}".format(identifier=identifier),
                "image_id": identifier,
                "filename": "db://amsterdam_app_api.warning_message/{identifier}".format(identifier=identifier),
                "description": image_data.get('description', '')},
        }
    }

    warning_message = WarningMessages.objects.filter(pk=project_warning_id).first()
    warning_message.images.append(warning_message_image)
    warning_message.save()

    return Response({'status': True, 'result': 'Image stored in database'}, status=200)
