"""Swagger abstract objects to be used in Swagger definitions"""

from drf_yasg import openapi

from construction_work.generic_functions.static_data import ARTICLE_MAX_AGE_PARAM

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
    "DEVICEAUTHORIZATION",
    openapi.IN_HEADER,
    description="Device authorization",
    type=openapi.TYPE_STRING,
    required=True,
)

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

query_foreign_id = openapi.Parameter(
    "foreign_id",
    openapi.IN_QUERY,
    description="Project foreign id",
    type=openapi.TYPE_INTEGER,
    format="int",
    required=True,
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

#
# Re-usable schema objects
#

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

_links = openapi.Schema(
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

recent_articles = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "meta_id": openapi.Schema(type=openapi.TYPE_STRING, description="meta id"),
            "modification_date": openapi.Schema(type=openapi.TYPE_STRING, description="datetime"),
        },
    ),
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
                    "date": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
                    "title": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
                    "body": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
                    "collapsed": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="bool"),
                    "items": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "date": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
                                "title": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
                                "body": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
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
        "aspectRatio": openapi.Schema(type=openapi.TYPE_NUMBER, description="aspect ratio"),
        "alternativeText": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
        "sources": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "url": openapi.Schema(type=openapi.TYPE_STRING, description="text"),
                    "width": openapi.Schema(type=openapi.TYPE_INTEGER, description="width"),
                    "height": openapi.Schema(type=openapi.TYPE_INTEGER, description="height"),
                },
            ),
        ),
    },
)

images = openapi.Schema(type=openapi.TYPE_ARRAY, items=image)
