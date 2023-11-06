""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""

from drf_yasg import openapi

from construction_work.api_messages import Messages
from construction_work.swagger.swagger_abstract_objects import (
    foreign_id,
    header_device_authorization,
    header_device_id,
    project_details_schema,
    projects_schema,
    query_address,
    query_article_max_age,
    query_fields,
    query_foreign_id,
    query_id,
    query_latitude,
    query_longitude,
    query_page,
    query_page_size,
    query_query_fields,
    query_text,
)

message = Messages()

#
# Actual Apidocs
#

as_projects = {
    # /api/v1/projects swagger_auto_schema
    "methods": ["GET"],
    "manual_parameters": [
        header_device_id,
        query_article_max_age,
        query_latitude,
        query_longitude,
        query_address,
        query_page_size,
        query_page,
    ],
    "responses": {
        200: openapi.Response(
            "application/json",
            projects_schema,
            examples={
                "application/json": {
                    "result": [
                        {
                            "id": 34,
                            "title": "Slotermeer",
                            "subtitle": "stedelijke vernieuwing",
                            "image": {
                                "id": 21360354,
                                "aspectRatio": 1.7816091954022988,
                                "alternativeText": None,
                                "sources": [
                                    {
                                        "url": "/publish/pages/960128/slotermeer.jpg",
                                        "width": 620,
                                        "height": 348,
                                    },
                                    {
                                        "url": "/publish/pages/960128/220px/slotermeer.jpg",
                                        "width": 220,
                                        "height": 123,
                                    },
                                    {
                                        "url": "/publish/pages/960128/80px/slotermeer.jpg",
                                        "width": 80,
                                        "height": 45,
                                    },
                                ],
                            },
                            "followed": True,
                            "strides": 3242,
                            "meters": 4552,
                            "recent_articles": [],
                            "project_id": 343,
                        }
                    ],
                    "page": {
                        "number": 2,
                        "size": 1,
                        "totalElements": 329,
                        "totalPages": 329,
                    },
                    "_links": {
                        "self": {"href": "http://localhost:8000/api/v1/projects"},
                        "next": {
                            "href": "http://localhost:8000/api/v1/projects?page=3&page_size=1&lat=52.3676379&lon=4.8968271"
                        },
                        "previous": {
                            "href": "http://localhost:8000/api/v1/projects?page=1&page_size=1&lat=52.3676379&lon=4.8968271"
                        },
                    },
                }
            },
        ),
        400: openapi.Response(message.invalid_query),
    },
    "tags": ["Projects"],
}


