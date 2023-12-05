""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""

from copy import copy

from drf_yasg import openapi

from construction_work.api_messages import Messages
from construction_work.swagger.swagger_generic_objects import (
    forbidden_403,
    get_paginated_schema,
    header_device_authorization,
    header_device_id,
    meta_id,
    not_found_404,
    project_details_schema,
    project_id,
    project_schema,
    query_address,
    query_article_max_age,
    query_fields,
    query_id,
    query_latitude,
    query_longitude,
    query_page,
    query_page_size,
    query_project_ids,
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
        header_device_authorization,
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
            get_paginated_schema(project_schema),
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
                            "meter": 4552,
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
        403: forbidden_403,
    },
    "tags": ["Projects"],
}


as_project_details = {
    # /api/v1/project/details swagger_auto_schema
    "methods": ["get"],
    "manual_parameters": [
        header_device_authorization,
        header_device_id,
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
                    "recent_articles": [
                        {
                            "id": 1,
                            "meta_id": {"id": 1, "type": "article"},
                            "foreign_id": 165556,
                            "active": True,
                            "last_seen": "2023-12-05T11:21:42.508600+01:00",
                            "title": "Plannen en publicaties NDSM-werf",
                            "intro": "<div><p>Plannen, besluiten en notities over NDSM.</p></div>",
                            "body": "<div></div>",
                            "image": {
                                "id": 21654735,
                                "sources": [
                                    {
                                        "url": "https://www.amsterdam.nl/publish/pages/856043/230726-ndsm-werf-west-bouwontwikkelingen_si-071.jpg",
                                        "width": 940,
                                        "height": 415,
                                    },
                                    {
                                        "url": "https://www.amsterdam.nl/publish/pages/856043/220px/230726-ndsm-werf-west-bouwontwikkelingen_si-071.jpg",
                                        "width": 220,
                                        "height": 97,
                                    },
                                    {
                                        "url": "https://www.amsterdam.nl/publish/pages/856043/460px/230726-ndsm-werf-west-bouwontwikkelingen_si-071.jpg",
                                        "width": 460,
                                        "height": 203,
                                    },
                                    {
                                        "url": "https://www.amsterdam.nl/publish/pages/856043/700px/230726-ndsm-werf-west-bouwontwikkelingen_si-071.jpg",
                                        "width": 700,
                                        "height": 309,
                                    },
                                    {
                                        "url": "https://www.amsterdam.nl/publish/pages/856043/80px/230726-ndsm-werf-west-bouwontwikkelingen_si-071.jpg",
                                        "width": 80,
                                        "height": 35,
                                    },
                                ],
                                "aspectRatio": 2.2650602409638556,
                                "alternativeText": None,
                            },
                            "url": "http://www.amsterdam.nl/projecten/ndsm-werf/plannen/",
                            "creation_date": "2009-01-20T15:32:00+01:00",
                            "modification_date": "2023-08-21T11:07:00+02:00",
                            "publication_date": "2023-08-21T11:07:00+02:00",
                            "expiration_date": None,
                            "projects": [1],
                        }
                    ],
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
        403: forbidden_403,
        404: not_found_404,
    },
    "tags": ["Projects"],
}

as_projects_search = copy(as_projects)
as_projects_search["manual_parameters"] = [
    header_device_authorization,
    query_text,
    query_fields,
    query_query_fields,
    query_address,
    query_article_max_age,
    query_latitude,
    query_longitude,
    query_page,
    query_page_size,
]
as_projects_search["tags"] = ["Search"]


as_project_follow_post = {
    # /api/v1/image swagger_auto_schema
    "methods": ["POST"],
    "manual_parameters": [header_device_authorization, header_device_id],
    "request_body": project_id,
    "responses": {
        200: openapi.Response(
            "application/json",
            examples={"application/json": "Subscription added"},
        ),
        400: openapi.Response(
            "application/json",
            examples={
                "application/json": [
                    message.invalid_parameters,
                    message.invalid_headers,
                ]
            },
        ),
        403: forbidden_403,
        404: not_found_404,
    },
    "tags": ["Projects"],
}


as_project_follow_delete = {
    # /api/v1/image swagger_auto_schema
    "methods": ["DELETE"],
    "manual_parameters": [header_device_authorization, header_device_id],
    "request_body": project_id,
    "responses": {
        200: openapi.Response(
            "application/json",
            examples={"application/json": "Subscription removed"},
        ),
        400: openapi.Response(
            "application/json",
            examples={
                "application/json": [
                    message.invalid_parameters,
                    message.invalid_headers,
                ]
            },
        ),
        403: forbidden_403,
        404: not_found_404,
    },
    "tags": ["Projects"],
}


as_projects_followed_articles = {
    # /api/v1/project/followed/articles swagger_auto_schema
    "methods": ["get"],
    "manual_parameters": [
        header_device_authorization,
        header_device_id,
        query_project_ids,
        query_article_max_age,
    ],
    "responses": {
        200: openapi.Response(
            "application/json",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "project_id": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "meta_id": meta_id,
                                "modification_date": openapi.Schema(
                                    type=openapi.TYPE_STRING
                                ),
                            },
                        ),
                    )
                },
            ),
            examples={
                "application/json": {
                    "155581": [
                        {
                            "meta_id": {"type": "article", "id": 163},
                            "modification_date": "2023-08-21T11:07:00+02:00",
                        },
                        {
                            "meta_id": {"type": "warning", "id": 67},
                            "modification_date": "2023-08-23T16:28:00+02:00",
                        },
                    ],
                    "155584": [
                        {
                            "meta_id": {"type": "warning", "id": 356},
                            "modification_date": "2023-10-24T15:16:00+02:00",
                        }
                    ],
                }
            },
        ),
        400: openapi.Response(
            "application/json",
            examples={
                "application/json": [
                    message.invalid_parameters,
                    message.invalid_headers,
                ]
            },
        ),
        403: forbidden_403,
        404: not_found_404,
    },
    "tags": ["Projects"],
}
