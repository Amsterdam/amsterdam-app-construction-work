from drf_yasg import openapi
from amsterdam_app_api.serializers import ProjectsSerializer, ProjectDetailsSerializer
from amsterdam_app_api.api_messages import Messages

message = Messages()

""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""

images = openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
    'type': openapi.Schema(type=openapi.TYPE_STRING, description='image type'),
    'sources': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        '<int>px': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'url': openapi.Schema(type=openapi.TYPE_STRING, description='url'),
            'size': openapi.Schema(type=openapi.TYPE_STRING, description='size'),
            'filename': openapi.Schema(type=openapi.TYPE_STRING, description='filename'),
            'image_id': openapi.Schema(type=openapi.TYPE_STRING, description='image id'),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description='description'),
        })
    })
}))

body_element = openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
    'html': openapi.Schema(type=openapi.TYPE_STRING, description='html'),
    'text': openapi.Schema(type=openapi.TYPE_STRING, description='text'),
    'title': openapi.Schema(type=openapi.TYPE_STRING, description='title')
}))

news = openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
    'url': openapi.Schema(type=openapi.TYPE_STRING, description='url'),
    'identifier': openapi.Schema(type=openapi.TYPE_STRING, description='identifier'),
    'project_identifier': openapi.Schema(type=openapi.TYPE_STRING, description='project identifier')
}))

timeline = openapi.Schema(type=openapi.TYPE_OBJECT, properties={
    'title': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        'html': openapi.Schema(type=openapi.TYPE_STRING, description='html'),
        'text': openapi.Schema(type=openapi.TYPE_STRING, description='text')
    }),
    'intro': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        'html': openapi.Schema(type=openapi.TYPE_STRING, description='html'),
        'text': openapi.Schema(type=openapi.TYPE_STRING, description='text')
    }),
    'items': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        'title': openapi.Schema(type=openapi.TYPE_STRING, description='text'),
        'collapsed': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='collapsed'),
        'progress': openapi.Schema(type=openapi.TYPE_STRING, description='current progress'),
        'content': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, description='text'),
            'body': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'html': openapi.Schema(type=openapi.TYPE_STRING, description='html'),
                'text': openapi.Schema(type=openapi.TYPE_STRING, description='text')
            })
        }))
    }))
})


as_projects = {
    # /api/v1/projects swagger_auto_schema
    'methods': ['GET'],
    'manual_parameters': [openapi.Parameter('deviceId',
                                            openapi.IN_HEADER,
                                            description="device identifier",
                                            type=openapi.TYPE_STRING,
                                            required=True),
                          openapi.Parameter('project-type',
                                            openapi.IN_QUERY,
                                            'Query by projects type',
                                            type=openapi.TYPE_STRING,
                                            format='<brug, kade, bouw-en-verkeer>',
                                            required=False),
                          openapi.Parameter('district-id',
                                            openapi.IN_QUERY,
                                            'Query by district id',
                                            type=openapi.TYPE_INTEGER,
                                            format='<integer>',
                                            required=False),
                          openapi.Parameter('articles_max_age',
                                            openapi.IN_QUERY,
                                            'Number of days (default: 3)',
                                            type=openapi.TYPE_INTEGER,
                                            format='<int>',
                                            required=False),
                          openapi.Parameter('fields',
                                            openapi.IN_QUERY,
                                            'Return given fields',
                                            type=openapi.TYPE_STRING,
                                            format='<any key from model + followed (dynamic)>',
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
                                            required=False),
                          openapi.Parameter('lat',
                                            openapi.IN_QUERY,
                                            'latitude',
                                            type=openapi.TYPE_STRING,
                                            format='float',
                                            required=False),
                          openapi.Parameter('lon',
                                            openapi.IN_QUERY,
                                            'longitude',
                                            type=openapi.TYPE_STRING,
                                            format='float',
                                            required=False),
                          openapi.Parameter('radius',
                                            openapi.IN_QUERY,
                                            'radius (unit is meter)',
                                            type=openapi.TYPE_STRING,
                                            format='float',
                                            required=False),
                          openapi.Parameter('address',
                                            openapi.IN_QUERY,
                                            'address (street and number)',
                                            type=openapi.TYPE_STRING,
                                            format='string',
                                            required=False)],
    'responses': {
        200: openapi.Response('application/json',
                              openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                  'status': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='status'),
                                  'result': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                      'identifier': openapi.Schema(type=openapi.TYPE_STRING, description='identifier'),
                                      'project_type': openapi.Schema(type=openapi.TYPE_STRING, description='project_type'),
                                      'district_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='dictrict id'),
                                      'district_name': openapi.Schema(type=openapi.TYPE_STRING, description='district name'),
                                      'title': openapi.Schema(type=openapi.TYPE_STRING, description='title'),
                                      'subtitle': openapi.Schema(type=openapi.TYPE_STRING, description='subtitle'),
                                      'content_html': openapi.Schema(type=openapi.TYPE_STRING, description='content html'),
                                      'content_text': openapi.Schema(type=openapi.TYPE_STRING, description='content text'),
                                      'images': images,
                                      'publication_date': openapi.Schema(type=openapi.TYPE_STRING, description='publication date'),
                                      'modification_date': openapi.Schema(type=openapi.TYPE_STRING, description='modification date'),
                                      'source_url': openapi.Schema(type=openapi.TYPE_STRING, description='source url'),
                                      'last_seen': openapi.Schema(type=openapi.TYPE_STRING, description='datetime field'),
                                      'active': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='is record active'),
                                      'followed': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='is following this project'),
                                      'meter': openapi.Schema(type=openapi.TYPE_INTEGER, description='meter'),
                                      'strides': openapi.Schema(type=openapi.TYPE_INTEGER, description='strides'),
                                      'recent_articles': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                          'identifier': openapi.Schema(type=openapi.TYPE_STRING, description='identifier'),
                                          'publication_date': openapi.Schema(type=openapi.TYPE_STRING, description='publication date')
                                      }))
                                  }))
                              }),
                              examples={'application/json': {'status': True, 'result': []}}),
        405: openapi.Response('Error: Method not allowed'),
        422: openapi.Response('Error: Unprocessable Entity')
    },
    'tags': ['Projects']
}


