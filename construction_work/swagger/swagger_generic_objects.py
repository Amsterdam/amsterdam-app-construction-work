"""Swagger abstract objects to be used in Swagger definitions"""

from copy import copy

from drf_yasg import openapi

from construction_work.api_messages import Messages
from construction_work.generic_functions.static_data import ARTICLE_MAX_AGE_PARAM

messages = Messages()

#
# Headers
#

header_device_id = openapi.Parameter(
    "deviceId",
    openapi.IN_HEADER,
    description="Device identifier",
    type=openapi.TYPE_STRING,
    required=True,
)

header_device_authorization = openapi.Parameter(
    "DeviceAuthorization",
    openapi.IN_HEADER,
    description="AES encrypted UUID4",
    type=openapi.TYPE_STRING,
    required=True,
)

header_device_authorization_not_required = copy(header_device_authorization)
header_device_authorization_not_required.required = False

header_ingest_authorization = openapi.Parameter(
    "IngestAuthorization",
    openapi.IN_HEADER,
    description="AES encrypted UUID4",
    type=openapi.TYPE_STRING,
    required=True,
)

header_user_authorization = openapi.Parameter(
    "UserAuthorization",
    openapi.IN_HEADER,
    description="AES encrypted project manager key (UUID)",
    type=openapi.TYPE_STRING,
    required=True,
)

header_jwt_authorization = openapi.Parameter(
    "Authorization",
    openapi.IN_HEADER,
    description="JWT token, retrievable via /get-token",
    type=openapi.TYPE_STRING,
    required=True,
)

header_jwt_authorization_not_required = copy(header_jwt_authorization)
header_jwt_authorization_not_required.required = False

#
# Query parameters
#

query_article_max_age = openapi.Parameter(
    ARTICLE_MAX_AGE_PARAM,
    openapi.IN_QUERY,
    description="Number of days (default: 3)",
    type=openapi.TYPE_INTEGER,
    format="int",
    required=False,
)

query_latitude = openapi.Parameter(
    "lat",
    openapi.IN_QUERY,
    description="Latitude",
    type=openapi.TYPE_STRING,
    format="float",
    required=False,
)

query_longitude = openapi.Parameter(
    "lon",
    openapi.IN_QUERY,
    description="Longitude",
    type=openapi.TYPE_STRING,
    format="float",
    required=False,
)

query_address = openapi.Parameter(
    "address",
    openapi.IN_QUERY,
    description="Address (street and number)",
    type=openapi.TYPE_STRING,
    format="string",
    required=False,
)

query_id = openapi.Parameter(
    "id",
    openapi.IN_QUERY,
    description="id",
    type=openapi.TYPE_INTEGER,
    format="int",
    required=True,
)

query_project_id = openapi.Parameter(
    "project_id",
    openapi.IN_QUERY,
    description="id",
    type=openapi.TYPE_INTEGER,
    format="int",
    required=True,
)

query_project_ids = openapi.Parameter(
    "project_ids",
    openapi.IN_QUERY,
    description="Limit articles to these comma seperated project ids",
    type=openapi.TYPE_STRING,
    required=False,
)


query_foreign_id = openapi.Parameter(
    "foreign_id",
    openapi.IN_QUERY,
    description="Project foreign id",
    type=openapi.TYPE_INTEGER,
    format="int",
    required=True,
)

query_warning_message_id = openapi.Parameter(
    "id",
    openapi.IN_QUERY,
    "Warning message identifier",
    type=openapi.TYPE_STRING,
    format="<identifier>",
    required=True,
)

query_text = openapi.Parameter(
    "text",
    openapi.IN_QUERY,
    description="search text",
    type=openapi.TYPE_STRING,
    format="<string>",
    required=True,
)

query_query_fields = openapi.Parameter(
    "query_fields",
    openapi.IN_QUERY,
    description="field to be queried",
    type=openapi.TYPE_STRING,
    format="<field,field,...>",
    required=True,
)

query_fields = openapi.Parameter(
    "fields",
    openapi.IN_QUERY,
    description="field to be returned",
    type=openapi.TYPE_STRING,
    format="<field,field,...>",
    required=True,
)

