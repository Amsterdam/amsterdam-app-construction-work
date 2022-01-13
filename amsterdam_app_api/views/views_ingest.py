from amsterdam_app_api.swagger.swagger_views_ingest import as_ingest_projects
from amsterdam_app_api.api_messages import Messages
from amsterdam_app_api.FetchData.IproxIngestion import IproxIngestion
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


message = Messages()


@swagger_auto_schema(**as_ingest_projects)
@api_view(['GET'])
def ingest_projects(request):
    """
    Ingestion route for acquiring data for the backend from multiple 'Gemeente Amsterdam' sources
    """
    project_types = ['brug', 'kade', 'stadsloket']

    # Get project type from query string or return invalid
    project_type = request.GET.get('project-type', '')
    if project_type not in project_types:
        return Response({'status': False, 'result': message.invalid_query}, status=422)

    ingest = IproxIngestion()
    result = ingest.start(project_type)

    return Response({'status': True, 'result': result}, status=200)
