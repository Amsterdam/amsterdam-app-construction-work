from amsterdam_app_api.api_messages import Messages
from amsterdam_app_api.models import WarningMessages
from amsterdam_app_api.models import Projects
from amsterdam_app_api.models import ProjectManager
from amsterdam_app_api.models import PushNotification
from amsterdam_app_api.serializers import WarningMessagesExternalSerializer
from amsterdam_app_api.PushNotifications.SendNotification import SendNotification
from rest_framework.decorators import api_view
from rest_framework.response import Response
from amsterdam_app_api.swagger_views_messages import as_warning_message_post
from amsterdam_app_api.swagger_views_messages import as_warning_message_get
from amsterdam_app_api.swagger_views_messages import as_push_notification_post
from drf_yasg.utils import swagger_auto_schema

message = Messages()


@swagger_auto_schema(**as_warning_message_post)
@api_view(['POST'])
def warning_message_post(request):
    """ Post a warning message. Only warnings by a valid Project manager for a valid project are allowed.
    """
    title = request.data.get('title', None)
    project_identifier = request.data.get('project_identifier', None)
    project_manager_token = request.data.get('project_manager_token', None)
    body = request.data.get('body', {})

    if None in [title, project_identifier, project_manager_token]:
        return Response({'status': False, 'result': message.invalid_query}, status=422)
    elif not isinstance(body.get('preface', None), str):
        return Response({'status': False, 'result': message.invalid_query}, status=422)
    elif not isinstance(body.get('content', None), str):
        return Response({'status': False, 'result': message.invalid_query}, status=422)
    elif Projects.objects.filter(pk=project_identifier).first() is None:
        return Response({'status': False, 'result': message.invalid_query}, status=422)

    # Check if the project manager exists and is entitled for sending a message for this project
    project_manager = ProjectManager.objects.filter(pk=project_manager_token).first()
    if project_manager is None:
        return Response({'status': False, 'result': message.no_record_found}, status=404)
    elif project_identifier not in project_manager.projects:
        return Response({'status': False, 'result': message.no_record_found}, status=404)

    message_object = WarningMessages(title=title,
                                     body=body,
                                     project_identifier=project_identifier,
                                     project_manager_token=project_manager_token,
                                     images=[])
    message_object.save()
    return Response({'status': True, 'result': {'warning_identifier': message_object.identifier}}, status=200)


@swagger_auto_schema(**as_warning_message_get)
@api_view(['GET'])
def warning_message_get(request):
    project_identifier = request.GET.get('id', None)
    if project_identifier is None:
        return Response({'status': False, 'result': message.invalid_query}, status=422)
    elif Projects.objects.filter(pk=project_identifier).first() is None:
        return Response({'status': False, 'result': message.no_record_found}, status=404)
    else:
        warning_messages_objects = WarningMessages.objects.filter(project_identifier=project_identifier).all()
        serializer = WarningMessagesExternalSerializer(warning_messages_objects, many=True)
        return Response({'status': True, 'result': serializer.data}, status=200)


@swagger_auto_schema(**as_push_notification_post)
@api_view(['POST'])
def push_notification_post(request):
    title = request.data.get('title', None)
    body = request.data.get('body', None)
    news_identifier = request.data.get('news_identifier', None)
    warning_identifier = request.data.get('warning_identifier', None)

    if None in [title, body]:
        return Response({'status': False, 'result': message.invalid_query}, status=422)
    elif news_identifier is None and warning_identifier is None:
        return Response({'status': False, 'result': message.invalid_query}, status=422)

    push_notification = PushNotification(title=title,
                                         body=body,
                                         news_identifier=news_identifier,
                                         warning_identifier=warning_identifier)
    push_notification.save()

    # Trigger the push notification services
    notification_services = SendNotification(push_notification.identifier)
    notification_services.send()

    return Response({'status': True, 'result': 'push-notification accepted'}, status=200)