as_project_details = {
    # /api/v1/project/details swagger_auto_schema
    "methods": ["get"],
    "manual_parameters": [
        header_device_id,
        header_device_authorization,
        query_id,
        query_article_max_age,
        query_latitude,
        query_longitude,
        query_address,
    ],
    "responses": {
        200: openapi.Response(
            "application/json",
            project_details_schema,
            examples={
                "application/json": {
                    "followed": False,
                    "recent_articles": [],
                    "meter": None,
                    "strides": None,
                    "followers": 5,
                    "foreign_id": 1003333,
                    "active": True,
                    "last_seen": "2023-10-12T10:54:50.907421+02:00",
                    "title": "Slotermeer",
                    "subtitle": "stedelijke vernieuwing",
                    "coordinates": None,
                    "sections": {
                        "what": [
                            {
                                "body": "<div><p>We werken samen met bewoners, woningcorporaties, besturen van scholen en andere partijen aan de vernieuwing van Slotermeer. We gaan woningen en gebouwen van scholen vernieuwen. Ook richten we de openbare ruimte waar nodig opnieuw in en knappen speelplekken op.</p></div>",
                                "title": "Opknapbeurt",
                            }
                        ],
                        "when": [],
                        "work": [],
                        "where": [],
                        "contact": [],
                    },
                    "contacts": [
                        {
                            "id": 16800775,
                            "name": "Kees Vissers",
                            "email": "k.vissers@amsterdam.nl",
                            "phone": None,
                            "position": "Projectmanager",
                        }
                    ],
                    "timeline": {
                        "intro": None,
                        "items": [
                            {
                                "body": "<div><ul><li>bouw 260 nieuwe woningen</li><li>opknappen 370 woningen</li></ul></div>",
                                "items": [],
                                "title": "2021 - 2026: Rousseaubuurt",
                                "collapsed": True,
                            }
                        ],
                        "title": "Wanneer",
                    },
                    "image": {
                        "id": 21360354,
                        "sources": [
                            {
                                "url": "/publish/pages/960128/slotermeer.jpg",
                                "width": 620,
                                "height": 348,
                            },
                            {
                                "url": "/publish/pages/960128/220px/slotermeer.jpg",
                                "width": 220,
                                "height": 123,
                            },
                            {
                                "url": "/publish/pages/960128/80px/slotermeer.jpg",
                                "width": 80,
                                "height": 45,
                            },
                        ],
                        "aspectRatio": 1.7816091954022988,
                        "alternativeText": None,
                    },
                    "images": [],
                    "url": "http://www.amsterdam.nl/projecten/slotermeer/",
                    "creation_date": "2016-09-29T14:25:00+02:00",
                    "modification_date": "2023-10-02T06:34:00+02:00",
                    "publication_date": "2023-10-02T06:34:00+02:00",
                    "expiration_date": None,
                }
            },
        ),
        400: openapi.Response(message.invalid_query),
        404: openapi.Response(message.no_record_found),
    },
    "tags": ["Projects"],
}


as_projects_search = {
    # /api/v1/XXX/search swagger_auto_schema
    "methods": ["get"],
    "manual_parameters": [
        query_text,
        query_fields,
        query_query_fields,
        query_address,
        query_article_max_age,
        query_latitude,
        query_longitude,
        query_page,
        query_page_size,
    ],
    "responses": {
        200: openapi.Response("application/json", projects_schema),
        400: openapi.Response(f"{message.invalid_query}|{message.no_such_field_in_model}"),
    },
    "tags": ["Search"],
}


as_project_follow_post = {
    # /api/v1/image swagger_auto_schema
    "methods": ["POST"],
    "manual_parameters": [header_device_authorization, header_device_id],
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT, properties={"id": openapi.Schema(type=openapi.TYPE_INTEGER, description="project id")}
    ),
    "responses": {
        200: openapi.Response(
            "application/json",
            examples={"application/json": "Subscription added"},
        ),
        400: openapi.Response(
            "application/json",
            examples={"application/json": [message.invalid_parameters, message.invalid_headers]},
        ),
        404: openapi.Response(
            "application/json",
            examples={"application/json": message.no_record_found},
        ),
    },
    "tags": ["Projects"],
}


as_project_follow_delete = {
    # /api/v1/image swagger_auto_schema
    "methods": ["DELETE"],
    "manual_parameters": [header_device_authorization, header_device_id],
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={"project_id": openapi.Schema(type=openapi.TYPE_STRING, description="Project identifier")},
    ),
    "responses": {
        200: openapi.Response(
            "application/json",
            examples={"application/json": "Subscription removed"},
        ),
        403: openapi.Response(
            "application/json",
            examples={"application/json": message.access_denied},
        ),
        400: openapi.Response(
            "application/json",
            examples={"application/json": [message.invalid_parameters, message.invalid_headers]},
        ),
        404: openapi.Response(
            "application/json",
            examples={"application/json": message.no_record_found},
        ),
    },
    "tags": ["Projects"],
}


as_projects_followed_articles = {
    # /api/v1/project/followed/articles swagger_auto_schema
    "methods": ["get"],
    "manual_parameters": [header_device_id, query_article_max_age],
    "responses": {
        200: openapi.Response(
            "application/json",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "status": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="status"),
                    "result": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "projects": openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={"<identifier>": foreign_id},
                            )
                        },
                    ),
                },
            ),
            examples={"application/json": {"status": True, "result": {}}},
        )
    },
    "tags": ["Projects"],
}
