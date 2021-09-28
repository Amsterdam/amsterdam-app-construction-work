from amsterdam_app_api.swagger_views_ingest import as_ingest_projects
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
    paths = {
        'brug': '/projecten/bruggen/maatregelen-vernieuwen-bruggen/',
        'kade': '/projecten/kademuren/maatregelen-vernieuwing/'
    }

    # Get project type from query string or return invalid
    project_type = request.GET.get('project-type', '')
    if paths.get(request.GET.get('project-type', '')) is None:
        return Response({'status': False, 'result': message.invalid_query}, status=422)

    ingest = IproxIngestion()
    result = ingest.get_set_projects(project_type)

    return Response({'status': True, 'result': result}, status=200)