as_project_details = {
    # /api/v1/project/details swagger_auto_schema
    'methods': ['get'],
    'manual_parameters': [openapi.Parameter('deviceId',
                                            openapi.IN_HEADER,
                                            description="device identifier",
                                            type=openapi.TYPE_STRING,
                                            required=True),
                          openapi.Parameter('id',
                                            openapi.IN_QUERY,
                                            'Project identifier',
                                            type=openapi.TYPE_STRING,
                                            format='<identifier>',
                                            required=True),
                          openapi.Parameter('articles_max_age',
                                            openapi.IN_QUERY,
                                            'Number of days (default: 3)',
                                            type=openapi.TYPE_INTEGER,
                                            format='<int>',
                                            required=False),
                          openapi.Parameter('lat',
                                            openapi.IN_QUERY,
                                            'latitude',
                                            type=openapi.TYPE_STRING,
                                            format='float',
                                            required=False),
                          openapi.Parameter('lon',
                                            openapi.IN_QUERY,
                                            'longitude',
                                            type=openapi.TYPE_STRING,
                                            format='float',
                                            required=False),
                          openapi.Parameter('address',
                                            openapi.IN_QUERY,
                                            'address (street and number)',
                                            type=openapi.TYPE_STRING,
                                            format='string',
                                            required=False),
                          ],
    'responses': {
        200: openapi.Response('application/json',
                              openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                  'status': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='status'),
                                  'result': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                      'identifier': openapi.Schema(type=openapi.TYPE_STRING, description='identifier'),
                                      'body': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                          'what': body_element,
                                          'when': body_element,
                                          'work': body_element,
                                          'where': body_element,
                                          'contact': body_element,
                                          'more-info': body_element,
                                          'timeline': timeline
                                      }),
                                      'district_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='dictrict id'),
                                      'district_name': openapi.Schema(type=openapi.TYPE_STRING, description='district name'),
                                      'news': news,
                                      'images': images,
                                      'page_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='page id'),
                                      'title': openapi.Schema(type=openapi.TYPE_STRING, description='title'),
                                      'subtitle': openapi.Schema(type=openapi.TYPE_STRING, description='subtitle'),
                                      'rel_url': openapi.Schema(type=openapi.TYPE_STRING, description='relative url'),
                                      'url': openapi.Schema(type=openapi.TYPE_STRING, description='url'),
                                      'meter': openapi.Schema(type=openapi.TYPE_STRING, description='distance between address and project'),
                                      'strides': openapi.Schema(type=openapi.TYPE_STRING, description='distance between address and project')
                                  })
                              }),
                              examples={'application/json': {'status': True, 'result': {}}}),
        404: openapi.Response('Error: No record found'),
        405: openapi.Response('Error: Method not allowed'),
        422: openapi.Response('Error: Unprocessable Entity')},
    'tags': ['Projects']
}


as_projects_follow_post = {
    # /api/v1/image swagger_auto_schema
    'methods': ['POST'],
    'manual_parameters': [openapi.Parameter('DeviceAuthorization',
                                            openapi.IN_HEADER,
                                            description="Device authorization token",
                                            type=openapi.TYPE_STRING,
                                            required=True),
                          openapi.Parameter('deviceId',
                                            openapi.IN_HEADER,
                                            description="device identifier",
                                            type=openapi.TYPE_STRING,
                                            required=True),
                          ],
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'project_id': openapi.Schema(type=openapi.TYPE_STRING, description='project identifier')
        }
    ),
    'responses': {
        200: openapi.Response('application/json',
                              examples={
                                  'application/json': {
                                      'status': True,
                                      'result': 'Subscription added'}
                              }),
        403: openapi.Response('application/json',
                              examples={
                              'application/json': {
                                  'status': False,
                                  'result': message.access_denied}}),
        404: openapi.Response('application/json',
                              examples={
                                  'application/json': {
                                      'status': False,
                                      'result': message.no_record_found}}),
        422: openapi.Response('application/json',
                              examples={
                                  'application/json': {
                                      'status': False,
                                      'result': message.invalid_headers}})
    },
    'tags': ['Projects']
}


as_projects_follow_delete = {
    # /api/v1/image swagger_auto_schema
    'methods': ['DELETE'],
    'manual_parameters': [openapi.Parameter('DeviceAuthorization',
                                            openapi.IN_HEADER,
                                            description="Device authorization token",
                                            type=openapi.TYPE_STRING,
                                            required=True),
                          openapi.Parameter('deviceId',
                                            openapi.IN_HEADER,
                                            description="device identifier",
                                            type=openapi.TYPE_STRING,
                                            required=True),
                          ],
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'project_id': openapi.Schema(type=openapi.TYPE_STRING, description='project identifier')
        }
    ),
    'responses': {
        200: openapi.Response('application/json',
                              examples={
                                  'application/json': {
                                      'status': True,
                                      'result': 'Subscription removed'}
                              }),
        403: openapi.Response('application/json',
                              examples={
                              'application/json': {
                                  'status': False,
                                  'result': message.access_denied}}),
        422: openapi.Response('application/json',
                              examples={
                                  'application/json': {
                                      'status': False,
                                      'result': message.invalid_headers}})
    },
    'tags': ['Projects']
}
