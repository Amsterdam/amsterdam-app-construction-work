""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""

from drf_yasg import openapi

from amsterdam_app_api.serializers import NewsSerializer
from amsterdam_app_api.views.views_messages import Messages

messages = Messages()


as_news_by_project_id = {
    # /api/v1/project/news_by_project_id swagger_auto_schema
    "methods": ["GET"],
    "manual_parameters": [
        openapi.Parameter(
            "project-identifier",
            openapi.IN_QUERY,
            "Query by news project-identifier",
            type=openapi.TYPE_STRING,
            format="<brug, kade>",
            required=False,
        ),
        openapi.Parameter(
            "sort-by",
            openapi.IN_QUERY,
            "Sort response (default=publication_date)",
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
            NewsSerializer,
            examples={"application/json": {"status": True, "result": []}},
        ),
        405: openapi.Response("Error: Method not allowed"),
        422: openapi.Response("Error: Unprocessable Entity"),
    },
    "tags": ["Projects"],
}

as_news = {
    # /api/v1/project/news swagger_auto_schema
    "methods": ["GET"],
    "manual_parameters": [
        openapi.Parameter(
            "id",
            openapi.IN_QUERY,
            "Query by news identifier",
            type=openapi.TYPE_STRING,
            format="<identifier>",
            required=True,
        )
    ],
    "responses": {
        200: openapi.Response(
            "application/json",
            NewsSerializer,
            examples={"application/json": {"status": True, "result": []}},
        ),
        404: openapi.Response("Error: No record found"),
        405: openapi.Response("Error: Method not allowed"),
        422: openapi.Response("Error: Unprocessable Entity"),
    },
    "tags": ["Projects"],
}


as_articles_get = {
    # /api/v1/articles
    "methods": ["GET"],
    "manual_parameters": [
        openapi.Parameter(
            "project-ids",
            openapi.IN_QUERY,
            "Query articles by project-identifier(s)",
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_STRING),
            required=False,
        ),
        openapi.Parameter(
            "limit",
            openapi.IN_QUERY,
            "Limit returned items",
            type=openapi.TYPE_INTEGER,
            format="<int>",
            required=False,
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
            openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "identifier": openapi.Schema(
                            type=openapi.TYPE_STRING, description="identifier"
                        ),
                        "title": openapi.Schema(
                            type=openapi.TYPE_STRING, description="title"
                        ),
                        "publication_date": openapi.Schema(
                            type=openapi.TYPE_STRING, description="year-month-day"
                        ),
                        "type": openapi.Schema(
                            type=openapi.TYPE_STRING, description="<news|warning>>"
                        ),
                        "image": openapi.Schema(
                            type=openapi.TYPE_OBJECT, properties={}
                        ),
                    },
                ),
            ),
            examples={"application/json": {"status": True, "result": {}}},
        )
    },
    "tags": ["Articles", "Projects"],
}
