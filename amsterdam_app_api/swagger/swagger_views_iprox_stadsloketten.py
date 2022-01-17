from drf_yasg import openapi


as_city_contact = {
    'methods': ['get'],
    'responses': {
        200: openapi.Response('application/json',
                              openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                  'title': openapi.Schema(type=openapi.TYPE_STRING, description='title'),
                                  'html': openapi.Schema(type=openapi.TYPE_STRING, description='html formatted text'),
                                  'text': openapi.Schema(type=openapi.TYPE_STRING, description='plain text'),
                              })),
                              examples={'application/json': {'status': True, 'result': {}}})
    },
    'tags': ['City']
}


as_city_offices = {
    'methods': ['get'],
    'responses': {
        200: openapi.Response('application/json',
                              openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                  'url': openapi.Schema(type=openapi.TYPE_STRING, description='original url'),
                                  'location': openapi.Schema(type=openapi.TYPE_STRING, description='text'),
                                  'identifier': openapi.Schema(type=openapi.TYPE_STRING, description='identifier'),
                              })),
                              examples={'application/json': {'status': True, 'result': {}}})
    },
    'tags': ['City']
}


as_city_office = {
    'methods': ['get'],
    'manual_parameters': [openapi.Parameter('id',
                                            openapi.IN_QUERY,
                                            'CityOffice identifier',
                                            type=openapi.TYPE_STRING,
                                            format='<identifier>',
                                            required=True)],
    'responses': {
        200: openapi.Response('application/json',
                              openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                  'identifier': openapi.Schema(type=openapi.TYPE_STRING, description='identifier'),
                                  'location': openapi.Schema(type=openapi.TYPE_STRING, description='CityOffice'),
                                  'contact': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                      "Bellen": openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                          "txt": openapi.Schema(type=openapi.TYPE_STRING, description='plain text'),
                                          "html": openapi.Schema(type=openapi.TYPE_STRING, description='html formatted text'),
                                      }),
                                      "Mailen": openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                          "txt": openapi.Schema(type=openapi.TYPE_STRING, description='plain text'),
                                          "html": openapi.Schema(type=openapi.TYPE_STRING, description='html formatted text'),
                                      }),
                                      "Openingstijden": openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                          "txt": openapi.Schema(type=openapi.TYPE_STRING, description='plain text'),
                                          "html": openapi.Schema(type=openapi.TYPE_STRING, description='html formatted text')
                                      }),
                                  }),
                                  'images': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                      'type': openapi.Schema(type=openapi.TYPE_STRING, description='image type'),
                                      'sources': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                          "orig": openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                              "url": openapi.Schema(type=openapi.TYPE_STRING, description='original url'),
                                              "filename": openapi.Schema(type=openapi.TYPE_STRING, description='filename'),
                                              "image_id": openapi.Schema(type=openapi.TYPE_STRING, description='identifier'),
                                              "description": openapi.Schema(type=openapi.TYPE_STRING, description='description'),
                                          }),
                                          "XXXpx": openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                              "url": openapi.Schema(type=openapi.TYPE_STRING, description='original url'),
                                              "filename": openapi.Schema(type=openapi.TYPE_STRING, description='filename'),
                                              "image_id": openapi.Schema(type=openapi.TYPE_STRING, description='identifier'),
                                              "description": openapi.Schema(type=openapi.TYPE_STRING, description='description'),
                                          })
                                      })
                                  }),
                                  'info': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                      "txt": openapi.Schema(type=openapi.TYPE_STRING, description='plain text'),
                                      "html": openapi.Schema(type=openapi.TYPE_STRING, description='html formatted text'),
                                  }),
                                  'address': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                      "txt": openapi.Schema(type=openapi.TYPE_STRING, description='plain text'),
                                      "html": openapi.Schema(type=openapi.TYPE_STRING, description='html formatted text'),
                                  }),
                                  'last_seen': openapi.Schema(type=openapi.TYPE_STRING, description='date'),
                                  'active': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='active record')
                              }),
                              examples={'application/json': {'status': True, 'result': {}}}),
        404: openapi.Response('Error: No record found'),
        422: openapi.Response('Error: Unprocessable Entity')},
    'tags': ['City']
}