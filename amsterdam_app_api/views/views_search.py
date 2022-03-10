from rest_framework.response import Response
from django.contrib.postgres.search import TrigramSimilarity
from rest_framework.decorators import api_view
from django.apps import apps
from amsterdam_app_api.api_messages import Messages
from amsterdam_app_api.swagger.swagger_views_search import as_search
from drf_yasg.utils import swagger_auto_schema

messages = Messages()


@swagger_auto_schema(**as_search)
@api_view(['GET'])
def string_in_model(request):
    # Get query parameters
    query_model_name = request.GET.get('model', 'ProjectDetails')
    query_string = request.GET.get('text', '')
    query_fields = request.GET.get('query_fields', 'title,subtitle')
    model_items = request.GET.get('fields', None)
    min_similarity = request.GET.get('min_similarity', '0.07')
    limit = request.GET.get('limit', 20)

    # Get appropriate model and filter
    all_models = apps.all_models['amsterdam_app_api']
    forbidden_models = ['ProjectManager', 'MobileDevices']
    if query_model_name.lower() in all_models and query_model_name.lower() not in forbidden_models:
        model = all_models[query_model_name.lower()]
        model_fields = [x.name for x in model._meta.get_fields() if x.name != 'data'] + ['similarity']
    else:
        return Response({'status': False, 'result': messages.no_such_database_model}, status=404)

    # Build filter and query
    similarity = 0
    weight = 1.0
    for query_field in query_fields.split(','):
        if query_field not in model_fields:
            return Response({'status': False, 'result': messages.no_such_field_in_model}, status=404)
        similarity += weight * TrigramSimilarity(query_field, query_string)
        weight = weight / 2  # Next item has half the weight of the previous item
    search_results = list(model.objects.annotate(similarity=similarity).filter(similarity__gt=float(min_similarity)).order_by('-similarity'))[:int(limit)]

    # Build field list for given model
    if model_items is not None:
        model_fields = [x for x in model_fields if x in model_items.split(',')]

    # Filter field from search_results
    result = list()
    for search_result in search_results:
        data = {}
        for model_field in model_fields:
            data[model_field] = getattr(search_result, model_field)
        result.append(data)

    # Return result
    return Response({'status': True, 'result': result}, status=200)
