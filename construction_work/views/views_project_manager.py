""" Views for CRUD a project-manager and assign projects
"""

from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from construction_work.api_messages import Messages
from construction_work.generic_functions.is_authorized import IsAuthorized, get_jwt_auth_token, is_valid_jwt_token
from construction_work.models import Project, ProjectManager
from construction_work.serializers import ProjectManagerSerializer
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
@IsAuthorized
def crud(request):
    """CRUD project manager(s)"""
    if request.method == "GET":
        return get(request)

    if request.method in ["POST", "PATCH"]:
        return post_patch(request)

    if request.method in ["DELETE"]:
        return delete(request)


def get(request):
    """Get one or all project managers from database"""
    manager_key = request.GET.get("manager_key", None)
    if manager_key is None:
        # Call is made from VUE, we expect a valid jwt token to continue
        jwt_token = get_jwt_auth_token(request)
        if not is_valid_jwt_token(jwt_encrypted_token=jwt_token):
            return Response(data=messages.access_denied, status=status.HTTP_403_FORBIDDEN)

        project_manager_objects = ProjectManager.objects.all()
        serializer = ProjectManagerSerializer(project_manager_objects, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    # Call is made from mobile device
    if not ProjectManager.objects.filter(manager_key=manager_key).exists():
        return Response(data=messages.no_record_found, status=status.HTTP_404_NOT_FOUND)

    project_manager_object = ProjectManager.objects.filter(manager_key=manager_key).first()
    serializer = ProjectManagerSerializer(
        instance=project_manager_object, data={}, context={"project_augmented": True}, many=False, partial=True
    )

    # Validation is required to get data from serializer
    if not serializer.is_valid():  # pragma: no cover
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(data=serializer.data, status=status.HTTP_200_OK)


def post_patch(request):
    """
    Register a project manager with an optional set of project identifiers
    """
    manager_key = request.data.get("manager_key", None)
    email = request.data.get("email", None)
    project_ids = request.data.get("projects", [])

    if email is None:
        return Response(data=messages.invalid_query, status=status.HTTP_400_BAD_REQUEST)

    project_manager_object = ProjectManager.objects.filter(pk=manager_key).first()

    # Use the instance parameter to update the existing article or create a new one
    project_manager = {"manager_key": manager_key, "email": email, "projects": project_ids}
    serializer = ProjectManagerSerializer(instance=project_manager_object, data=project_manager)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()

    return Response(data=serializer.data, status=status.HTTP_200_OK)


def delete(request):
    """Delete project manager"""
    jwt_token = get_jwt_auth_token(request)
    if not is_valid_jwt_token(jwt_encrypted_token=jwt_token):
        return Response(data=messages.access_denied, status=status.HTTP_403_FORBIDDEN)

    manager_key = request.GET.get("manager_key", None)

    if manager_key is None:
        return Response(data=messages.invalid_query, status=status.HTTP_400_BAD_REQUEST)

    # remove project manager from database
    ProjectManager.objects.filter(manager_key=manager_key).delete()
    return Response(data="Project manager removed", status=status.HTTP_200_OK)
