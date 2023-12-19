""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""

from drf_yasg import openapi

from construction_work.serializers import ArticleSerializer
from construction_work.swagger.swagger_generic_objects import (
    forbidden_403,
    header_device_authorization,
    images,
    meta_id,
    not_found_404,
    query_id,
    query_limit,
    query_project_ids,
    query_sort_by,
    query_sort_order,
)
from construction_work.views.views_messages import Messages

messages = Messages()


as_article_get = {
    # /api/v1/project/news swagger_auto_schema
    "methods": ["GET"],
    "manual_parameters": [header_device_authorization, query_id],
    "responses": {
        200: openapi.Response(
            "Article details",
            ArticleSerializer,
            examples={
                "application/json": {
                    "id": 54321,
                    "meta_id": {"id": 54321, "type": "article"},
                    "foreign_id": 987654321,
                    "active": True,
                    "last_seen": "2023-10-19T16:37:10.316472+02:00",
                    "title": "Over de Sportheldenbuurt",
                    "intro": "<div>intro</div>",
                    "body": "<div>body</div>",
                    "image": {
                        "id": 243215678,
                        "sources": [
                            {
                                "url": "http://...",
                                "width": 940,
                                "height": 415,
                            }
                        ],
                        "aspectRatio": 2.2650602409638556,
                        "alternativeText": None,
                    },
                    "url": "http://...",
                    "creation_date": "2015-11-30T13:46:00+01:00",
                    "modification_date": "2021-11-05T09:13:00+01:00",
                    "publication_date": "2021-11-05T09:13:00+01:00",
                    "expiration_date": None,
                    "projects": [53, 26],
                }
            },
        ),
        400: openapi.Response(
            "Invalid query",
            examples={"application/json": messages.invalid_query},
        ),
        403: forbidden_403,
        404: not_found_404,
    },
    "tags": ["Projects"],
}


as_articles_get = {
    # /api/v1/articles
    "methods": ["GET"],
    "manual_parameters": [
        header_device_authorization,
        query_project_ids,
        query_limit,
        query_sort_by,
        query_sort_order,
    ],
    "responses": {
        200: openapi.Response(
            "application/json",
            openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "meta_id": meta_id,
                        "title": openapi.Schema(
                            type=openapi.TYPE_STRING, description="title"
                        ),
                        "images": images,
                        "publication_date": openapi.Schema(
                            type=openapi.TYPE_STRING, description="year-month-day"
                        ),
                    },
                ),
            ),
            examples={
                "application/json": [
                    {
                        "meta_id": {"type": "article", "id": 45},
                        "title": "title",
                        "images": [
                            {
                                "id": 23148339,
                                "sources": [
                                    {
                                        "url": "https://...",
                                        "width": 940,
                                        "height": 415,
                                    }
                                ],
                                "aspectRatio": 2.2650602409638556,
                                "alternativeText": None,
                            }
                        ],
                        "publication_date": "2023-10-30T11:54:00Z",
                    }
                ]
            },
        ),
        400: openapi.Response(
            "application/json",
            examples={"application/json": messages.invalid_query},
        ),
        403: forbidden_403,
    },
    "tags": ["Projects"],
}
