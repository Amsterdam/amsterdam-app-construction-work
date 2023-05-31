""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""

from drf_yasg import openapi

from amsterdam_app_api.api_messages import Messages

message = Messages()


as_change_password = {
    # /api/v1/user/password
    "methods": ["POST"],
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(
                type=openapi.TYPE_STRING, description="identifier"
            ),
            "old_password": openapi.Schema(
                type=openapi.TYPE_STRING, description="identifier"
            ),
            "password": openapi.Schema(
                type=openapi.TYPE_STRING, description="identifier"
            ),
            "password_verify": openapi.Schema(
                type=openapi.TYPE_STRING, description="identifier"
            ),
        },
    ),
    "responses": {
        200: openapi.Response(
            "application/json",
            examples={
                "application/json": {"status": True, "result": "password update"}
            },
        ),
        401: openapi.Response(
            "application/json",
            examples={
                "application/json": {"status": False, "result": message.do_not_match}
            },
        ),
        422: openapi.Response(
            "application/json",
            examples={
                "application/json": {"status": False, "result": message.invalid_query}
            },
        ),
    },
    "tags": ["Users"],
}
