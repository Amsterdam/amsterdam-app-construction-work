""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""

from drf_yasg import openapi

from amsterdam_app_api.api_messages import Messages

message = Messages()


as_device_register_post = {
    # /api/v1/image swagger_auto_schema
    "methods": ["POST"],
    "manual_parameters": [
        openapi.Parameter(
            "DeviceAuthorization",
            openapi.IN_HEADER,
            description="Device authorization token",
            type=openapi.TYPE_STRING,
            required=True,
        ),
        openapi.Parameter(
            "deviceId",
            openapi.IN_HEADER,
            description="device identifier",
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "firebase_token": openapi.Schema(
                type=openapi.TYPE_STRING, description="firebase_token"
            ),
            "os": openapi.Schema(
                type=openapi.TYPE_STRING, description="os [ios|android]"
            ),
        },
    ),
    "responses": {
        200: openapi.Response(
            "application/json",
            examples={
                "application/json": {"status": True, "result": "Registration added"}
            },
        ),
        403: openapi.Response(
            "application/json",
            examples={
                "application/json": {"status": False, "result": message.access_denied}
            },
        ),
        422: openapi.Response(
            "application/json",
            examples={
                "application/json": {"status": False, "result": message.invalid_headers}
            },
        ),
    },
    "tags": ["Devices"],
}


as_device_register_delete = {
    # /api/v1/image swagger_auto_schema
    "methods": ["DELETE"],
    "manual_parameters": [
        openapi.Parameter(
            "DeviceAuthorization",
            openapi.IN_HEADER,
            description="Device authorization token",
            type=openapi.TYPE_STRING,
            required=True,
        ),
        openapi.Parameter(
            "deviceId",
            openapi.IN_HEADER,
            description="device identifier",
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    "responses": {
        200: openapi.Response(
            "application/json",
            examples={
                "application/json": {"status": True, "result": "Registration removed"}
            },
        ),
        403: openapi.Response(
            "application/json",
            examples={
                "application/json": {"status": False, "result": message.access_denied}
            },
        ),
        422: openapi.Response(
            "application/json",
            examples={
                "application/json": {"status": False, "result": message.invalid_headers}
            },
        ),
    },
    "tags": ["Devices"],
}
