from drf_yasg import openapi
from amsterdam_app_api.serializers import MobileDevicesSerializer
from amsterdam_app_api.views_messages import Messages

message = Messages()


""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""

as_push_notifications_registration = {
    # /api/v1/image swagger_auto_schema
    'methods': ['POST', 'PATCH', 'DELETE'],
    'request_body': MobileDevicesSerializer,
    'responses': {
        200: openapi.Response('application/json',
                              examples={
                                  'application/json': {
                                      'status': True,
                                      'result': 'Device registration updated'}}),
        422: openapi.Response('application/json',
                              examples={
                                  'application/json': {
                                      'status': True,
                                      'result': message.invalid_query}})
    },
    'tags': ['Push-Notifications']
}
