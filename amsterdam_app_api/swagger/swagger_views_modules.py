from drf_yasg import openapi
from amsterdam_app_api.api_messages import Messages

message = Messages()

""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""

version = openapi.Schema(type=openapi.TYPE_STRING, description='Version number')
slug = openapi.Schema(type=openapi.TYPE_STRING, description='Unique human readable identifier (Slug)')
status = openapi.Schema(type=openapi.TYPE_INTEGER, description='The current state of this module\n\n0: inactive\n1: active')
title = openapi.Schema(type=openapi.TYPE_STRING, description='Descriptive title')
icon = openapi.Schema(type=openapi.TYPE_STRING, description='Icon name')
description = openapi.Schema(type=openapi.TYPE_STRING, description='Description')

modules_for_app = {
    "description": description,
    "slug": slug,
    "title": title,
    "icon": icon,
    "status": status,
    "version": version
}

modules_by_app = {
    "appVersion": version,
    "moduleSlug": slug,
    "moduleVersion": version,
    "status": status
}

modules = {
    "slug": slug,
    "title": title,
    "icon": icon,
    "version": version,
    "description": description
}

module_order = {
    "appVersion": version,
    "order": openapi.Schema(type=openapi.TYPE_ARRAY,
                            items=slug)
}


as_module_app_versions ={
    'methods': ['get'],
    'responses': {
        200: openapi.Response(
            'application/json',
            schema=openapi.Schema(type=openapi.TYPE_OBJECT,
                                  properties={
                                      'status': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='result status'),
                                      'result': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                               items=openapi.Schema(type=openapi.TYPE_STRING, description='app versions'))
                                  }))
    },
    'tags': ['App Versions']
}


as_module_get = {
    'methods': ['get'],
    'manual_parameters': [
        openapi.Parameter('slug',
                          openapi.IN_QUERY,
                          required=True,
                          description="Slug for requesting modules",
                          type=openapi.TYPE_STRING),
        openapi.Parameter('version',
                          openapi.IN_QUERY,
                          required=True,
                          description="Version for requesting modules",
                          type=openapi.TYPE_STRING)
    ],
    'responses': {
        200: openapi.Response(
            'application/json',
            schema=openapi.Schema(type=openapi.TYPE_OBJECT,
                                  properties={
                                      'status': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='result status'),
                                      'result': openapi.Schema(type=openapi.TYPE_OBJECT, properties=modules)
                                  }))
    },
    'tags': ['Module']
}


as_modules_get = {
    'methods': ['get'],
    'manual_parameters': [openapi.Parameter('slug',
                                            openapi.IN_QUERY,
                                            description="Slug for requesting modules",
                                            type=openapi.TYPE_STRING)],
    'responses': {
        200: openapi.Response(
            'application/json',
            schema=openapi.Schema(type=openapi.TYPE_OBJECT,
                                  properties={
                                      'status': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='result status'),
                                      'result': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                               items=openapi.Schema(type=openapi.TYPE_OBJECT, properties=modules))
                                  }))
    },
    'tags': ['Modules']
}


as_modules_post = {
    'methods': ['POST'],
    'manual_parameters': [openapi.Parameter('Authorization',
                                            openapi.IN_HEADER,
                                            description="Authorization token",
                                            type=openapi.TYPE_STRING,
                                            required=True)],
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["slug", "title", "icon", "version", "description"],
        properties=modules,
    ),
    'responses': {
        200: openapi.Response('application/json',
                              examples={
                                  'application/json': {
                                      'status': True,
                                      'result': 'string'
                                  }
                              })
    },
    'tags': ['Modules']
}


as_modules_patch = {
    'methods': ['PATCH'],
    'manual_parameters': [openapi.Parameter('Authorization',
                                            openapi.IN_HEADER,
                                            description="Authorization token",
                                            type=openapi.TYPE_STRING,
                                            required=True)],
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["slug", "version"],
        properties=modules,
    ),
    'responses': {
        200: openapi.Response('application/json',
                              examples={
                                  'application/json': {
                                      'status': True,
                                      'result': 'string'
                                  }
                              })
    },
    'tags': ['Modules']
}


as_modules_delete = {
    'methods': ['DELETE'],
    'manual_parameters': [openapi.Parameter('Authorization',
                                            openapi.IN_HEADER,
                                            description="Authorization token",
                                            type=openapi.TYPE_STRING,
                                            required=True)],
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['version', 'slug'],
        properties={
            'version': version,
            'slug': slug
        }
    ),
    'responses': {
        200: openapi.Response('application/json',
                              examples={
                                  'application/json': {
                                      'status': True,
                                      'result': 'string'
                                  }
                              }),
        500: openapi.Response('application/json',
                              examples={
                                  'application/json': {
                                      'status': True,
                                      'result': 'error string'
                                  }
                              }),
    },
    'tags': ['Modules']
}


as_modules_by_app_get = {
    'methods': ['get'],
    'manual_parameters': [openapi.Parameter('appVersion',
                                            openapi.IN_QUERY,
                                            description="appVersion for requesting modules",
                                            type=openapi.TYPE_STRING)],
    'responses': {
        200: openapi.Response(
            'application/json',
            schema=openapi.Schema(type=openapi.TYPE_OBJECT,
                                  properties={
                                      'status': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='result status'),
                                      'result': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                               items=openapi.Schema(type=openapi.TYPE_OBJECT, properties=modules_by_app))
                                  }))
    },
    'tags': ['Modules by App']
}


