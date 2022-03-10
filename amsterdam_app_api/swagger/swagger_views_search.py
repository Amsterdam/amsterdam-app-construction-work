from drf_yasg import openapi
from amsterdam_app_api.api_messages import Messages

messages = Messages()

""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""

as_search = {
    # /api/v1/search swagger_auto_schema
    'methods': ['get'],
    'manual_parameters': [openapi.Parameter('model',
                                            openapi.IN_QUERY,
                                            'model name',
                                            type=openapi.TYPE_STRING,
                                            format='<string (default:ProjectDetails)>',
                                            required=False),
                          openapi.Parameter('text',
                                            openapi.IN_QUERY,
                                            'text to search for',
                                            type=openapi.TYPE_STRING,
                                            format='<string>',
                                            required=True),
                          openapi.Parameter('query_fields',
                                            openapi.IN_QUERY,
                                            'the field(s) on which to operate your query',
                                            type=openapi.TYPE_STRING,
                                            format='<string (default:title,subtitle)>',
                                            required=False),
                          openapi.Parameter('fields',
                                            openapi.IN_QUERY,
                                            'the field(s) which are returned from the model',
                                            type=openapi.TYPE_STRING,
                                            format='<string (default:title,subtitle)>',
                                            required=False),
                          openapi.Parameter('min_similarity',
                                            openapi.IN_QUERY,
                                            'Omit results with a similarity less then (int)',
                                            type=openapi.TYPE_NUMBER,
                                            format='<int (default:0.07)>',
                                            required=False),
                          openapi.Parameter('limit',
                                            openapi.IN_QUERY,
                                            'Limit the result to <limit> items',
                                            type=openapi.TYPE_INTEGER,
                                            format='<int (default:20)>',
                                            required=False)
                          ],
    'responses': {
        200: openapi.Response('json data'),
        404: openapi.Response('{a}|{b}'.format(a=messages.no_such_database_model, b=messages.no_such_field_in_model))
    },
    'tags': ['Search']
}