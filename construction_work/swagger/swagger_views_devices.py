""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""

from drf_yasg import openapi

from construction_work.api_messages import Messages
from construction_work.swagger.swagger_generic_objects import (
    forbidden_403,
    header_device_authorization,
    header_device_id,
    not_found_404,
)

message = Messages()


as_device_register_post = {
    # /api/v1/device/register swagger_auto_schema
    "methods": ["POST"],
    "manual_parameters": [header_device_authorization, header_device_id],
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
            examples={"application/json": "Registration added"},
        ),
        400: openapi.Response(
            "application/json",
            examples={"application/json": message.invalid_query},
        ),
        403: forbidden_403,
        404: not_found_404,
    },
    "tags": ["Devices"],
}


as_device_register_delete = {
    # /api/v1/device/register swagger_auto_schema
    "methods": ["DELETE"],
    "manual_parameters": [header_device_authorization, header_device_id],
    "responses": {
        200: openapi.Response(
            "application/json",
            examples={"application/json": "Registration removed"},
        ),
        400: openapi.Response(
            "application/json",
            examples={"application/json": message.invalid_headers},
        ),
        403: forbidden_403,
        404: not_found_404,
    },
    "tags": ["Devices"],
}
