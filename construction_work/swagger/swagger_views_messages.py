""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""


from drf_yasg import openapi

from construction_work.api_messages import Messages
from construction_work.serializers import (
    WarningImageSerializer,
    WarningMessageSerializer,
)
from construction_work.swagger.swagger_generic_objects import (
    coordinates,
    forbidden_403,
    header_device_authorization,
    header_jwt_authorization,
    header_user_authorization,
    not_found_404,
    query_id,
    query_project_id,
    query_sort_by,
    query_sort_order,
    query_warning_message_id,
    warning_message,
    warning_messages,
)

message = Messages()


image = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "main": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="main image"),
        "sources": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "uri": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
                    "width": openapi.Schema(
                        type=openapi.TYPE_INTEGER, description="width"
                    ),
                    "height": openapi.Schema(
                        type=openapi.TYPE_INTEGER, description="height"
                    ),
                },
            ),
        ),
        "landscape": openapi.Schema(
            type=openapi.TYPE_BOOLEAN, description="image orientation"
        ),
        "coordinates": coordinates,
        "description": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
        "aspect_ratio": openapi.Schema(
            type=openapi.TYPE_NUMBER, description="aspect ratio"
        ),
    },
)

images = openapi.Schema(type=openapi.TYPE_ARRAY, items=image)

as_warning_message_get = {
    # /api/v1/notification/messages/warning/get
    "methods": ["GET"],
    "manual_parameters": [header_device_authorization, query_id],
    "responses": {
        200: openapi.Response(
            "application/json",
            warning_message,
            examples={
                "application/json": {
                    "id": 1,
                    "meta_id": {"id": 1, "type": "warning"},
                    "images": [
                        {
                            "main": True,
                            "sources": [
                                {"uri": "https://...", "width": 1, "height": 1}
                            ],
                            "landscape": False,
                            "coordinates": {"lat": None, "lon": None},
                            "description": "image",
                            "aspect_ratio": 1,
                        }
                    ],
                    "title": "title",
                    "body": "body",
                    "publication_date": "2023-12-06T11:40:54.418000+01:00",
                    "modification_date": "2023-12-06T11:41:01.525000+01:00",
                    "author_email": "info@amsterdam.nl",
                    "project": 1,
                }
            },
        ),
        400: openapi.Response(
            "application/json",
            examples={"application/json": message.invalid_query},
        ),
        403: forbidden_403,
        404: not_found_404,
    },
    "tags": ["Projects"],
}

as_warning_message_post = {
    # /api/v1/notification/messages/warning
    "methods": ["POST"],
    "manual_parameters": [
        header_user_authorization,
    ],
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "title": openapi.Schema(type=openapi.TYPE_STRING, description="title"),
            "body": openapi.Schema(type=openapi.TYPE_STRING, description="full text"),
            "project_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="project id"),
            "project_manager_key": openapi.Schema(type=openapi.TYPE_STRING, description="project manager key (UUID)"),
        },
    ),
    "responses": {
        200: openapi.Response(
            "application/json",
            WarningMessageSerializer,
            examples={
                "application/json": {
                    "id": 11,
                    "title": "foobar title",
                    "body": "foobar body",
                    "publication_date": "2023-11-20T15:57:16.166948+01:00",
                    "modification_date": "2023-11-20T15:57:16.166978+01:00",
                    "author_email": "mock0@amsterdam.nl",
                    "project": 55,
                    "project_manager": 55,
                }
            },
        ),
        400: openapi.Response(
            "application/json",
            examples={"application/json": message.invalid_query},
        ),
        403: forbidden_403,
        404: not_found_404,
    },
    "tags": ["Projects"],
}

as_warning_message_patch = {
    # /api/v1/notification/messages/warning
    "methods": ["PATCH"],
    "manual_parameters": [header_jwt_authorization],
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "title": openapi.Schema(type=openapi.TYPE_STRING, description="title"),
            "body": openapi.Schema(type=openapi.TYPE_STRING, description="body text"),
            "id": openapi.Schema(type=openapi.TYPE_STRING, description="message id"),
        },
    ),
    "responses": {
        200: openapi.Response(
            "application/json",
            WarningMessageSerializer,
            examples={
                "application/json": {
                    "id": 6,
                    "title": "new title",
                    "body": "new body text",
                    "publication_date": "2023-11-20T15:51:37.080818+01:00",
                    "modification_date": "2023-11-20T15:51:37.097048+01:00",
                    "author_email": "mock0@amsterdam.nl",
                    "project": 27,
                    "project_manager": 27,
                }
            },
        ),
        400: openapi.Response(
            "application/json",
            examples={"application/json": message.invalid_query},
        ),
        403: forbidden_403,
        404: not_found_404,
    },
    "tags": ["Projects"],
}

