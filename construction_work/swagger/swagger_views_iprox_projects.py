""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""

from drf_yasg import openapi

from construction_work.api_messages import Messages
from construction_work.generic_functions.static_data import ARTICLE_MAX_AGE_PARAM
from construction_work.serializers import (
    ProjectDetailsSerializer,
    ProjectListSerializer,
)
from construction_work.swagger.swagger_views_search import pagination_schema

message = Messages()

article_identifiers = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(type=openapi.TYPE_STRING, description="article identifier"),
)

body_element = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "html": openapi.Schema(type=openapi.TYPE_STRING, description="html"),
            "text": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
            "title": openapi.Schema(type=openapi.TYPE_STRING, description="title"),
        },
    ),
)

news = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "url": openapi.Schema(type=openapi.TYPE_STRING, description="url"),
            "identifier": openapi.Schema(
                type=openapi.TYPE_STRING, description="identifier"
            ),
            "project_identifier": openapi.Schema(
                type=openapi.TYPE_STRING, description="project identifier"
            ),
        },
    ),
)

timeline = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "title": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "html": openapi.Schema(type=openapi.TYPE_STRING, description="html"),
                "text": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
            },
        ),
        "intro": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "html": openapi.Schema(type=openapi.TYPE_STRING, description="html"),
                "text": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
            },
        ),
        "items": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "title": openapi.Schema(
                        type=openapi.TYPE_STRING, description="text"
                    ),
                    "collapsed": openapi.Schema(
                        type=openapi.TYPE_BOOLEAN, description="collapsed"
                    ),
                    "progress": openapi.Schema(
                        type=openapi.TYPE_STRING, description="current progress"
                    ),
                    "content": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "title": openapi.Schema(
                                    type=openapi.TYPE_STRING, description="text"
                                ),
                                "body": openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        "html": openapi.Schema(
                                            type=openapi.TYPE_STRING, description="html"
                                        ),
                                        "text": openapi.Schema(
                                            type=openapi.TYPE_STRING, description="text"
                                        ),
                                    },
                                ),
                            },
                        ),
                    ),
                },
            ),
        ),
    },
)


