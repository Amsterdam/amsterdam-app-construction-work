from amsterdam_app_api.api_messages import Messages
from amsterdam_app_api.models import Projects
from amsterdam_app_api.models import ProjectManager
from amsterdam_app_api.serializers import ProjectManagerSerializer
from amsterdam_app_api.swagger_views_project_manager import as_project_manager_post_patch
from amsterdam_app_api.swagger_views_project_manager import as_project_manager_delete
from amsterdam_app_api.swagger_views_project_manager import as_project_manager_get
from django.db.models import Q
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from amsterdam_app_api.GenericFunctions.IsAuthorized import IsAuthorized
messages = Messages()

""" Views for CRUD a project-manager and assign projects
"""


@swagger_auto_schema(**as_project_manager_post_patch)
@swagger_auto_schema(**as_project_manager_delete)
@swagger_auto_schema(**as_project_manager_get)
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
#@IsAuthorized
def crud(request):
    if request.method in ['GET']:
        """ Get project manager(s). Optionally filter by id 
        """
        data = get(request)
        return Response(data['result'], status=data['status'])
    elif request.method in ['POST', 'PATCH']:
        data = post_patch(request)
        return Response(data['result'], status=data['status'])
    elif request.method in ['DELETE']:
        data = delete(request)
        return Response(data['result'], status=data['status'])


def get(request):
    """ Get one or all project managers from database
    """
    identifier = request.GET.get('id', None)
    if identifier is None:
        project_manager_objects = ProjectManager.objects.all()
        serializer = ProjectManagerSerializer(project_manager_objects, many=True)
        return {'result': {'status': True, 'result': serializer.data}, 'status': 200}
    else:
        project_manager_object = ProjectManager.objects.filter(pk=identifier).first()
        serializer = ProjectManagerSerializer(project_manager_object, many=False)
        return {'result': {'status': True, 'result': [serializer.data]}, 'status': 200}


def post_patch(request):
    """
    Register a project manager with an optional set of project identifiers
    """
    identifier = request.data.get('identifier', None)
    email = request.data.get('email', None)
    projects = request.data.get('projects', list())

    if email is None:
        return {'result': {'status': False, 'result': messages.invalid_query}, 'status': 422}

    for project in projects:
        if Projects.objects.filter(pk=project).first() is None:
            return {'result': {'status': False, 'result': messages.no_record_found}, 'status': 404}

    project_manager_object = ProjectManager.objects.filter(Q(pk=identifier) | Q(email=email)).first()

    # New record
    if project_manager_object is None:
        try:
            project_manager_object = ProjectManager(identifier=identifier, email=email, projects=projects)
            project_manager_object.save()
            return {'result': {'status': True, 'result': 'Project manager created', 'identifier': project_manager_object.identifier}, 'status': 200}
        except Exception as error:
            return {'result': {'status': False, 'result': str(error)}, 'status': 422}

    # Update existing record
    else:
        project_manager_object.identifier = identifier
        project_manager_object.email = email
        project_manager_object.projects = projects
        project_manager_object.save()

    return {'result': {'status': True, 'result': 'Project manager updated'}, 'status': 200}


def delete(request):
    identifier = request.GET.get('id', None)
    if identifier is None:
        return {'result': {'status': False, 'result': messages.invalid_query}, 'status': 422}
    else:
        # remove project manager from database
        ProjectManager.objects.filter(pk=identifier).delete()
        return {'result': {'status': True, 'result': 'Project manager removed'}, 'status': 200}

