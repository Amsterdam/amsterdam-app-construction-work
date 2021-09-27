from drf_yasg import openapi
from amsterdam_app_api.serializers import WarningMessagesExternalSerializer
from amsterdam_app_api.serializers import PushNotificationSerializer
from amsterdam_app_api.api_messages import Messages

message = Messages()


as_warning_message_post = {
    # /api/v1/notification/messages/warning/create
    'methods': ['POST'],
    'manual_parameters': [openapi.Parameter('UserAuthorization',
                                            openapi.IN_HEADER,
                                            description="authorization token",
                                            type=openapi.TYPE_STRING)],
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, description='identifier'),
            'body': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'preface': openapi.Schema(type=openapi.TYPE_STRING, description='short text'),
                'content': openapi.Schema(type=openapi.TYPE_STRING, description='full text')
            }),
            'project_identifier': openapi.Schema(type=openapi.TYPE_STRING, description='identifier'),
            'project_manager_token': openapi.Schema(type=openapi.TYPE_STRING, description='identifier'),
            'author_email': openapi.Schema(type=openapi.TYPE_STRING, description='author@amsterdam.nl'),
        }
    ),
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
    'manual_parameters': [openapi.Parameter('UserAuthorization',
                                            openapi.IN_HEADER,
                                            description="authorization token",
                                            type=openapi.TYPE_STRING)],
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

as_warning_message_image_post = {
    # /api/v1/notification/messages/image/post
    'methods': ['POST'],
    'manual_parameters': [openapi.Parameter('UserAuthorization',
                                            openapi.IN_HEADER,
                                            description="authorization token",
                                            type=openapi.TYPE_STRING)],
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'project_warning_id': openapi.Schema(type=openapi.TYPE_STRING, description='identifier'),
            'image': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'type': openapi.Schema(type=openapi.TYPE_STRING, description='<header|additional>'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='about this image'),
                'data': openapi.Schema(type=openapi.TYPE_STRING, description='base64 image data')
            })
        }
    ),
    'responses': {
        200: openapi.Response('application/json', examples={
            'application/json': {
                'status': True,
                'result': 'Image stored in database'
            }
        }),
        404: openapi.Response('application/json', examples={
            'application/json': {
                'status': False,
                'result': message.no_record_found
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