from amsterdam_app_api.swagger.swagger_views_iprox_projects import as_projects, as_project_details, as_projects_follow_post, as_projects_follow_delete
from amsterdam_app_api.swagger.swagger_views_search import as_search
from amsterdam_app_api.api_messages import Messages
from amsterdam_app_api.models import Projects
from amsterdam_app_api.models import ProjectDetails
from amsterdam_app_api.models import FollowedProjects
from amsterdam_app_api.serializers import ProjectsSerializer
from amsterdam_app_api.serializers import ProjectDetailsSerializer
from amsterdam_app_api.GenericFunctions.SetFilter import SetFilter
from amsterdam_app_api.GenericFunctions.Sort import Sort
from amsterdam_app_api.GenericFunctions.TextSearch import TextSearch
from amsterdam_app_api.GenericFunctions.RequestMustComeFromApp import RequestMustComeFromApp
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.db import IntegrityError
from django.db.models import Count

message = Messages()


def search(model, request):
    text = request.GET.get('text', None)
    query_fields = request.GET.get('query_fields', '')
    fields = request.GET.get('fields', None)
    page_size = int(request.GET.get('page_size', 10))
    page = int(request.GET.get('page', 1)) - 1

    # Get Model fields
    model_fields = [x.name for x in model._meta.get_fields()]

    if text is None:
        return Response({'status': False, 'result': message.invalid_query}, status=422)
    if len([x for x in query_fields.split(',') if x not in model_fields]) > 0:
        return Response({'status': False, 'result': message.no_such_field_in_model}, status=422)
    if fields is not None and len([x for x in fields.split(',') if x not in model_fields]) > 0:
        return Response({'status': False, 'result': message.no_such_field_in_model}, status=422)

    text_search = TextSearch(model, text, query_fields, return_fields=fields, page_size=page_size, page=page)
    result = text_search.search()
    return Response({'status': True, 'result': result['page'], 'pages': result['pages']}, status=200)


@swagger_auto_schema(**as_projects)
@api_view(['GET'])
def projects(request):
    """
    Get a list of all projects. Narrow down by query param: project-type
    """
    if request.method == 'GET':
        deviceid = request.META.get('HTTP_DEVICEID', None)
        if deviceid is None:
            return Response({'status': False, 'result': message.invalid_headers}, status=422)

        project_type = request.GET.get('project-type', None)
        sort_by = request.GET.get('sort-by', None)
        sort_order = request.GET.get('sort-order', None)
        model_items = request.GET.get('fields', None)
        fields = [] if model_items is None else model_items.split(',')
        followed = False
        if 'followed' in fields:
            fields.remove('followed')
            if 'identifier' in fields:
                followed = True

        # Check query parameters
        if project_type is not None and project_type not in ['brug', 'kade', 'bouw-en-verkeer']:
            return Response({'status': False, 'result': message.invalid_query}, status=422)

        # Get list of projects by district
        try:
            district_id = int(request.GET.get('district-id', None))
        except Exception as error:
            district_id = None

        # Set filter
        query_filter = SetFilter(district_id=district_id, project_type=project_type, active=True).get()

        # Return filtered result or all projects
        projects_object = Projects.objects.filter(**query_filter).all()

        # Get followers for projects
        following = [x['projectid'] for x in FollowedProjects.objects.filter(deviceid__iexact=deviceid).values('projectid')]

        if len(fields) != 0:
            serializer = ProjectsSerializer(projects_object, context={'fields': fields}, many=True)
            if followed is True:
                for i in range(len(serializer.data)):
                    serializer.data[i]['followed'] = False
                    if serializer.data[i]['identifier'] in following:
                        serializer.data[i]['followed'] = True
        else:
            serializer = ProjectsSerializer(projects_object, many=True)
            for i in range(len(serializer.data)):
                serializer.data[i]['followed'] = False
                if serializer.data[i]['identifier'] in following:
                    serializer.data[i]['followed'] = True

        result = Sort().list_of_dicts(serializer.data, key=sort_by, sort_order=sort_order)
        return Response({'status': True, 'result': result}, status=200)


@swagger_auto_schema(**as_search)
@api_view(['GET'])
def projects_search(request):
    model = Projects
    result = search(model, request)
    return result


@swagger_auto_schema(**as_project_details)
@api_view(['GET'])
def project_details(request):
    """
    Get details for a project by identifier
    """
    if request.method == 'GET':
        deviceid = request.META.get('HTTP_DEVICEID', None)
        if deviceid is None:
            return Response({'status': False, 'result': message.invalid_headers}, status=422)

        identifier = request.GET.get('id', None)
        if identifier is None:
            return Response({'status': False, 'result': message.invalid_query}, status=422)

        project_object = ProjectDetails.objects.filter(pk=identifier, active=True).first()
        if project_object is not None:
            count = FollowedProjects.objects.filter(projectid=identifier).count()
            followed = FollowedProjects.objects.filter(deviceid=deviceid, projectid=identifier).first()
            project_data = dict(ProjectDetailsSerializer(project_object, many=False).data)
            project_data['followers'] = count
            project_data['followed'] = False if followed is None else True
            return Response({'status': True, 'result': project_data}, status=200)
        else:
            return Response({'status': False, 'result': message.no_record_found}, status=404)


@swagger_auto_schema(**as_search)
@api_view(['GET'])
def project_details_search(request):
    model = ProjectDetails
    result = search(model, request)
    return result


@swagger_auto_schema(**as_projects_follow_post)
@swagger_auto_schema(**as_projects_follow_delete)
@api_view(['POST', 'DELETE'])
@RequestMustComeFromApp
def projects_follow(request):
    deviceid = request.META.get('HTTP_DEVICEID', None)
    if deviceid is None:
        return Response({'status': False, 'result': message.invalid_headers}, status=422)

    project_id = request.data.get('projectId', None)
    if project_id is not None:
        project = ProjectDetails.objects.filter(identifier=project_id).first()
        if project is None:
            return Response({'status': False, 'result': message.no_record_found}, status=404)

    if request.method == 'POST':
        try:
            follow_project = FollowedProjects(projectid=project_id, deviceid=deviceid)
            follow_project.save()
        except IntegrityError:  # Double request with same data, discard...
            pass
        return Response({'status': False, 'result': 'Subscription added'}, status=200)

    if request.method == 'DELETE':
        FollowedProjects(projectid=project_id, deviceid=deviceid).delete()
        return Response({'status': False, 'result': 'Subscription removed'}, status=200)
