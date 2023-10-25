""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""

from drf_yasg import openapi

from construction_work.generic_functions.static_data import StaticData

as_image = {
    # /api/v1/image swagger_auto_schema
    "methods": ["get"],
    "manual_parameters": [
        openapi.Parameter(
            "id",
            openapi.IN_QUERY,
            "Image Identifier",
            type=openapi.TYPE_STRING,
            format="<identifier>",
            required=True,
        )
    ],
    "responses": {
        200: openapi.Response("Binary data"),
        404: openapi.Response("Error: file not found"),
        422: openapi.Response("Error: Unprocessable Entity"),
    },
    "tags": ["Generic"],
}
