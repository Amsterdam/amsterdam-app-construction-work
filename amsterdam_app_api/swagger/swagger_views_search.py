from drf_yasg import openapi
from amsterdam_app_api.api_messages import Messages

messages = Messages()

""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""

as_search = {
    # /api/v1/XXX/search swagger_auto_schema
    'methods': ['get'],
    'manual_parameters': [openapi.Parameter('text',
                                            openapi.IN_QUERY,
                                            'text to search for',
                                            type=openapi.TYPE_STRING,
                                            format='<string>',
                                            required=True),
                          openapi.Parameter('query_fields',
                                            openapi.IN_QUERY,
                                            'comma separated field(s) on which to operate your query',
                                            type=openapi.TYPE_STRING,
                                            format='<string,string,...>',
                                            required=True),
                          openapi.Parameter('threshold',
                                            openapi.IN_QUERY,
                                            'Fine-tune the results',
                                            type=openapi.TYPE_NUMBER,
                                            format='<float>',
                                            required=True),
                          openapi.Parameter('fields',
                                            openapi.IN_QUERY,
                                            'comma separated field(s) which are returned from the model',
                                            type=openapi.TYPE_STRING,
                                            format='<string,string,...>',
                                            required=False),
                          openapi.Parameter('page_size',
                                            openapi.IN_QUERY,
                                            'Limit items per page for paginated result',
                                            type=openapi.TYPE_INTEGER,
                                            format='<int (default:10)>',
                                            required=False),
                          openapi.Parameter('page',
                                            openapi.IN_QUERY,
                                            'Page from paginated result',
                                            type=openapi.TYPE_INTEGER,
                                            format='<int (default:1)>',
                                            required=False)
                          ],
    'responses': {
        200: openapi.Response('json data'),
        422: openapi.Response('{a}|{b}'.format(a=messages.invalid_query, b=messages.no_such_field_in_model))
    },
    'tags': ['Search']
}