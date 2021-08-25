from django.http import HttpResponse
from amsterdam_app_api.views_swagger_auto_schema import as_projects, as_project_details, as_ingest_projects, as_image
from amsterdam_app_api.models import Projects, ProjectDetails, Image
from amsterdam_app_api.serializers import ProjectsSerializer, ProjectDetailsSerializer
from amsterdam_app_api.FetchData.Projects import IngestProjects
from amsterdam_app_api.GenericFunctions.SetFilter import SetFilter
from amsterdam_app_api.GenericFunctions.Sort import Sort
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


# Generic error message pointing to a single documentation point
invalid_query_message = 'Invalid query parameter(s). See /api/v1/apidocs for more information'


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
            return Response({'status': False, 'result': invalid_query_message}, status=422)

        # Get list of projects by district
        try:
            district_id = int(request.GET.get('district_id', None))
        except Exception as error:
            district_id = None

        # Set filter
        query_filter = SetFilter(district_id=district_id, project_type=project_type).get()

        # Return filtered result or all projects
        if filter != {}:
            projects_object = Projects.objects.filter(**query_filter).all()
        # Get all projects
        else:
            projects_object = Projects.objects.all()

        serializer = ProjectsSerializer(projects_object, many=True)
        result = Sort().list_of_dicts(serializer.data, key=sort_by, sort_order=sort_order)
        return Response({'status': True, 'result': result}, status=200)
    else:
        return Response({'status': False, 'result': 'Method not allowed'}, status=405)


@swagger_auto_schema(**as_project_details)
@api_view(['GET'])
def project_details(request):
    """
    Get details for a project by identifier
    """
    if request.method == 'GET':
        identifier = request.GET.get('id', None)
        if identifier is None:
            return Response({'status': False, 'result': invalid_query_message}, status=422)
        else:
            project_object = ProjectDetails.objects.filter(pk=identifier).first()
            if project_object is not None:
                serializer = ProjectDetailsSerializer(project_object, many=False)
                return Response({'status': True, 'result': serializer.data}, status=200)
            else:
                return Response({'status': False, 'result': 'No record found'}, status=404)
    else:
        return Response({'status': False, 'result': 'Method not allowed'}, status=405)


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
        return Response({'status': False, 'result': invalid_query_message}, status=422)

    ingest = IngestProjects()
    result = ingest.get_set_projects(project_type)

    return Response({'status': True, 'result': result}, status=200)


@swagger_auto_schema(**as_image)
@api_view(['GET'])
def image(request):
    """
    Request image from API by identifier
    """
    if request.method == 'GET':
        identifier = request.GET.get('id', None)
        if identifier is None:
            return Response({'status': False, 'result': invalid_query_message}, status=422)
        else:
            image_object = Image.objects.filter(pk=identifier).first()
            if image_object is not None:
                return HttpResponse(image_object.data, content_type=image_object.mime_type, status=200)
            else:
                return Response('No image found', status=404)
