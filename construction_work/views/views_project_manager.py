""" Views for CRUD a project-manager and assign projects
"""

from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from construction_work.api_messages import Messages
from construction_work.generic_functions.is_authorized import (
    IsAuthorized,
    JWTAuthorized,
)
from construction_work.models import Project, ProjectManager
from construction_work.serializers import (
    ProjectManagerAugmentedSerializer,
    ProjectManagerSerializer,
)
from construction_work.swagger.swagger_views_project_manager import (
    as_project_manager_delete,
    as_project_manager_get,
    as_project_manager_post_patch,
)

messages = Messages()


@swagger_auto_schema(**as_project_manager_post_patch)
@swagger_auto_schema(**as_project_manager_delete)
@swagger_auto_schema(**as_project_manager_get)
@api_view(["GET", "POST", "PATCH", "DELETE"])
def crud(request):
    """CRUD project manager(s)"""
    if request.method == "GET":
        return get(request)

    if request.method in ["POST"]:
        return post(request)

    if request.method in ["PATCH"]:
        return patch(request)

    if request.method in ["DELETE"]:
        return delete(request)


def get(request):
    """Get one or all project managers from database"""
    manager_key = request.GET.get("manager_key", None)

    @IsAuthorized
    def get_single_manager(_request, manager_key):
        # Call is made from mobile device
        project_manager_object = ProjectManager.objects.filter(
            manager_key=manager_key
        ).first()
        if project_manager_object is None:
            return Response(
                data=messages.no_record_found, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProjectManagerAugmentedSerializer(instance=project_manager_object)
        return serializer.data

    @JWTAuthorized
    def get_all_managers(_request):
        # Call is made from VUE, we expect a valid jwt token to continue
        project_manager_objects = ProjectManager.objects.all()
        serializer = ProjectManagerSerializer(project_manager_objects, many=True)
        return serializer.data

    if manager_key:
        get_response = get_single_manager(request, manager_key)
    else:
        get_response = get_all_managers(request)

    # Get functions might return HttpResponseForbidden
    if isinstance(get_response, HttpResponse):
        return get_response

    return Response(data=get_response, status=status.HTTP_200_OK)


@JWTAuthorized
def patch(request):
    """Patch an existing project manager"""
    manager_key = request.data.get("manager_key", None)
    if manager_key is None:
        return Response(data=messages.invalid_query, status=status.HTTP_400_BAD_REQUEST)

    project_manager = ProjectManager.objects.filter(manager_key=manager_key).first()
    if project_manager is None:
        return Response(data=messages.no_record_found, status=status.HTTP_404_NOT_FOUND)

    # Rest of code is equal to post request
    return post(request)


@JWTAuthorized
def post(request):
    """Register a project manager with an optional set of project identifiers"""
    manager_key = request.data.get("manager_key", None)
    email = request.data.get("email", None)
    project_ids = request.data.get("projects", [])

    if email is None:
        return Response(data=messages.invalid_query, status=status.HTTP_400_BAD_REQUEST)

    projects = list(Project.objects.filter(pk__in=project_ids).all())

    # Check if all projects really exist
    if len(projects) != len(project_ids) and len(project_ids) != 0:
        return Response(data=messages.no_record_found, status=status.HTTP_404_NOT_FOUND)

    project_manager_object = ProjectManager.objects.filter(
        manager_key=manager_key
    ).first()

    # TODO: check if manager key is UUID, should be done by serializer.is_valid?

    # Use the instance parameter to update the existing article or create a new one
    project_manager = {"manager_key": manager_key, "email": email}
    serializer = ProjectManagerSerializer(
        instance=project_manager_object, data=project_manager
    )
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    updated_project_manager = serializer.save()

    # Add related projects to the ProjectManager instance
    updated_project_manager.projects.set(project_ids)
    updated_project_manager.save()

    return Response(data=serializer.data, status=status.HTTP_200_OK)


@JWTAuthorized
def delete(request):
    """Delete project manager"""
    manager_key = request.GET.get("manager_key", None)

    if manager_key is None:
        return Response(data=messages.invalid_query, status=status.HTTP_400_BAD_REQUEST)

    # remove project manager from database
    ProjectManager.objects.filter(manager_key=manager_key).delete()
    return Response(data="Project manager removed", status=status.HTTP_200_OK)
