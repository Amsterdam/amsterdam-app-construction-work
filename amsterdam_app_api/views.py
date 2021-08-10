from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from amsterdam_app_api.models import ProjectenBruggen, ProjectenKademuren
from amsterdam_app_api.serializers import ProjectenBruggenSerializer, ProjectenKademurenSerializer
from amsterdam_app_api.FetchData.ProjectenBruggen import FetchProjectAll, FetchProjectDetails


def all_projects(request):
    """
    List all code snippets, or create a new snippet.
    """
    project_types = ['brug', 'kade']
    if request.method == 'GET':
        project_type = request.GET.get('project-type', '')
        if project_type not in project_types:
            return JsonResponse({'status': False,
                                 'result': 'Invalid query parameter. Valid query params: project-type={params}'.format(params=project_types)})

        if project_type == 'brug':
            projects = ProjectenBruggen.objects.all()
            serializer = ProjectenBruggenSerializer(projects, many=True)
            return JsonResponse(serializer.data, safe=False)
        elif project_type == 'kade':
            projects = ProjectenKademuren.objects.all()
            serializer = ProjectenKademurenSerializer(projects, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            JsonResponse({'status': False,
                          'result': 'Invalid request'})


def ingest_all_projects(request):
    """
    Should move to cron job!!!!
    :param request:
    :return:
    """
    paths = {
        'brug': '/projecten/bruggen/maatregelen-vernieuwen-bruggen/',
        'kade': '/projecten/kademuren/maatregelen-vernieuwing/'
    }

    # Get project type from query string or return invalid
    project_type = request.GET.get('project-type', '')
    if paths.get(request.GET.get('project-type', '')) is None:
        return JsonResponse({'status': False,
                             'result': 'Invalid query parameter. Valid query params: project-type={params}'.format(params=[key for key in paths.keys()])})

    # Fetch projects and ingest data
    fpa = FetchProjectAll(paths.get(request.GET.get('project-type')))
    fpa.get_data()
    fpa.parse_data()

    updated = new = failed = 0
    for item in fpa.parsed_data:
        if project_type == 'kade':
            try:
                project, created = ProjectenKademuren.objects.update_or_create(identifier=item.get('identifier'))

                if created:
                    project = ProjectenKademuren(**item)
                    project.save()
                    new += 1
                else:
                    ProjectenKademuren.objects.filter(pk=item.get('identifier')).update(**item)
                    updated += 1
            except Exception as error:
                print('failed ingesting data {project}: {error}'.format(project=item.get('title'), error=error))
                failed += 1
        elif project_type == 'brug':
            try:
                project, created = ProjectenBruggen.objects.update_or_create(identifier=item.get('identifier'))

                if created:
                    project = ProjectenBruggen(**item)
                    project.save()
                    new += 1
                else:
                    ProjectenBruggen.objects.filter(pk=item.get('identifier')).update(**item)
                    updated += 1
            except Exception as error:
                print('failed ingesting data {project}: {error}'.format(project=item.get('title'), error=error))
                failed += 1

    return JsonResponse({'status': True,
                         'result': 'Updated: {updated}, New: {new}, Failed: {failed}'.format(new=new,
                                                                                             updated=updated,
                                                                                             failed=failed)})