as_projects = {
    # /api/v1/projects swagger_auto_schema
    "methods": ["GET"],
    "manual_parameters": [
        openapi.Parameter(
            "deviceId",
            openapi.IN_HEADER,
            description="Device identifier",
            type=openapi.TYPE_STRING,
            required=True,
        ),
        openapi.Parameter(
            ARTICLE_MAX_AGE_PARAM,
            openapi.IN_QUERY,
            description="Number of days (default: 3)",
            type=openapi.TYPE_INTEGER,
            format="int",
            required=False,
        ),
        openapi.Parameter(
            "lat",
            openapi.IN_QUERY,
            description="Latitude",
            type=openapi.TYPE_STRING,
            format="float",
            required=False,
        ),
        openapi.Parameter(
            "lon",
            openapi.IN_QUERY,
            description="Longitude",
            type=openapi.TYPE_STRING,
            format="float",
            required=False,
        ),
        openapi.Parameter(
            "address",
            openapi.IN_QUERY,
            description="Address (street and number)",
            type=openapi.TYPE_STRING,
            format="string",
            required=False,
        ),
        openapi.Parameter(
            "page_size",
            openapi.IN_QUERY,
            description="Number of results per page (default 10)",
            type=openapi.TYPE_INTEGER,
            format="int",
            required=False,
        ),
        openapi.Parameter(
            "page",
            openapi.IN_QUERY,
            description="Page number",
            type=openapi.TYPE_INTEGER,
            format="int",
            required=False,
        ),
    ],
    "responses": {
        200: openapi.Response(
            "application/json",
            pagination_schema,
            examples={
                "application/json": {
                    "result": [
                        {
                            "id": 34,
                            "followed": True,
                            "foreign_id": 1003333,
                            "active": True,
                            "last_seen": "2023-10-12T10:54:50.907421+02:00",
                            "title": "Slotermeer",
                            "subtitle": "stedelijke vernieuwing",
                            "coordinates": {"lat": 52.3584996, "lon": 4.8035019},
                            "sections": {
                                "what": [
                                    {
                                        "body": "",
                                        "title": "Vernieuwd stadscentrum voor heel Nieuw-West",
                                    }
                                ],
                                "when": [{"body": None, "title": "Wanneer"}],
                                "work": [],
                                "where": [],
                                "contact": [],
                            },
                            "contacts": [
                                {
                                    "id": 16800775,
                                    "name": "",
                                    "email": "",
                                    "phone": None,
                                    "position": "",
                                }
                            ],
                            "timeline": {
                                "intro": None,
                                "items": [
                                    {
                                        "body": "",
                                        "items": [],
                                        "title": "",
                                        "collapsed": True,
                                    }
                                ],
                                "title": "",
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
        400: openapi.Response(
            "Invalid header(s). See /api/v1/apidocs for more information"
        ),
    },
    "tags": ["Projects"],
}


as_project_details = {
    # /api/v1/project/details swagger_auto_schema
    "methods": ["get"],
    "manual_parameters": [
        openapi.Parameter(
            "deviceId",
            openapi.IN_HEADER,
            description="Device identifier",
            type=openapi.TYPE_STRING,
            required=True,
        ),
        openapi.Parameter(
            "foreign_id",
            openapi.IN_QUERY,
            description="Project identifier",
            type=openapi.TYPE_INTEGER,
            format="int",
            required=True,
        ),
        openapi.Parameter(
            ARTICLE_MAX_AGE_PARAM,
            openapi.IN_QUERY,
            description="Number of days (default: 3)",
            type=openapi.TYPE_INTEGER,
            format="int",
            required=False,
        ),
        openapi.Parameter(
            "lat",
            openapi.IN_QUERY,
            description="Latitude",
            type=openapi.TYPE_STRING,
            format="float",
            required=False,
        ),
        openapi.Parameter(
            "lon",
            openapi.IN_QUERY,
            description="Longitude",
            type=openapi.TYPE_STRING,
            format="float",
            required=False,
        ),
        openapi.Parameter(
            "address",
            openapi.IN_QUERY,
            description="Address (street and number)",
            type=openapi.TYPE_STRING,
            format="string",
            required=False,
        ),
    ],
    "responses": {
        200: openapi.Response(
            "application/json",
            # ProjectDetailsSerializer,
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
        400: openapi.Response(
            "Invalid header(s). See /api/v1/apidocs for more information"
        ),
        404: openapi.Response("No record found"),
    },
    "tags": ["Projects"],
}


as_projects_follow_post = {
    # /api/v1/image swagger_auto_schema
    "methods": ["POST"],
    "manual_parameters": [
        openapi.Parameter(
            "DeviceAuthorization",
            openapi.IN_HEADER,
            description="Device authorization token",
            type=openapi.TYPE_STRING,
            required=True,
        ),
        openapi.Parameter(
            "deviceId",
            openapi.IN_HEADER,
            description="Device identifier",
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "foreign_id": openapi.Schema(
                type=openapi.TYPE_STRING, description="Project identifier"
            )
        },
    ),
    "responses": {
        200: openapi.Response(
            "application/json",
            examples={"application/json": "Subscription added"},
        ),
        403: openapi.Response(
            "application/json",
            examples={"application/json": message.access_denied},
        ),
        400: openapi.Response(
            "application/json",
            examples={"application/json": message.invalid_headers},
        ),
        400: openapi.Response(
            "application/json",
            examples={"application/json": message.invalid_parameters},
        ),
        404: openapi.Response(
            "application/json",
            examples={"application/json": message.no_record_found},
        ),
    },
    "tags": ["Projects"],
}


as_projects_follow_delete = {
    # /api/v1/image swagger_auto_schema
    "methods": ["DELETE"],
    "manual_parameters": [
        openapi.Parameter(
            "DeviceAuthorization",
            openapi.IN_HEADER,
            description="Device authorization token",
            type=openapi.TYPE_STRING,
            required=True,
        ),
        openapi.Parameter(
            "deviceId",
            openapi.IN_HEADER,
            description="Device identifier",
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "project_id": openapi.Schema(
                type=openapi.TYPE_STRING, description="Project identifier"
            )
        },
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
            examples={"application/json": message.invalid_headers},
        ),
        400: openapi.Response(
            "application/json",
            examples={"application/json": message.invalid_parameters},
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
    "manual_parameters": [
        openapi.Parameter(
            "deviceId",
            openapi.IN_HEADER,
            description="device identifier",
            type=openapi.TYPE_STRING,
            required=True,
        ),
        openapi.Parameter(
            "article-max-age",
            openapi.IN_QUERY,
            "Number of days (default: 3)",
            type=openapi.TYPE_INTEGER,
            format="<int>",
            required=False,
        ),
    ],
    "responses": {
        200: openapi.Response(
            "application/json",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "status": openapi.Schema(
                        type=openapi.TYPE_BOOLEAN, description="status"
                    ),
                    "result": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "projects": openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={"<identifier>": article_identifiers},
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
