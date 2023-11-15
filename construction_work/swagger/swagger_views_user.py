""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""

from drf_yasg import openapi

from construction_work.api_messages import Messages

message = Messages()


as_change_password = {
    # /api/v1/user/password
    "methods": ["POST"],
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(type=openapi.TYPE_STRING, description="username"),
            "old_password": openapi.Schema(type=openapi.TYPE_STRING, description="old password"),
            "password": openapi.Schema(type=openapi.TYPE_STRING, description="new password"),
            "password_verify": openapi.Schema(type=openapi.TYPE_STRING, description="new password (verify)"),
        },
    ),
    "responses": {
        200: openapi.Response(
            "application/json",
            examples={"application/json": "password update"},
        ),
        400: openapi.Response(
            "application/json",
            examples={"application/json": message.invalid_query},
        ),
    },
    "tags": ["Users"],
}
