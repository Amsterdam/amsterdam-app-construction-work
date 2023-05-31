""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""

from drf_yasg import openapi

from amsterdam_app_api.api_messages import Messages
from amsterdam_app_api.serializers import ProjectManagerSerializer
from amsterdam_app_api.swagger.swagger_abstract_objects import images

message = Messages()

as_project_manager_get = {
    # /api/v1/project/news swagger_auto_schema
    "methods": ["GET"],
    "Description": "test",
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
            "Query project manager (optionally by identifier)",
            type=openapi.TYPE_STRING,
            format="<id>",
            required=False,
        ),
    ],
    "responses": {
        200: openapi.Response(
            "application/json",
            openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "identifier": openapi.Schema(
                            type=openapi.TYPE_STRING, description="identifier"
                        ),
                        "email": openapi.Schema(
                            type=openapi.TYPE_STRING, description="email"
                        ),
                        "projects": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "identifier": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="identifier",
                                    ),
                                    "images": images,
                                    "subtitle": openapi.Schema(
                                        type=openapi.TYPE_STRING, description="subtitle"
                                    ),
                                    "title": openapi.Schema(
                                        type=openapi.TYPE_STRING, description="title"
                                    ),
                                },
                            ),
                        ),
                    },
                ),
            ),
            examples={"application/json": {"status": True, "result": {}}},
        )
    },
    "tags": ["Projects"],
}


as_project_manager_delete = {
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
            "Remove project manager by identifier",
            type=openapi.TYPE_STRING,
            format="<identifier>",
            required=True,
        ),
    ],
    "responses": {
        200: openapi.Response(
            "application/json",
            examples={
                "application/json": {
                    "status": True,
                    "result": "Project manager removed",
                }
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


as_project_manager_post_patch = {
    # /api/v1/image swagger_auto_schema
    "methods": ["POST", "PATCH"],
    "manual_parameters": [
        openapi.Parameter(
            "UserAuthorization",
            openapi.IN_HEADER,
            description="authorization token",
            type=openapi.TYPE_STRING,
            required=True,
        )
    ],
    "request_body": ProjectManagerSerializer,
    "responses": {
        200: openapi.Response(
            "application/json",
            examples={
                "application/json": {
                    "status": True,
                    "result": "Project manager updated",
                }
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
