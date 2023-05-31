""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""


from drf_yasg import openapi

from amsterdam_app_api.api_messages import Messages
from amsterdam_app_api.serializers import (
    NotificationSerializer,
    WarningMessagesExternalSerializer,
)

message = Messages()


as_warning_message_post = {
    # /api/v1/notification/messages/warning
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
            "title": openapi.Schema(type=openapi.TYPE_STRING, description="title"),
            "body": openapi.Schema(type=openapi.TYPE_STRING, description="full text"),
            "project_identifier": openapi.Schema(
                type=openapi.TYPE_STRING, description="identifier"
            ),
            "project_manager_id": openapi.Schema(
                type=openapi.TYPE_STRING, description="identifier"
            ),
            "author_email": openapi.Schema(
                type=openapi.TYPE_STRING, description="author@amsterdam.nl"
            ),
        },
    ),
    "responses": {
        200: openapi.Response(
            "application/json",
            examples={
                "application/json": {
                    "status": True,
                    "result": {"warning_identifier": "identifier"},
                }
            },
        ),
        403: openapi.Response(
            "application/json",
            examples={
                "application/json": {"status": False, "result": message.access_denied}
            },
        ),
        404: openapi.Response(
            "application/json",
            examples={
                "application/json": {"status": False, "result": message.no_record_found}
            },
        ),
        422: openapi.Response(
            "application/json",
            examples={
                "application/json": {"status": False, "result": message.invalid_query}
            },
        ),
    },
    "tags": ["Projects"],
}

as_warning_message_patch = {
    # /api/v1/notification/messages/warning
    "methods": ["PATCH"],
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
            "title": openapi.Schema(type=openapi.TYPE_STRING, description="title"),
            "body": openapi.Schema(type=openapi.TYPE_STRING, description="full text"),
            "project_identifier": openapi.Schema(
                type=openapi.TYPE_STRING, description="identifier"
            ),
        },
    ),
    "responses": {
        200: openapi.Response(
            "application/json",
            examples={
                "application/json": {"status": True, "result": "Message patched"}
            },
        ),
        403: openapi.Response(
            "application/json",
            examples={
                "application/json": {"status": False, "result": message.access_denied}
            },
        ),
        404: openapi.Response(
            "application/json",
            examples={
                "application/json": {"status": False, "result": message.no_record_found}
            },
        ),
        422: openapi.Response(
            "application/json",
            examples={
                "application/json": {"status": False, "result": message.invalid_query}
            },
        ),
    },
    "tags": ["Projects"],
}

as_warning_message_delete = {
    # /api/v1/asset swagger_auto_schema
    "methods": ["DELETE"],
    "manual_parameters": [
        openapi.Parameter(
            "UserAuthorization",
            openapi.IN_HEADER,
            description="authorization token",
            type=openapi.TYPE_STRING,
            required=True,
        ),
        openapi.Parameter(
            "id",
            openapi.IN_QUERY,
            "Warning message identifier",
            type=openapi.TYPE_STRING,
            format="<identifier>",
            required=True,
        ),
    ],
    "responses": {
        200: openapi.Response(
            "application/json",
            examples={
                "application/json": {"status": True, "result": "Message deleted"}
            },
        ),
        403: openapi.Response("Error: Forbidden"),
        422: openapi.Response(
            "application/json",
            examples={
                "application/json": {"status": False, "result": message.invalid_query}
            },
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
            WarningMessagesExternalSerializer,
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
    "manual_parameters": [
        openapi.Parameter(
            "id",
            openapi.IN_QUERY,
            "Query by identifier",
            type=openapi.TYPE_STRING,
            format="<identifier>",
            required=False,
        )
    ],
    "responses": {
        200: openapi.Response(
            "application/json",
            WarningMessagesExternalSerializer,
            examples={"application/json": {"status": True, "result": {}}},
        ),
        404: openapi.Response("Error: Not Found"),
        422: openapi.Response("Error: Unprocessable Entity"),
    },
    "tags": ["Projects"],
}

as_notification_post = {
    # /api/v1/notification/messages/push/send
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
    "request_body": NotificationSerializer,
    "responses": {
        200: openapi.Response(
            "application/json",
            examples={
                "application/json": {
                    "status": True,
                    "result": "push-notification accepted",
                }
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
                "application/json": {"status": False, "result": message.invalid_query}
            },
        ),
    },
    "tags": ["Notifications"],
}

as_notification_get = {
    # /api/v1/notification/messages/push/get
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
                "application/json": {"status": False, "result": message.access_denied}
            },
        ),
        404: openapi.Response(
            "application/json",
            examples={
                "application/json": {"status": False, "result": message.no_record_found}
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
