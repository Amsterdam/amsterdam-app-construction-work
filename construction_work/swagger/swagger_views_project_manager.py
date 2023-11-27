""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""

from drf_yasg import openapi

from construction_work.api_messages import Messages
from construction_work.serializers import ProjectManagerSerializer
from construction_work.swagger.swagger_abstract_objects import (
    header_jwt_authorization,
    header_jwt_authorization_not_required,
    header_user_authorization,
    header_user_authorization_not_required,
)

message = Messages()


images = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="image id"),
            "aspectRatio": openapi.Schema(
                type=openapi.TYPE_NUMBER, description="aspect ratio"
            ),
            "alternativeText": openapi.Schema(
                type=openapi.TYPE_STRING, description="Alternative text"
            ),
            "sources": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "url": openapi.Schema(
                            type=openapi.TYPE_STRING, description="url"
                        ),
                        "width": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="width"
                        ),
                        "height": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="height"
                        ),
                    },
                ),
            ),
        },
    ),
)

projects = {
    "manager_key": openapi.Schema(type=openapi.TYPE_STRING, description="manager_key"),
    "email": openapi.Schema(type=openapi.TYPE_STRING, description="email"),
    "projects": openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Schema(type=openapi.TYPE_INTEGER, description="foreign_id"),
    ),
}

projects_augmented = {
    "manager_key": openapi.Schema(type=openapi.TYPE_STRING, description="manager_key"),
    "email": openapi.Schema(type=openapi.TYPE_STRING, description="email"),
    "projects": openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "foreign_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="foreign_id",
                ),
                "images": images,
                "subtitle": openapi.Schema(
                    type=openapi.TYPE_STRING, description="subtitle"
                ),
                "title": openapi.Schema(type=openapi.TYPE_STRING, description="title"),
            },
        ),
    ),
}

as_project_manager_get = {
    # /api/v1/project/news swagger_auto_schema
    "methods": ["GET"],
    "Description": "test",
    "manual_parameters": [
        header_user_authorization,
        openapi.Parameter(
            "manager_key",
            openapi.IN_QUERY,
            "Query project manager (optionally by manager_key)",
            type=openapi.TYPE_STRING,
            format="<uuid4>",
            required=False,
        ),
    ],
    "responses": {
        200: openapi.Response(
            "application/json",
            openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT, properties=projects_augmented
                ),
            ),
            examples={
                "application/json": {
                    "manager_key": "fa201b9e-1634-41e2-8646-ee7fdec93840",
                    "email": "j.doe@amsterdam.nl",
                    "projects": [382512, 472782, 190062],
                }
            },
        ),
        404: openapi.Response(
            description="Error response",
            schema=openapi.Schema(
                type=openapi.TYPE_STRING,
                format="text",
                description=message.no_record_found,
            ),
            examples={"application/json": message.no_record_found},
        ),
    },
    "tags": ["Project Manager"],
}


as_project_manager_delete = {
    # /api/v1/asset swagger_auto_schema
    "methods": ["DELETE"],
    "manual_parameters": [
        header_jwt_authorization,
        openapi.Parameter(
            "manager_key",
            openapi.IN_QUERY,
            description="Remove project manager by manager_key",
            type=openapi.TYPE_STRING,
            format="<uuid4>",
            required=True,
        ),
    ],
    "responses": {
        200: openapi.Response(
            description="Successful response",
            schema=openapi.Schema(
                type=openapi.TYPE_STRING,
                format="text",
                description="Project manager removed",
            ),
            examples={"application/json": "Project manager removed"},
        ),
        400: openapi.Response(
            description="Error response",
            schema=openapi.Schema(
                type=openapi.TYPE_STRING,
                format="text",
                description=message.invalid_query,
            ),
            examples={"application/json": message.invalid_query},
        ),
    },
    "tags": ["Project Manager"],
}


as_project_manager_post_patch = {
    # /api/v1/image swagger_auto_schema
    "methods": ["POST", "PATCH"],
    "manual_parameters": [
        header_user_authorization_not_required,
        header_jwt_authorization_not_required,
    ],
    "request_body": openapi.Schema(type=openapi.TYPE_OBJECT, properties=projects),
    "responses": {
        200: ProjectManagerSerializer,
        400: openapi.Response(
            description="Error response",
            schema=openapi.Schema(
                type=openapi.TYPE_STRING,
                format="text",
                description=message.invalid_query,
            ),
            examples={"application/json": message.invalid_query},
        ),
        404: openapi.Response(
            description="Error response",
            schema=openapi.Schema(
                type=openapi.TYPE_STRING,
                format="text",
                description=message.no_record_found,
            ),
            examples={"application/json": message.no_record_found},
        ),
    },
    "tags": ["Project Manager"],
}