as_warning_message_delete = {
    # /api/v1/asset swagger_auto_schema
    "methods": ["DELETE"],
    "manual_parameters": [
        header_jwt_authorization,
        query_warning_message_id,
    ],
    "responses": {
        200: openapi.Response(
            "application/json",
            examples={"application/json": "Message deleted"},
        ),
        400: openapi.Response(
            "application/json",
            examples={"application/json": message.invalid_query},
        ),
        403: forbidden_403,
    },
    "tags": ["Projects"],
}

as_warning_messages_get = {
    # /api/v1/notification/messages/warning/get
    "methods": ["GET"],
    "manual_parameters": [
        header_device_authorization,
        query_project_id,
        query_sort_by,
        query_sort_order,
    ],
    "responses": {
        200: openapi.Response(
            "application/json",
            warning_messages,
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "meta_id": {"id": 1, "type": "warning"},
                        "images": [
                            {
                                "main": True,
                                "sources": [
                                    {"uri": "https://...", "width": 1, "height": 1}
                                ],
                                "landscape": False,
                                "coordinates": {"lat": None, "lon": None},
                                "description": "image",
                                "aspect_ratio": 1,
                            }
                        ],
                        "title": "title",
                        "body": "body",
                        "publication_date": "2023-12-06T11:40:54.418000+01:00",
                        "modification_date": "2023-12-06T11:41:01.525000+01:00",
                        "author_email": "info@amsterdam.nl",
                        "project": 1,
                    }
                ]
            },
        ),
        400: openapi.Response(
            "application/json",
            examples={"application/json": message.invalid_query},
        ),
        403: forbidden_403,
        404: not_found_404,
    },
    "tags": ["Projects"],
}

as_notification_post = {
    # /api/v1/notification
    "methods": ["POST"],
    "manual_parameters": [header_user_authorization],
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "title": openapi.Schema(
                type=openapi.TYPE_STRING, description="Title of notification"
            ),
            "body": openapi.Schema(
                type=openapi.TYPE_STRING, description="Body of notification"
            ),
            "warning_id": openapi.Schema(
                type=openapi.TYPE_INTEGER, description="Warning identifier"
            ),
        },
    ),
    "responses": {
        200: openapi.Response(
            "application/json",
            examples={"application/json": "Push notifications sent"},
        ),
        400: openapi.Response(
            "application/json",
            examples={"application/json": message.invalid_query},
        ),
        403: forbidden_403,
        404: not_found_404,
    },
    "tags": ["Notifications"],
}

as_warning_message_image_post = {
    # /api/v1/notification/messages/image/post
    "methods": ["POST"],
    "manual_parameters": [header_user_authorization],
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "warning_id": openapi.Schema(
                type=openapi.TYPE_INTEGER, description="warning id"
            ),
            "image": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "main": openapi.Schema(
                        type=openapi.TYPE_BOOLEAN, description="<false|true>"
                    ),
                    "description": openapi.Schema(
                        type=openapi.TYPE_STRING, description="about this image"
                    ),
                    "data": openapi.Schema(
                        type=openapi.TYPE_STRING, description="base64 image data"
                    ),
                },
                required=["main", "data"],
            ),
        },
        required=["warning_id"],
    ),
    "responses": {
        200: openapi.Response(
            "application/json",
            WarningImageSerializer,
            examples={
                "application/json": {
                    "id": 234,
                    "is_main": False,
                    "warning": 3245,
                    "images": [34, 35, 36],
                }
            },
        ),
        400: openapi.Response(
            "application/json",
            examples={
                "application/json": [
                    message.invalid_query,
                    message.unsupported_image_format,
                ]
            },
        ),
        403: forbidden_403,
        404: not_found_404,
    },
    "tags": ["Projects"],
}