query_sort_by = openapi.Parameter(
    "sort_by",
    openapi.IN_QUERY,
    "Sort response (default: modification_date)",
    type=openapi.TYPE_STRING,
    format="<any key from model>",
    required=False,
)

query_sort_order = openapi.Parameter(
    "sort_order",
    openapi.IN_QUERY,
    "Sorting order (default: asc)",
    type=openapi.TYPE_STRING,
    format="<asc, desc>",
    required=False,
)

query_page_size = openapi.Parameter(
    "page_size",
    openapi.IN_QUERY,
    description="Number of results per page (default 10)",
    type=openapi.TYPE_INTEGER,
    format="int",
    required=False,
)

query_page = openapi.Parameter(
    "page",
    openapi.IN_QUERY,
    description="Page number",
    type=openapi.TYPE_INTEGER,
    format="int",
    required=False,
)

query_limit = openapi.Parameter(
    "limit",
    openapi.IN_QUERY,
    description="Limit returned items to this number",
    type=openapi.TYPE_INTEGER,
    format="<int>",
    required=False,
)


#
# Re-usable schema objects
#

project_id = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Project id")
    },
)

page = openapi.Schema(
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
)

link_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "href": openapi.Schema(
            type=openapi.TYPE_STRING,
        ),
    },
)

links = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "self": link_schema,
        "next": link_schema,
        "previous": link_schema,
    },
)

foreign_id = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(type=openapi.TYPE_STRING, description="foreign id"),
)

news_type = openapi.Schema(type=openapi.TYPE_STRING, description="<article|warning>")

meta_id = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "type": news_type,
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="id"),
    },
)

article_minimal = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "meta_id": meta_id,
        "modification_date": openapi.Schema(
            type=openapi.TYPE_STRING, description="datetime"
        ),
    },
)

articles_minimal = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=article_minimal,
)

article_full = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="internal id"),
        "meta_id": meta_id,
        "foreign_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="iprox id"),
        "active": openapi.Schema(
            type=openapi.TYPE_BOOLEAN, description="active or not"
        ),
        "last_seen": openapi.Schema(type=openapi.TYPE_STRING, description="datetime"),
        "title": openapi.Schema(type=openapi.TYPE_STRING, description="article title"),
        "intro": openapi.Schema(
            type=openapi.TYPE_STRING, description="html format intro"
        ),
        "body": openapi.Schema(
            type=openapi.TYPE_STRING, description="html format body"
        ),
        # "image": openapi.Schema(type=openapi.TYPE_INTEGER, description="iprox id"),
        "url": openapi.Schema(
            type=openapi.TYPE_STRING, description="absolute url path"
        ),
        "creation_date": openapi.Schema(
            type=openapi.TYPE_STRING, description="datetime"
        ),
        "modification_date": openapi.Schema(
            type=openapi.TYPE_STRING, description="datetime"
        ),
        "publication_date": openapi.Schema(
            type=openapi.TYPE_STRING, description="datetime"
        ),
        "expiration_date": openapi.Schema(
            type=openapi.TYPE_STRING, description="datetime"
        ),
        "projects": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            description="related to these project ids",
            items=openapi.Schema(type=openapi.TYPE_INTEGER, description="projects id"),
        ),
    },
)

articles_full = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=article_full,
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

coordinates = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "lat": openapi.Schema(type=openapi.TYPE_NUMBER, description="float"),
        "lon": openapi.Schema(type=openapi.TYPE_NUMBER, description="float"),
    },
)

section_part = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "title": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
            "body": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
        },
    ),
)

sections = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "what": section_part,
        "when": section_part,
        "work": section_part,
        "where": section_part,
        "contact": section_part,
    },
)

contacts = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="id"),
            "name": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
            "email": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
            "phone": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
            "position": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
        },
    ),
)

timeline = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "title": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
        "intro": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
        "items": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "date": openapi.Schema(
                        type=openapi.TYPE_STRING, description="text"
                    ),
                    "title": openapi.Schema(
                        type=openapi.TYPE_STRING, description="text"
                    ),
                    "body": openapi.Schema(
                        type=openapi.TYPE_STRING, description="text"
                    ),
                    "collapsed": openapi.Schema(
                        type=openapi.TYPE_BOOLEAN, description="bool"
                    ),
                    "items": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "date": openapi.Schema(
                                    type=openapi.TYPE_STRING, description="text"
                                ),
                                "title": openapi.Schema(
                                    type=openapi.TYPE_STRING, description="text"
                                ),
                                "body": openapi.Schema(
                                    type=openapi.TYPE_STRING, description="text"
                                ),
                            },
                        ),
                    ),
                },
            ),
        ),
    },
)

image = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="id"),
        "aspectRatio": openapi.Schema(
            type=openapi.TYPE_NUMBER, description="aspect ratio"
        ),
        "alternativeText": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
        "sources": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "url": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
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
)

images = openapi.Schema(type=openapi.TYPE_ARRAY, items=image)

warning_images = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "main": openapi.Schema(
                type=openapi.TYPE_BOOLEAN, description="primary image"
            ),
            "sources": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "uri": openapi.Schema(
                            type=openapi.TYPE_STRING, description="image uri"
                        ),
                        "width": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="image width"
                        ),
                        "height": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="image height"
                        ),
                    },
                ),
            ),
            "landscape": openapi.Schema(
                type=openapi.TYPE_BOOLEAN, description="landscape"
            ),
            "coordinates": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "lan": openapi.Schema(
                        type=openapi.TYPE_INTEGER, description="latitude"
                    ),
                    "lon": openapi.Schema(
                        type=openapi.TYPE_INTEGER, description="longitude"
                    ),
                },
            ),
            "description": openapi.Schema(
                type=openapi.TYPE_STRING, description="image description"
            ),
            "aspect_ratio": openapi.Schema(
                type=openapi.TYPE_INTEGER, description="image aspect ratio"
            ),
        },
    ),
)

project_details_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="int"),
        "meter": openapi.Schema(type=openapi.TYPE_INTEGER, description="int"),
        "strides": openapi.Schema(type=openapi.TYPE_INTEGER, description="int"),
        "followed": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="boolean"),
        "recent_articles": articles_full,
        "followers": openapi.Schema(type=openapi.TYPE_INTEGER, description="int"),
        "foreign_id": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="foreign id"
        ),
        "active": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="boolean"),
        "last_seen": openapi.Schema(type=openapi.TYPE_STRING, description="datetime"),
        "title": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
        "subtitle": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
        "coordinates": coordinates,
        "sections": sections,
        "contacts": contacts,
        "timeline": timeline,
        "image": image,
        "images": images,
        "url": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
        "creation_date": openapi.Schema(
            type=openapi.TYPE_STRING, description="datetime"
        ),
        "modification_date": openapi.Schema(
            type=openapi.TYPE_STRING, description="datetime"
        ),
        "publication_date": openapi.Schema(
            type=openapi.TYPE_STRING, description="datetime"
        ),
        "expiration_date": openapi.Schema(
            type=openapi.TYPE_STRING, description="datetime"
        ),
    },
)

project_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="int"),
        "title": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
        "subtitle": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
        "image": image,
        "followed": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="boolean"),
        "meter": openapi.Schema(type=openapi.TYPE_INTEGER, description="int"),
        "strides": openapi.Schema(type=openapi.TYPE_INTEGER, description="int"),
        "recent_articles": articles_minimal,
    },
)

warning_message = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="id"),
        "meta_id": meta_id,
        "images": warning_images,
        "title": openapi.Schema(type=openapi.TYPE_STRING, description="id"),
        "body": openapi.Schema(type=openapi.TYPE_STRING, description="body"),
        "modification_date": openapi.Schema(
            type=openapi.TYPE_STRING, description="datetime"
        ),
        "publication_date": openapi.Schema(
            type=openapi.TYPE_STRING, description="datetime"
        ),
        "author_email": openapi.Schema(
            type=openapi.TYPE_STRING, description="author email"
        ),
        "project": openapi.Schema(type=openapi.TYPE_INTEGER, description="project id"),
    },
)

warning_messages = openapi.Schema(type=openapi.TYPE_ARRAY, items=warning_message)


def get_paginated_schema(schema: openapi.Schema):
    """Get paginated schema"""
    return openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "result": schema,
            "page": page,
            "_links": links,
        },
    )


#
# Responses
#

forbidden_403 = openapi.Response(
    description="Forbidden",
)

not_found_404 = openapi.Response(
    description="Object not found",
    examples={"application/json": messages.no_record_found},
)
