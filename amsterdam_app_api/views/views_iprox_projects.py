from amsterdam_app_api.swagger.swagger_views_iprox_projects import as_projects, as_project_details
from amsterdam_app_api.api_messages import Messages
from amsterdam_app_api.models import Projects
from amsterdam_app_api.models import ProjectDetails
from amsterdam_app_api.models import News
from amsterdam_app_api.models import WarningMessages
from amsterdam_app_api.serializers import ProjectsSerializer
from amsterdam_app_api.serializers import ProjectDetailsSerializer
from amsterdam_app_api.serializers import NewsSerializer
from amsterdam_app_api.serializers import WarningMessagesExternalSerializer
from amsterdam_app_api.GenericFunctions.SetFilter import SetFilter
from amsterdam_app_api.GenericFunctions.Sort import Sort
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

message = Messages()


@swagger_auto_schema(**as_projects)
@api_view(['GET'])
def projects(request):
    """
    Get a list of all projects. Narrow down by query param: project-type
    """
    if request.method == 'GET':
        project_type = request.GET.get('project-type', None)
        sort_by = request.GET.get('sort-by', None)
        sort_order = request.GET.get('sort-order', None)

        # Check query parameters
        if project_type is not None and project_type not in ['brug', 'kade']:
            return Response({'status': False, 'result': message.invalid_query}, status=422)

        # Get list of projects by district
        try:
            district_id = int(request.GET.get('district-id', None))
        except Exception as error:
            district_id = None

        # Set filter
        query_filter = SetFilter(district_id=district_id, project_type=project_type).get()

        # Return filtered result or all projects
        if query_filter != {}:
            projects_object = Projects.objects.filter(**query_filter).all()
        # Get all projects
        else:
            projects_object = Projects.objects.all()

        serializer = ProjectsSerializer(projects_object, many=True)
        result = Sort().list_of_dicts(serializer.data, key=sort_by, sort_order=sort_order)
        return Response({'status': True, 'result': result}, status=200)


@swagger_auto_schema(**as_project_details)
@api_view(['GET'])
def project_details(request):
    """
    Get details for a project by identifier
    """
    def filter(data, article_type):
        articles = []
        for item in data:
            articles.append({
                'identifier': item['identifier'],
                'title': item['title'],
                'publication_date': item['publication_date'].split('T')[0],
                'type': article_type,
                'image': next(iter([x for x in item['images'] if x['type'] in ['banner', 'header']]), None)
            })
        sorted_articles = Sort().list_of_dicts(articles, key='publication_date', sort_order='asc')
        return sorted_articles

    if request.method == 'GET':
        identifier = request.GET.get('id', None)
        if identifier is None:
            return Response({'status': False, 'result': message.invalid_query}, status=422)
        else:
            project_object = ProjectDetails.objects.filter(pk=identifier).first()
            if project_object is not None:
                articles = []
                project_data = ProjectDetailsSerializer(project_object, many=False).data
                news_objects = News.objects.filter(project_identifier=identifier).all()
                warning_messages_objects = WarningMessages.objects.filter(project_identifier=identifier).all()
                news_data = NewsSerializer(news_objects, many=True).data
                warning_messages_data = WarningMessagesExternalSerializer(warning_messages_objects, many=True).data
                articles += filter(news_data, 'news')
                articles += filter(warning_messages_data, 'warning')
                del project_data['news']
                project_data['articles'] = articles
                return Response({'status': True, 'result': project_data}, status=200)
            else:
                return Response({'status': False, 'result': message.no_record_found}, status=404)
