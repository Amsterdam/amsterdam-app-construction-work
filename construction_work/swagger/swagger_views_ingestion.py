""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""

from drf_yasg import openapi

identifiers = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    description="List of ids to be deactivated or deleted",
    items=openapi.Schema(type=openapi.TYPE_STRING, description="identifier"),
)

datetime = openapi.Schema(type=openapi.TYPE_STRING, description="ETL epoch (%Y-%m-%d %H:%M:%S.%f)")

as_garbage_collector = {
    # /api/v1/project/news_by_project_id swagger_auto_schema
    "methods": ["POST"],
    "manual_parameters": [
        openapi.Parameter(
            "IngestAuthorization",
            openapi.IN_HEADER,
            description="IngestAuthorization authorization token",
            type=openapi.TYPE_STRING,
            required=True,
        )
    ],
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={"etl_epoch_string": datetime, "project_ids": identifiers, "article_ids": identifiers},
    ),
    "responses": {
        200: openapi.Response(
            "application/json",
            examples={
                "application/json": {"projects": {"active": 0, "inactive": 0}, "articles": {"deleted": 0, "active": 0}}
            },
        )
    },
    "tags": ["Ingestion"],
}
