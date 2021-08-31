from drf_yasg import openapi
from amsterdam_app_api.serializers import ProjectsSerializer, ProjectDetailsSerializer

""" Swagger definitions used in the views.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views.py prepended with 'as_' (auto_schema)
"""


as_projects = {
    # /api/v1/projects swagger_auto_schema
    'methods': ['GET'],
    'manual_parameters': [openapi.Parameter('project-type', 
                                            openapi.IN_QUERY, 
                                            'Query by projects type',
                                            type=openapi.TYPE_STRING,
                                            format='<brug, kade>',
                                            required=False),
                          openapi.Parameter('district_id',
                                            openapi.IN_QUERY,
                                            'Query by district id',
                                            type=openapi.TYPE_INTEGER,
                                            format='<integer>',
                                            required=False),
                          openapi.Parameter('sort-by',
                                            openapi.IN_QUERY,
                                            'Sort response',
                                            type=openapi.TYPE_STRING,
                                            format='<any key from model>',
                                            required=False),
                          openapi.Parameter('sort-order',
                                            openapi.IN_QUERY,
                                            'Sorting order (default: asc)',
                                            type=openapi.TYPE_STRING,
                                            format='<asc, desc>',
                                            required=False)],
    'responses': {
        200: openapi.Response('application/json',
                              ProjectsSerializer,
                              examples={'application/json': {'status': True, 'result': []}}),
        405: openapi.Response('Error: Method not allowed'),
        422: openapi.Response('Error: Unprocessable Entity')
    },
    'tags': ['Projects']
}


as_project_details = {
    # /api/v1/project/details swagger_auto_schema
    'methods': ['get'],
    'manual_parameters': [openapi.Parameter('id', 
                                            openapi.IN_QUERY, 
                                            'Project identifier',
                                            type=openapi.TYPE_STRING,
                                            format='<identifier>',
                                            required=True)],
    'responses': {
        200: openapi.Response('application/json',
                              ProjectDetailsSerializer,
                              examples={'application/json': {'status': True, 'result': {}}}),
        404: openapi.Response('Error: No record found'),
        405: openapi.Response('Error: Method not allowed'),
        422: openapi.Response('Error: Unprocessable Entity')},
    'tags': ['Project details']
}


as_ingest_projects = {
    # /api/v1/projects/ingest swagger_auto_schema
    'methods': ['get'],
    'manual_parameters': [openapi.Parameter('project-type',
                                            openapi.IN_QUERY,
                                            'Ingest projects by type',
                                            type=openapi.TYPE_STRING,
                                            format='<brug, kade>',
                                            required=True)],
    'responses': {
        200: openapi.Response('application/json',
                              examples={
                                  'application/json': {
                                      'status': True,
                                      'result': {'new': 0, 'updated': 0, 'unmodified': 0, 'failed': 0}}}),
        422: openapi.Response('Error: Unprocessable Entity')
    },
    'tags': ['Ingestion']
}


as_image = {
    # /api/v1/image swagger_auto_schema
    'methods': ['get'],
    'manual_parameters': [openapi.Parameter('id',
                                            openapi.IN_QUERY,
                                            'Image Identifier',
                                            type=openapi.TYPE_STRING,
                                            format='<identifier>',
                                            required=True)],
    'responses': {
        200: openapi.Response('Binary data'),
        404: openapi.Response('Error: file not found'),
        422: openapi.Response('Error: Unprocessable Entity')
    },
    'tags': ['Image']
}
