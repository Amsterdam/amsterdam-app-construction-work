from drf_yasg import openapi
from amsterdam_app_api.serializers import NewsSerializer


""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""


as_news = {
    # /api/v1/project/news swagger_auto_schema
    'methods': ['GET'],
    'manual_parameters': [openapi.Parameter('project-identifier',
                                            openapi.IN_QUERY,
                                            'Query by news project-identifier',
                                            type=openapi.TYPE_STRING,
                                            format='<brug, kade>',
                                            required=False),
                          openapi.Parameter('sort-by',
                                            openapi.IN_QUERY,
                                            'Sort response (default=publication_date)',
                                            type=openapi.TYPE_STRING,
                                            format='<any key from model>',
                                            required=False),
                          openapi.Parameter('sort-order',
                                            openapi.IN_QUERY,
                                            'Sorting order (default: desc)',
                                            type=openapi.TYPE_STRING,
                                            format='<asc, desc>',
                                            required=False)],
    'responses': {
        200: openapi.Response('application/json',
                              NewsSerializer,
                              examples={'application/json': {'status': True, 'result': []}}),
        405: openapi.Response('Error: Method not allowed'),
        422: openapi.Response('Error: Unprocessable Entity')
    },
    'tags': ['Projects']
}