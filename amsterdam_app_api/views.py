from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from django.http import JsonResponse, HttpResponse
from amsterdam_app_api.models import Projects, ProjectDetails, Image
from amsterdam_app_api.serializers import ProjectsSerializer, ProjectDetailsSerializer, ImageSerializer
from amsterdam_app_api.FetchData.Projects import IngestProjects
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(methods=['get'], manual_parameters=[
    openapi.Parameter('project-type', openapi.IN_QUERY, "options: [brug, kade]", type=openapi.TYPE_STRING)
], responses={
    200: openapi.Response('application/json'),
    405: openapi.Response('Error: Method not allowed'),
    422: openapi.Response('Error: Unprocessable Entity')
}, tags=['Projects'])
@api_view(['GET'])
def projects(request):
    """
    Get a list of all projects. Narrow down by query param: project-type
    """
    search_queries = ['brug', 'kade']
    if request.method == 'GET':
        project_type = request.GET.get('project-type', None)
        if project_type not in search_queries and project_type is not None:
            return Response(
                {
                    'status': False,
                    'result': 'Invalid query parameter. param(s): project-type={params}'.format(params=search_queries)
                },
                status=422)

        # Get list of projects by type
        if project_type is not None:
            projects_object = Projects.objects.filter(project_type=project_type).all()

        # Get all projects
        else:
            projects_object = Projects.objects.all()

        serializer = ProjectsSerializer(projects_object, many=True)
        # return JsonResponse({'status': True, 'result': serializer.data}, safe=False, status=200)
        return Response({'status': True, 'result': serializer.data}, status=200)
    else:
        return Response({'status': False, 'result': 'Method not allowed'}, status=405)


@swagger_auto_schema(methods=['get'], manual_parameters=[
    openapi.Parameter('id', openapi.IN_QUERY, "identifier", type=openapi.TYPE_STRING)
], responses={
    200: openapi.Response('application/json'),
    404: openapi.Response('Error: No record found'),
    405: openapi.Response('Error: Method not allowed'),
    422: openapi.Response('Error: Unprocessable Entity'),
}, tags=['Project details'])
@api_view(['GET'])
def project_details(request):
    """
    Get details for a project by identifier
    """
    if request.method == 'GET':
        identifier = request.GET.get('id', None)
        if identifier is None:
            return Response(
                {
                    'status': False,
                    'result': 'Invalid query parameter. param(s): id=<identifier>'
                },
                status=422
            )
        else:
            project_object = ProjectDetails.objects.filter(pk=identifier).first()
            if project_object is not None:
                serializer = ProjectDetailsSerializer(project_object, many=False)
                return Response({'status': True, 'result': serializer.data}, status=200)
            else:
                return Response({'status': False, 'result': 'No record found'}, status=404)
    else:
        return Response({'status': False, 'result': 'Method not allowed'}, status=405)


@swagger_auto_schema(methods=['get'], manual_parameters=[
    openapi.Parameter('project-type', openapi.IN_QUERY, "options: [brug, kade]", type=openapi.TYPE_STRING)
], responses={
    200: openapi.Response('application/json'),
    422: openapi.Response('Error: Unprocessable Entity')
}, tags=['Ingestion'])
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
        result = 'Invalid query parameter. param(s): project-type={params}'.format(params=[key for key in paths.keys()])
        return Response({'status': False, 'result': result}, status=422)

    ingest = IngestProjects()
    result = ingest.get_set_projects(project_type)

    return Response({'status': True, 'result': result}, status=200)


@swagger_auto_schema(methods=['get'], manual_parameters=[
    openapi.Parameter('id', openapi.IN_QUERY, "identifier", type=openapi.TYPE_STRING)
], responses={
    200: openapi.Response('Binary data'),
    404: openapi.Response('Error: file not found'),
    422: openapi.Response('Error: Unprocessable Entity')
}, tags=['Image'])
@api_view(['GET'])
def image(request):
    """
    Request image from API by identifier
    """
    if request.method == 'GET':
        identifier = request.GET.get('id', None)
        if identifier is None:
            return Response(
                {
                    'status': False,
                    'result': 'Invalid query parameter. param(s): identifier=<identifier>'
                },
                status=422)
        else:
            image_object = Image.objects.filter(pk=identifier).first()
            if image_object is not None:
                return HttpResponse(image_object.data, content_type=image_object.mime_type, status=200)
            else:
                return Response('No image found', status=404)
