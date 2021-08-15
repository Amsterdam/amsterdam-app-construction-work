from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse, HttpResponse
from amsterdam_app_api.models import Projects, ProjectDetails, Image
from amsterdam_app_api.serializers import ProjectsSerializer, ProjectDetailsSerializer, ImageSerializer
from amsterdam_app_api.FetchData.Projects import IngestProjects


def projects(request):
    """
    Get a list of all projects. Narrow down by query param: project-type

    :param request: project-type=[<brug>, <kade>]
    :return: JsonResponse
    """
    search_queries = ['brug', 'kade']
    if request.method == 'GET':
        project_type = request.GET.get('project-type', None)
        if project_type not in search_queries and project_type is not None:
            return JsonResponse(
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
        return JsonResponse({'status': True, 'result': serializer.data}, safe=False, status=200)
    else:
        return JsonResponse({'status': False, 'result': 'Method not allowed'}, status=405)


def project_details(request):
    """
    Get details for a project by identifier

    :param request: id=<identifier>
    :return: JsonResponse
    """
    if request.method == 'GET':
        identifier = request.GET.get('id', None)
        if identifier is None:
            return JsonResponse(
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
                return JsonResponse({'status': True, 'result': serializer.data}, safe=False, status=200)
            else:
                return JsonResponse({'status': False, 'result': 'No record found'}, status=404)
    else:
        return JsonResponse({'status': False, 'result': 'Method not allowed'}, status=405)


def ingest_projects(request):
    """
    Should move to cron job!!!!
    :param request:
    :return: JsonResponse
    """
    paths = {
        'brug': '/projecten/bruggen/maatregelen-vernieuwen-bruggen/',
        'kade': '/projecten/kademuren/maatregelen-vernieuwing/'
    }

    # Get project type from query string or return invalid
    project_type = request.GET.get('project-type', '')
    if paths.get(request.GET.get('project-type', '')) is None:
        result = 'Invalid query parameter. param(s): project-type={params}'.format(params=[key for key in paths.keys()])
        return JsonResponse({'status': False, 'result': result}, status=422)

    ingest = IngestProjects()
    result = ingest.get_set_projects(project_type)

    return JsonResponse({'status': True, 'result': result}, status=200)


def image(request):
    """
    Endpoint for retrieving images from database

    :param request:
    :return: HttpResponse
    """
    if request.method == 'GET':
        identifier = request.GET.get('id', None)
        if identifier is None:
            return JsonResponse(
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
                return HttpResponse('No image found', status=404)
