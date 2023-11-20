""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""


from drf_yasg import openapi

from construction_work.api_messages import Messages
from construction_work.serializers import (
    NotificationSerializer,
    WarningMessagePublicSerializer,
    WarningMessageSerializer,
)
from construction_work.swagger.swagger_abstract_objects import (
    coordinates,
    header_user_authorization,
    query_id,
    query_warning_message_id,
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
                    "url": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
                    "width": openapi.Schema(type=openapi.TYPE_INTEGER, description="width"),
                    "height": openapi.Schema(type=openapi.TYPE_INTEGER, description="height"),
                },
            ),
        ),
        "landscape": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="image orientation"),
        "coordinates": coordinates,
        "description": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
        "aspect_ratio": openapi.Schema(type=openapi.TYPE_NUMBER, description="aspect ratio"),
    },
)

images = openapi.Schema(type=openapi.TYPE_ARRAY, items=image)

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
            "project_identifier": openapi.Schema(type=openapi.TYPE_STRING, description="identifier"),
            "project_manager_id": openapi.Schema(type=openapi.TYPE_STRING, description="identifier"),
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
        403: openapi.Response(
            "application/json",
            examples={"application/json": message.no_record_found},
        ),
        404: openapi.Response(
            "application/json",
            examples={"application/json": message.no_record_found},
        ),
    },
    "tags": ["Projects"],
}

as_warning_message_patch = {
    # /api/v1/notification/messages/warning
    "methods": ["PATCH"],
    "manual_parameters": [header_user_authorization],
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
        404: openapi.Response(
            "application/json",
            examples={"application/json": message.no_record_found},
        ),
    },
    "tags": ["Projects"],
}

as_warning_message_delete = {
    # /api/v1/asset swagger_auto_schema
    "methods": ["DELETE"],
    "manual_parameters": [
        header_user_authorization,
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
    },
    "tags": ["Projects"],
}

as_warning_messages_get = {
    # /api/v1/notification/messages/warning/get
    "methods": ["GET"],
    "manual_parameters": [
        openapi.Parameter(
            "id",
            openapi.IN_QUERY,
            "Query by project-identifier",
            type=openapi.TYPE_STRING,
            format="<identifier>",
            required=False,
        ),
        openapi.Parameter(
            "sort-by",
            openapi.IN_QUERY,
            "Sort response (default: modification_date)",
            type=openapi.TYPE_STRING,
            format="<any key from model>",
            required=False,
        ),
        openapi.Parameter(
            "sort-order",
            openapi.IN_QUERY,
            "Sorting order (default: asc)",
            type=openapi.TYPE_STRING,
            format="<asc, desc>",
            required=False,
        ),
    ],
    "responses": {
        200: openapi.Response(
            "application/json",
            WarningMessagePublicSerializer,
            examples={"application/json": {"status": True, "result": []}},
        ),
        404: openapi.Response("Error: Not Found"),
        422: openapi.Response("Error: Unprocessable Entity"),
    },
    "tags": ["Projects"],
}

as_warning_message_get = {
    # /api/v1/notification/messages/warning/get
    "methods": ["GET"],
    "manual_parameters": [query_id],
    "responses": {
        200: openapi.Response(
            "application/json",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_STRING, description="id"),
                    "images": images,
                    "title": openapi.Schema(type=openapi.TYPE_STRING, description="id"),
                    "body": openapi.Schema(type=openapi.TYPE_STRING, description="body"),
                    "modification_date": openapi.Schema(type=openapi.TYPE_STRING, description="datetime"),
                    "publication_date": openapi.Schema(type=openapi.TYPE_STRING, description="datetime"),
                    "author_email": openapi.Schema(type=openapi.TYPE_STRING, description="author email"),
                },
            ),
            examples={
                "application/json": {
                    "id": 3,
                    "images": [
                        {
                            "main": True,
                            "landscape": False,
                            "coordinates": {"lat": 52.14435833333333, "lon": 6.182558333333334},
                            "description": "unittest",
                            "aspect_ratio": 1.33,
                            "sources": [
                                [{"url": "http://testserver/api/v1/image?id=1", "width": 135, "height": 180}],
                                [{"url": "http://testserver/api/v1/image?id=2", "width": 324, "height": 432}],
                                [{"url": "http://testserver/api/v1/image?id=3", "width": 540, "height": 720}],
                                [{"url": "http://testserver/api/v1/image?id=4", "width": 810, "height": 1080}],
                                [{"url": "http://testserver/api/v1/image?id=5", "width": 3302, "height": 4032}],
                            ],
                        }
                    ],
                    "title": "foobar title",
                    "body": "foobar body",
                    "publication_date": "2023-11-20T14:53:45.841084+01:00",
                    "modification_date": "2023-11-20T14:53:45.841124+01:00",
                    "author_email": "mock0@amsterdam.nl",
                }
            },
        ),
        400: openapi.Response(
            "application/json",
            examples={"application/json": message.invalid_query},
        ),
        404: openapi.Response(
            "application/json",
            examples={"application/json": message.no_record_found},
        ),
    },
    "tags": ["Projects"],
}

as_notification_post = {
    # /api/v1/notification
    "methods": ["POST"],
    "manual_parameters": [
        header_user_authorization
    ],
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
        404: openapi.Response(
            "application/json",
            examples={"application/json": message.no_record_found},
        ),
    },
    "tags": ["Notifications"],
}

as_notification_get = {
    # /api/v1/notifications
    "methods": ["GET"],
    "manual_parameters": [
        openapi.Parameter(
            "project-ids",
            openapi.IN_QUERY,
            "Query push-notifications by project-identifier(s)",
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_STRING),
            required=True,
        ),
        openapi.Parameter(
            "sort-by",
            openapi.IN_QUERY,
            "Sort response (default: publication_date)",
            type=openapi.TYPE_STRING,
            format="<any key from model>",
            required=False,
        ),
        openapi.Parameter(
            "sort-order",
            openapi.IN_QUERY,
            "Sorting order (default: desc)",
            type=openapi.TYPE_STRING,
            format="<asc, desc>",
            required=False,
        ),
    ],
    "responses": {
        200: openapi.Response(
            "application/json",
            NotificationSerializer,
            examples={"application/json": {"status": True, "result": []}},
        ),
        422: openapi.Response("Error: Unprocessable Entity"),
    },
    "tags": ["Notifications"],
}

as_warning_message_image_post = {
    # /api/v1/notification/messages/image/post
    "methods": ["POST"],
    "manual_parameters": [
        openapi.Parameter(
            "UserAuthorization",
            openapi.IN_HEADER,
            description="authorization token",
            type=openapi.TYPE_STRING,
            required=True,
        )
    ],
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "project_warning_id": openapi.Schema(
                type=openapi.TYPE_STRING, description="identifier"
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
            ),
        },
    ),
    "responses": {
        200: openapi.Response(
            "application/json",
            examples={
                "application/json": {
                    "status": True,
                    "result": "Images stored in database",
                }
            },
        ),
        403: openapi.Response(
            "application/json",
            examples={
                "application/json": {"status": False, "result": messages.access_denied}
            },
        ),
        404: openapi.Response(
            "application/json",
            examples={
                "application/json": {
                    "status": False,
                    "result": message.no_record_found,
                }
            },
        ),
        422: openapi.Response(
            "application/json",
            examples={
                "application/json": {
                    "status": False,
                    "result": "{invalid}|{unsupported}".format(
                        invalid=message.invalid_query,
                        unsupported=message.unsupported_image_format,
                    ),
                }
            },
        ),
    },
    "tags": ["Projects"],
}
