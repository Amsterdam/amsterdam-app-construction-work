from drf_yasg import openapi
from amsterdam_app_api.serializers import WarningMessagesInternalSerializer
from amsterdam_app_api.serializers import WarningMessagesExternalSerializer
from amsterdam_app_api.serializers import PushNotificationSerializer
from amsterdam_app_api.api_messages import Messages

message = Messages()


as_warning_message_post = {
    # /api/v1/notification/messages/warning/create
    'methods': ['POST'],
    'request_body': WarningMessagesInternalSerializer,
    'responses': {
        200: openapi.Response('application/json', examples={
            'application/json': {
                'status': True,
                'result': {'warning_identifier': 'identifier'}}
        }),
        404: openapi.Response('application/json', examples={
            'application/json': {
                'status': False,
                'result': message.no_record_found}
        }),
        422: openapi.Response('application/json', examples={
            'application/json': {
                'status': False,
                'result': message.invalid_query
            }
        })
    },
    'tags': ['(push-) Notifications']
}

as_warning_message_get = {
    # /api/v1/notification/messages/warning/get
    'methods': ['GET'],
    'manual_parameters': [openapi.Parameter('id',
                                            openapi.IN_QUERY,
                                            'Query by project-identifier',
                                            type=openapi.TYPE_STRING,
                                            format='<identifier>',
                                            required=True)],
    'responses': {
        200: openapi.Response('application/json',
                              WarningMessagesExternalSerializer,
                              examples={'application/json': {'status': True, 'result': []}}),
        404: openapi.Response('Error: Not Found'),
        422: openapi.Response('Error: Unprocessable Entity')
    },
    'tags': ['(push-) Notifications']
}

as_push_notification_post = {
    # /api/v1/notification/messages/push/send
    'methods': ['POST'],
    'request_body': PushNotificationSerializer,
    'responses': {
        200: openapi.Response('application/json', examples={
            'application/json': {
                'status': True,
                'result': 'push-notification accepted'
            }
        }),
        422: openapi.Response('application/json', examples={
            'application/json': {
                'status': False,
                'result': message.invalid_query
            }
        })
    },
    'tags': ['(push-) Notifications']
}

as_push_notification_get = {
    # /api/v1/notification/messages/push/get
    'methods': ['GET'],
    'manual_parameters': [openapi.Parameter('project-ids',
                                            openapi.IN_QUERY,
                                            'Query push-notifications by project-identifier(s)',
                                            type=openapi.TYPE_ARRAY,
                                            items=openapi.Items(type=openapi.TYPE_STRING),
                                            required=True)],
    'responses': {
        200: openapi.Response('application/json',
                              PushNotificationSerializer,
                              examples={'application/json': {'status': True, 'result': []}}),
        422: openapi.Response('Error: Unprocessable Entity')
    },
    'tags': ['(push-) Notifications']
}
