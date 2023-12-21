""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""

from drf_yasg import openapi

from construction_work.api_messages import Messages
from construction_work.swagger.swagger_generic_objects import (
    forbidden_403,
    header_device_authorization,
    not_found_404,
    query_id,
)

messages = Messages()

as_image = {
    # /api/v1/image swagger_auto_schema
    "methods": ["get"],
    "manual_parameters": [header_device_authorization, query_id],
    "responses": {
        200: openapi.Response("Binary data"),
        400: openapi.Response(
            "application/json",
            examples={"application/json": messages.invalid_query},
        ),
        403: forbidden_403,
        404: not_found_404,
    },
    "tags": ["Generic"],
}
