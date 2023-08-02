""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""

from drf_yasg import openapi

as_distance = {
    # /api/v1/projects/distance swagger_auto_schema
    "methods": ["get"],
    "manual_parameters": [
        openapi.Parameter(
            "lat",
            openapi.IN_QUERY,
            "latitude",
            type=openapi.TYPE_STRING,
            format="float",
            required=False,
        ),
        openapi.Parameter(
            "lon",
            openapi.IN_QUERY,
            "longitude",
            type=openapi.TYPE_STRING,
            format="float",
            required=False,
        ),
        openapi.Parameter(
            "radius",
            openapi.IN_QUERY,
            "radius (unit is meter)",
            type=openapi.TYPE_STRING,
            format="float",
            required=False,
        ),
        openapi.Parameter(
            "address",
            openapi.IN_QUERY,
            "address (street and number)",
            type=openapi.TYPE_STRING,
            format="string",
            required=False,
        ),
        openapi.Parameter(
            "fields",
            openapi.IN_QUERY,
            "Return given fields (model: projects)",
            type=openapi.TYPE_STRING,
            format="<field1,field2>",
            required=False,
        ),
    ],
    "responses": {
        200: openapi.Response(
            "application/json",
            examples={
                "application/json": {
                    "project_id": "0123456789",
                    "name": "project title",
                    "distance_meter": 1000,
                    "distance_strides": 1351,
                }
            },
        ),
        422: openapi.Response("Error: Unprocessable Entity"),
    },
    "tags": ["Projects"],
}
