""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""

from drf_yasg import openapi

from construction_work.api_messages import Messages
from construction_work.swagger.swagger_abstract_objects import (
    query_address,
    query_article_max_age,
    query_latitude,
    query_longitude,
)

messages = Messages()


link_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "href": openapi.Schema(
            type=openapi.TYPE_STRING,
        ),
    },
)


pagination_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "result": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            description="List of requested data",
            items=openapi.Schema(type=openapi.TYPE_OBJECT),
        ),
        "page": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "number": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                ),
                "size": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                ),
                "totalElements": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                ),
                "totalPages": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                ),
            },
        ),
        "_links": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "self": link_schema,
                "next": link_schema,
                "previous": link_schema,
            },
        ),
    },
)

as_search = {
    # /api/v1/XXX/search swagger_auto_schema
    "methods": ["get"],
    "manual_parameters": [
        openapi.Parameter(
            "text",
            openapi.IN_QUERY,
            "text to search for",
            type=openapi.TYPE_STRING,
            format="<string>",
            required=True,
        ),
        openapi.Parameter(
            "query_fields",
            openapi.IN_QUERY,
            "comma separated field(s) on which to operate your query",
            type=openapi.TYPE_STRING,
            format="<string,string,...>",
            required=True,
        ),
        openapi.Parameter(
            "fields",
            openapi.IN_QUERY,
            "comma separated field(s) which are returned from the model",
            type=openapi.TYPE_STRING,
            format="<string,string,...>",
            required=False,
        ),
        openapi.Parameter(
            "page_size",
            openapi.IN_QUERY,
            "Limit items per page for paginated result",
            type=openapi.TYPE_INTEGER,
            format="<int (default:10)>",
            required=False,
        ),
        openapi.Parameter(
            "page",
            openapi.IN_QUERY,
            "Page from paginated result",
            type=openapi.TYPE_INTEGER,
            format="<int (default:1)>",
            required=False,
        ),
    ],
    "responses": {
        200: openapi.Response("application/json", pagination_schema),
        422: openapi.Response("{a}|{b}".format(a=messages.invalid_query, b=messages.no_such_field_in_model)),
    },
    "tags": ["Search"],
}
