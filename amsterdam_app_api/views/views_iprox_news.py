from amsterdam_app_api.api_messages import Messages
from amsterdam_app_api.swagger.swagger_views_iprox_news import as_news
from amsterdam_app_api.models import News
from amsterdam_app_api.serializers import NewsSerializer
from amsterdam_app_api.GenericFunctions.SetFilter import SetFilter
from amsterdam_app_api.GenericFunctions.Sort import Sort
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

message = Messages()


@swagger_auto_schema(**as_news)
@api_view(['GET'])
def news(request):
    """
    Get a list of news items. Narrow down by query param: identifier (from project details)
    """
    if request.method == 'GET':
        project_identifier = request.GET.get('project-identifier', None)
        sort_by = request.GET.get('sort-by', 'publication_date')
        sort_order = request.GET.get('sort-order', 'desc')

        # Set filter
        query_filter = SetFilter(project_identifier=project_identifier).get()

        # Return filtered result or all projects
        if query_filter != {}:
            news_objects = News.objects.filter(**query_filter).all()
        # Get all projects
        else:
            news_objects = News.objects.all()

        serializer = NewsSerializer(news_objects, many=True)
        result = Sort().list_of_dicts(serializer.data, key=sort_by, sort_order=sort_order)
        return Response({'status': True, 'result': result}, status=200)
