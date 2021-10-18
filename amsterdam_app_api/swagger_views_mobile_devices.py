from drf_yasg import openapi
from amsterdam_app_api.serializers import MobileDevicesSerializer
from amsterdam_app_api.api_messages import Messages

message = Messages()


""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""

as_push_notifications_registration_device_delete = {
    # /api/v1/asset swagger_auto_schema
    'methods': ['DELETE'],
    'manual_parameters': [openapi.Parameter('id',
                                            openapi.IN_QUERY,
                                            'Mobile device identifier',
                                            type=openapi.TYPE_STRING,
                                            format='<identifier>',
                                            required=True),
                          openapi.Parameter('DeviceAuthorization',
                                            openapi.IN_HEADER,
                                            description="Device authorization token",
                                            type=openapi.TYPE_STRING)],
    'responses': {
        200: openapi.Response('application/json',
                              examples={
                                  'application/json': {
                                      'status': True,
                                      'result': 'Device removed from database'}}),
        403: openapi.Response('Error: Forbidden'),
        422: openapi.Response('application/json',
                              examples={
                                  'application/json': {
                                      'status': False,
                                      'result': message.invalid_query}})
    },
    'tags': ['Consumers']
}


as_push_notifications_registration_device_post = {
    # /api/v1/image swagger_auto_schema
    'methods': ['POST'],
    'manual_parameters': [openapi.Parameter('DeviceAuthorization',
                                            openapi.IN_HEADER,
                                            description="Device authorization token",
                                            type=openapi.TYPE_STRING)],
    'request_body': MobileDevicesSerializer,
    'responses': {
        200: openapi.Response('application/json',
                              examples={
                                  'application/json': {
                                      'status': True,
                                      'result': 'Device registration updated'}}),
        403: openapi.Response('Error: Forbidden'),
        422: openapi.Response('application/json',
                              examples={
                                  'application/json': {
                                      'status': False,
                                      'result': message.invalid_query}})
    },
    'tags': ['Consumers']
}

as_push_notifications_registration_device_patch = {
    # /api/v1/image swagger_auto_schema
    'methods': ['PATCH'],
    'manual_parameters': [openapi.Parameter('DeviceAuthorization',
                                            openapi.IN_HEADER,
                                            description="Device authorization token",
                                            type=openapi.TYPE_STRING)],
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'device_token': openapi.Schema(type=openapi.TYPE_STRING, description='device_token'),
            'device_refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='device_refresh_token'),
            'os_type': openapi.Schema(type=openapi.TYPE_STRING, description='<android|ios>'),
            'projects': dict(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description='project_identifier')
        }
    ),
    'responses': {
        200: openapi.Response('application/json',
                              examples={
                                  'application/json': {
                                      'status': True,
                                      'result': 'Device registration updated'}}),
        403: openapi.Response('Error: Forbidden'),
        422: openapi.Response('application/json',
                              examples={
                                  'application/json': {
                                      'status': False,
                                      'result': message.invalid_query}})
    },
    'tags': ['Consumers']
}