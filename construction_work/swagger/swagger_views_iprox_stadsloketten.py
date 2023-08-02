""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""

from drf_yasg import openapi

as_city_contact = {
    "methods": ["get"],
    "responses": {
        200: openapi.Response(
            "application/json",
            openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "title": openapi.Schema(
                            type=openapi.TYPE_STRING, description="title"
                        ),
                        "html": openapi.Schema(
                            type=openapi.TYPE_STRING, description="html formatted text"
                        ),
                        "text": openapi.Schema(
                            type=openapi.TYPE_STRING, description="plain text"
                        ),
                    },
                ),
            ),
            examples={"application/json": {"status": True, "result": {}}},
        )
    },
    "tags": ["City"],
}


opening_hours_regular = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "city_office_id": openapi.Schema(
                type=openapi.TYPE_STRING, description="city office id (foreign key)"
            ),
            "day_of_week": openapi.Schema(
                type=openapi.TYPE_STRING, description="day of the week (sun = 0)"
            ),
            "opens_hours": openapi.Schema(
                type=openapi.TYPE_STRING, description="hours (0-23)"
            ),
            "opens_minutes": openapi.Schema(
                type=openapi.TYPE_STRING, description="minutes (0-59)"
            ),
            "closes_hours": openapi.Schema(
                type=openapi.TYPE_STRING, description="hours (0-23)"
            ),
            "closes_minutes": openapi.Schema(
                type=openapi.TYPE_STRING, description="minutes (0-59)"
            ),
        },
    ),
)

opening_hours_exceptions = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "city_office_id": openapi.Schema(
                type=openapi.TYPE_STRING, description="city office id (foreign key)"
            ),
            "date": openapi.Schema(
                type=openapi.TYPE_STRING, description="date field (2022-12-31)"
            ),
            "opens_hours": openapi.Schema(
                type=openapi.TYPE_STRING, description="hours (0-23)"
            ),
            "opens_minutes": openapi.Schema(
                type=openapi.TYPE_STRING, description="minutes (0-59)"
            ),
            "closes_hours": openapi.Schema(
                type=openapi.TYPE_STRING, description="hours (0-23)"
            ),
            "closes_minutes": openapi.Schema(
                type=openapi.TYPE_STRING, description="minutes (0-59)"
            ),
        },
    ),
)

as_city_offices = {
    "methods": ["get"],
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
                        "image": openapi.Schema(
                            type=openapi.TYPE_OBJECT, description="images"
                        ),
                        "address": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description="address",
                            properties={
                                "streetName": openapi.Schema(
                                    type=openapi.TYPE_STRING, description="street name"
                                ),
                                "streetNumber": openapi.Schema(
                                    type=openapi.TYPE_STRING, description="house number"
                                ),
                                "postalCode": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description="postal code (1234ab)",
                                ),
                                "city": openapi.Schema(
                                    type=openapi.TYPE_STRING, description="city"
                                ),
                            },
                        ),
                        "addressContent": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description="address info",
                            properties={
                                "html": openapi.Schema(
                                    type=openapi.TYPE_STRING, description="html"
                                ),
                                "title": openapi.Schema(
                                    type=openapi.TYPE_STRING, description="title"
                                ),
                            },
                        ),
                        "coordinates": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description="address",
                            properties={
                                "lat": openapi.Schema(
                                    type=openapi.TYPE_INTEGER, description="latitude"
                                ),
                                "lon": openapi.Schema(
                                    type=openapi.TYPE_INTEGER, description="longitude"
                                ),
                            },
                        ),
                        "directionsUrl": openapi.Schema(
                            type=openapi.TYPE_STRING, description="url"
                        ),
                        "appointment": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description="appointment details",
                            properties={
                                "url": openapi.Schema(
                                    type=openapi.TYPE_STRING, description="url"
                                ),
                                "text": openapi.Schema(
                                    type=openapi.TYPE_STRING, description="text"
                                ),
                            },
                        ),
                        "visitingHoursContent": openapi.Schema(
                            type=openapi.TYPE_STRING, description="html"
                        ),
                        "visitingHours": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "regular": opening_hours_regular,
                                    "exceptions": opening_hours_exceptions,
                                },
                            ),
                        ),
                    },
                ),
            ),
            examples={"application/json": {"status": True, "result": {}}},
        )
    },
    "tags": ["City"],
}


as_city_office = {
    "methods": ["get"],
    "manual_parameters": [
        openapi.Parameter(
            "id",
            openapi.IN_QUERY,
            "CityOffice identifier",
            type=openapi.TYPE_STRING,
            format="<identifier>",
            required=True,
        )
    ],
    "responses": {
        200: openapi.Response(
            "application/json",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "identifier": openapi.Schema(
                        type=openapi.TYPE_STRING, description="identifier"
                    ),
                    "location": openapi.Schema(
                        type=openapi.TYPE_STRING, description="CityOffice"
                    ),
                    "contact": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "Bellen": openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "txt": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="plain text",
                                    ),
                                    "html": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="html formatted text",
                                    ),
                                },
                            ),
                            "Mailen": openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "txt": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="plain text",
                                    ),
                                    "html": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="html formatted text",
                                    ),
                                },
                            ),
                            "Openingstijden": openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "txt": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="plain text",
                                    ),
                                    "html": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="html formatted text",
                                    ),
                                },
                            ),
                        },
                    ),
                    "images": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "type": openapi.Schema(
                                type=openapi.TYPE_STRING, description="image type"
                            ),
                            "sources": openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "orig": openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            "url": openapi.Schema(
                                                type=openapi.TYPE_STRING,
                                                description="original url",
                                            ),
                                            "filename": openapi.Schema(
                                                type=openapi.TYPE_STRING,
                                                description="filename",
                                            ),
                                            "image_id": openapi.Schema(
                                                type=openapi.TYPE_STRING,
                                                description="identifier",
                                            ),
                                            "description": openapi.Schema(
                                                type=openapi.TYPE_STRING,
                                                description="description",
                                            ),
                                        },
                                    ),
                                    "XXXpx": openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            "url": openapi.Schema(
                                                type=openapi.TYPE_STRING,
                                                description="original url",
                                            ),
                                            "filename": openapi.Schema(
                                                type=openapi.TYPE_STRING,
                                                description="filename",
                                            ),
                                            "image_id": openapi.Schema(
                                                type=openapi.TYPE_STRING,
                                                description="identifier",
                                            ),
                                            "description": openapi.Schema(
                                                type=openapi.TYPE_STRING,
                                                description="description",
                                            ),
                                        },
                                    ),
                                },
                            ),
                        },
                    ),
                    "info": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "txt": openapi.Schema(
                                type=openapi.TYPE_STRING, description="plain text"
                            ),
                            "html": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="html formatted text",
                            ),
                        },
                    ),
                    "address": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "txt": openapi.Schema(
                                type=openapi.TYPE_STRING, description="plain text"
                            ),
                            "html": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="html formatted text",
                            ),
                        },
                    ),
                    "last_seen": openapi.Schema(
                        type=openapi.TYPE_STRING, description="date"
                    ),
                    "active": openapi.Schema(
                        type=openapi.TYPE_BOOLEAN, description="active record"
                    ),
                },
            ),
            examples={"application/json": {"status": True, "result": {}}},
        ),
        404: openapi.Response("Error: No record found"),
        422: openapi.Response("Error: Unprocessable Entity"),
    },
    "tags": ["City"],
}
