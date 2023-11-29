""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. """
from drf_yasg import openapi

from construction_work.serializers import ArticleSerializer, ProjectSerializer
from construction_work.swagger.swagger_abstract_objects import (
    forbidden_403,
    header_ingest_authorization,
)

#
# Re-usable snippets
#

identifiers = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    description="List of ids to be deactivated or deleted",
    items=openapi.Schema(type=openapi.TYPE_STRING, description="identifier"),
)

datetime = openapi.Schema(
    type=openapi.TYPE_STRING, description="ETL epoch (%Y-%m-%d %H:%M:%S.%f)"
)

modification_dates = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "foreign_id": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "modification_date": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="datetime (%Y-%m-%d %H:%M:%S%z)",
                ),
            },
        )
    },
)

serializer_error = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "field name": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_STRING, description="error description"
            ),
        )
    },
)


#
# OpenAPI definitions
#

as_garbage_collector = {
    "methods": ["POST"],
    "manual_parameters": [header_ingest_authorization],
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={"project_ids": identifiers, "article_ids": identifiers},
    ),
    "responses": {
        200: openapi.Response(
            "application/json",
            examples={
                "application/json": {
                    "projects": {
                        "active": 300,
                        "inactive": 12,
                        "deleted": 4,
                        "count": 312,
                    },
                    "articles": {"deleted": 12, "count": 563},
                }
            },
        ),
        403: forbidden_403,
    },
    "tags": ["Ingestion"],
}


as_etl_get = {
    "methods": ["get"],
    "manual_parameters": [header_ingest_authorization],
    "responses": {
        200: openapi.Response(
            "application/json",
            modification_dates,
            examples={
                "application/json": {
                    "155581": {"modification_date": "2023-10-11 11:36:00+00:00"}
                }
            },
        ),
        403: forbidden_403,
    },
    "tags": ["Ingestion"],
}


as_etl_project_post = {
    "methods": ["POST"],
    "manual_parameters": [header_ingest_authorization],
    "request_body": ProjectSerializer,
    "responses": {
        200: openapi.Response(
            "application/json",
            ProjectSerializer,
            examples={
                "application/json": {
                    "id": 334,
                    "foreign_id": 1293650,
                    "active": True,
                    "last_seen": "2023-10-19T15:09:44.620037+02:00",
                    "title": "Title",
                    "subtitle": "Sub-title",
                    "coordinates": None,
                    "sections": {
                        "what": [
                            {
                                "title": "Wat",
                                "body": "<div><p>Wat</p></div>",
                            }
                        ],
                        "where": [
                            {
                                "title": "Waar",
                                "body": "<div><p>Waar</p></div>",
                            }
                        ],
                        "when": [
                            {
                                "title": "Wanneer",
                                "body": "<div><p>Wanneer</p></div>",
                            }
                        ],
                        "work": [
                            {
                                "title": "Werk",
                                "body": "<div><p>Werk</p></div>",
                            }
                        ],
                        "contact": [{"title": "Contact", "body": None}],
                    },
                    "contacts": [
                        {
                            "id": 17335235,
                            "name": "Lars Wouters",
                            "position": "Projectmanager",
                            "phone": None,
                            "email": "info@ovamsterdamhaarlemmermeer.nl",
                        }
                    ],
                    "timeline": {
                        "title": "Wanneer",
                        "intro": None,
                        "items": [
                            {
                                "title": "2017",
                                "body": "<div><p>body</p></div>",
                                "items": [],
                                "collapsed": True,
                            },
                            {
                                "title": "2022",
                                "body": "<div><p>body</p></div>",
                                "items": [],
                                "collapsed": True,
                            },
                            {
                                "title": "2023",
                                "body": "<div><p>body</p></div>",
                                "items": [],
                                "collapsed": False,
                            },
                            {
                                "title": "2025",
                                "body": "<div><p>body</p></div>",
                                "items": [],
                                "collapsed": True,
                            },
                        ],
                    },
                    "image": {
                        "id": 23223227,
                        "alternativeText": None,
                        "aspectRatio": 1.7816091954022988,
                        "sources": [
                            {
                                "url": "/publish/pages/1043581/940x_stationsgebied_hoofddorp_1.jpg",
                                "width": 620,
                                "height": 348,
                            },
                            {
                                "url": "/publish/pages/1043581/220px/940x_stationsgebied_hoofddorp_1.jpg",
                                "width": 220,
                                "height": 123,
                            },
                            {
                                "url": "/publish/pages/1043581/80px/940x_stationsgebied_hoofddorp_1.jpg",
                                "width": 80,
                                "height": 45,
                            },
                        ],
                    },
                    "images": [],
                    "url": "http://www.amsterdam.nl/projecten/amsterdam-haarlemmermeer/",
                    "creation_date": "2023-10-18T13:32:00+02:00",
                    "modification_date": "2023-10-18T17:13:00+02:00",
                    "publication_date": "2023-10-18T17:13:00+02:00",
                    "expiration_date": None,
                }
            },
        ),
        400: openapi.Response(
            "application/json",
            serializer_error,
            examples={"projects": ["This list may not be empty."]},
        ),
        403: forbidden_403,
    },
    "tags": ["Ingestion"],
}


as_etl_article_post = {
    "methods": ["POST"],
    "manual_parameters": [header_ingest_authorization],
    "request_body": ArticleSerializer,
    "responses": {
        200: openapi.Response(
            "application/json",
            ArticleSerializer,
            examples={
                "application/json": {
                    "foreign_id": 165556,
                    "active": True,
                    "last_seen": "2023-10-19T16:47:03.787677+02:00",
                    "title": "Title",
                    "intro": "<div><p>intro</p></div>",
                    "body": "<div><h3>body</h3></div>",
                    "image": None,
                    "type": "work",
                    "url": "http://www.amsterdam.nl/projecten/ndsm-werf/plannen/",
                    "creation_date": "2009-01-20T15:32:00+01:00",
                    "modification_date": "2023-08-21T11:07:00+02:00",
                    "publication_date": "2023-08-21T11:07:00+02:00",
                    "expiration_date": None,
                    "projects": [1],
                }
            },
        ),
        400: openapi.Response(
            "application/json",
            serializer_error,
            examples={"projects": ["This list may not be empty."]},
        ),
        403: forbidden_403,
    },
    "tags": ["Ingestion"],
}
