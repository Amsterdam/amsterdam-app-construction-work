"""Swagger abstract objects to be used in Swagger definitions"""

from drf_yasg import openapi

images = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "type": openapi.Schema(type=openapi.TYPE_STRING, description="image type"),
            "sources": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "<int>px": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "url": openapi.Schema(
                                type=openapi.TYPE_STRING, description="url"
                            ),
                            "size": openapi.Schema(
                                type=openapi.TYPE_STRING, description="size"
                            ),
                            "filename": openapi.Schema(
                                type=openapi.TYPE_STRING, description="filename"
                            ),
                            "image_id": openapi.Schema(
                                type=openapi.TYPE_STRING, description="image id"
                            ),
                            "description": openapi.Schema(
                                type=openapi.TYPE_STRING, description="description"
                            ),
                        },
                    )
                },
            ),
        },
    ),
)
