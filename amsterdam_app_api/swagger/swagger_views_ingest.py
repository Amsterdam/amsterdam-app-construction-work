from drf_yasg import openapi


""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""


as_ingest_projects = {
    # /api/v1/projects/ingest swagger_auto_schema
    'methods': ['get'],
    'manual_parameters': [openapi.Parameter('project-type',
                                            openapi.IN_QUERY,
                                            'Ingest projects by type',
                                            type=openapi.TYPE_STRING,
                                            format='<brug, kade, stadsloket>',
                                            required=True)],
    'responses': {
        200: openapi.Response('application/json',
                              examples={
                                  'application/json': {
                                      'status': True,
                                      'result': {'new': 0, 'updated': 0, 'failed': 0}}}),
        422: openapi.Response('Error: Unprocessable Entity')
    },
    'tags': ['Ingestion']
}
