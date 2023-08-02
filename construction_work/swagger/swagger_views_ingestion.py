""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""

from drf_yasg import openapi

as_garbage_collector = {
    # /api/v1/project/news_by_project_id swagger_auto_schema
    "methods": ["GET"],
    "manual_parameters": [
        openapi.Parameter(
            "IngestAuthorization",
            openapi.IN_HEADER,
            description="IngestAuthorization authorization token",
            type=openapi.TYPE_STRING,
            required=True,
        ),
        openapi.Parameter(
            "date",
            openapi.IN_QUERY,
            description="Datestamp when last scraper run was finished",
            type=openapi.TYPE_STRING,
            required=True,
        ),
        openapi.Parameter(
            "project_type",
            openapi.IN_QUERY,
            description="['projects', 'stadsloket']",
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    "responses": {
        200: openapi.Response(
            "application/json",
            examples={"application/json": {"status": True, "result": []}},
        )
    },
    "tags": ["Ingestion"],
}