as_modules_by_app_post = {
    'methods': ['POST'],
    'manual_parameters': [openapi.Parameter('Authorization',
                                            openapi.IN_HEADER,
                                            description="Authorization token",
                                            type=openapi.TYPE_STRING,
                                            required=True)],
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["appVersion", "moduleSlug", "moduleVersion", "status"],
        properties=modules_by_app,
    ),
    'responses': {
        200: openapi.Response('application/json',
                              examples={
                                  'application/json': {
                                      'status': True,
                                      'result': 'string'
                                  }
                              })
    },
    'tags': ['Modules by App']
}


as_modules_by_app_patch = {
    'methods': ['PATCH'],
    'manual_parameters': [openapi.Parameter('Authorization',
                                            openapi.IN_HEADER,
                                            description="Authorization token",
                                            type=openapi.TYPE_STRING,
                                            required=True)],
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["appVersion", "moduleSlug"],
        properties=modules_by_app,
    ),
    'responses': {
        200: openapi.Response('application/json',
                              examples={
                                  'application/json': {
                                      'status': True,
                                      'result': 'string'
                                  }
                              })
    },
    'tags': ['Modules by App']
}


as_modules_by_app_delete = {
    'methods': ['DELETE'],
    'manual_parameters': [openapi.Parameter('Authorization',
                                            openapi.IN_HEADER,
                                            description="Authorization token",
                                            type=openapi.TYPE_STRING,
                                            required=True)],
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["appVersion", "moduleSlug"],
        properties={
            'version': version,
            'slug': slug
        }
    ),
    'responses': {
        200: openapi.Response('application/json',
                              examples={
                                  'application/json': {
                                      'status': True,
                                      'result': 'string'
                                  }
                              }),
        500: openapi.Response('application/json',
                              examples={
                                  'application/json': {
                                      'status': True,
                                      'result': 'error string'
                                  }
                              }),
    },
    'tags': ['Modules by App']
}


as_module_order_get = {
    'methods': ['get'],
    'manual_parameters': [openapi.Parameter('appVersion',
                                            openapi.IN_QUERY,
                                            description="appVersion for requesting modules",
                                            type=openapi.TYPE_STRING)],
    'responses': {
        200: openapi.Response(
            'application/json',
            schema=openapi.Schema(type=openapi.TYPE_OBJECT,
                                  properties={
                                      'status': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='result status'),
                                      'result': module_order
                                  }))
    },
    'tags': ['Module Order']
}


as_module_order_post = {
    'methods': ['POST'],
    'manual_parameters': [openapi.Parameter('Authorization',
                                            openapi.IN_HEADER,
                                            description="Authorization token",
                                            type=openapi.TYPE_STRING,
                                            required=True)],
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["appVersion", "order"],
        properties=module_order,
    ),
    'responses': {
        200: openapi.Response('application/json',
                              examples={
                                  'application/json': {
                                      'status': True,
                                      'result': 'string'
                                  }
                              })
    },
    'tags': ['Module Order']
}


as_module_order_patch = {
    'methods': ['PATCH'],
    'manual_parameters': [openapi.Parameter('Authorization',
                                            openapi.IN_HEADER,
                                            description="Authorization token",
                                            type=openapi.TYPE_STRING,
                                            required=True)],
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["appVersion", "order"],
        properties=module_order,
    ),
    'responses': {
        200: openapi.Response('application/json',
                              examples={
                                  'application/json': {
                                      'status': True,
                                      'result': 'string'
                                  }
                              })
    },
    'tags': ['Module Order']
}


as_module_order_delete = {
    'methods': ['DELETE'],
    'manual_parameters': [openapi.Parameter('Authorization',
                                            openapi.IN_HEADER,
                                            description="Authorization token",
                                            type=openapi.TYPE_STRING,
                                            required=True)],
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["appVersion"],
        properties={'appVersion': version}
    ),
    'responses': {
        200: openapi.Response('application/json',
                              examples={
                                  'application/json': {
                                      'status': True,
                                      'result': 'string'
                                  }
                              }),
        500: openapi.Response('application/json',
                              examples={
                                  'application/json': {
                                      'status': True,
                                      'result': 'error string'
                                  }
                              }),
    },
    'tags': ['Module Order']
}


as_modules_for_app_get = {
    'methods': ['get'],
    'manual_parameters': [openapi.Parameter('appVersion',
                                            openapi.IN_QUERY,
                                            description="appVersion for requesting modules",
                                            type=openapi.TYPE_STRING)],
    'responses': {
        200: openapi.Response(
            'application/json',
            schema=openapi.Schema(type=openapi.TYPE_OBJECT,
                                  properties={
                                      'status': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='result status'),
                                      'result': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                               items=openapi.Schema(type=openapi.TYPE_OBJECT, properties=modules_for_app))
                                  }))

    },
    'tags': ['Modules for App']
}
