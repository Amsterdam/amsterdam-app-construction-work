""" Views for CRUD a project-manager and assign projects
"""

from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from construction_work.api_messages import Messages
from construction_work.generic_functions.is_authorized import IsAuthorized, get_jwt_auth_token, is_valid_jwt_token
from construction_work.models import Project, ProjectManager
from construction_work.serializers import ProjectManagerSerializer
from construction_work.swagger.swagger_views_project_manager import (as_project_manager_delete, as_project_manager_get,
                                                                     as_project_manager_post_patch)

messages = Messages()


@swagger_auto_schema(**as_project_manager_post_patch)
@swagger_auto_schema(**as_project_manager_delete)
@swagger_auto_schema(**as_project_manager_get)
@api_view(["GET", "POST", "PATCH", "DELETE"])
@IsAuthorized
def crud(request):
    """Get project manager(s). Optionally filter by id"""
    if request.method == "GET":
        data = get(request)
        return Response(data["result"], status=data["status"])

    if request.method in ["POST", "PATCH"]:
        data = post_patch(request)
        return Response(data["result"], status=data["status"])

    # request.method  == 'DELETE'
    data = delete(request)
    return Response(data["result"], status=data["status"])


def get(request):
    """Get one or all project managers from database"""
    identifier = request.GET.get("id", None)
    if identifier is None:
        jwt_token = get_jwt_auth_token(request)
        if is_valid_jwt_token(jwt_encrypted_token=jwt_token):
            project_manager_objects = ProjectManager.objects.all()
            serializer = ProjectManagerSerializer(project_manager_objects, many=True)
            return {
                "result": {"status": True, "result": serializer.data},
                "status": 200,
            }
        return {
            "result": {"status": True, "result": messages.access_denied},
            "status": 403,
        }

    if not ProjectManager.objects.filter(pk=identifier).exists():
        return {
            "result": {"status": False, "result": messages.no_record_found},
            "status": 404,
        }

    project_manager_object = ProjectManager.objects.filter(pk=identifier).first()

    data = ProjectManagerSerializer(project_manager_object, many=False).data
    active_projects = []
    for identifier in data["projects"]:
        project = Project.objects.filter(pk=identifier, active=True).first()
        if project is not None:
            active_projects.append(
                {
                    "identifier": identifier,
                    "images": project.images,
                    "subtitle": project.subtitle,
                    "title": project.title,
                }
            )
    data["projects"] = active_projects
    return {"result": {"status": True, "result": [data]}, "status": 200}


def post_patch(request):
    """
    Register a project manager with an optional set of project identifiers
    """
    identifier = request.data.get("identifier", None)
    email = request.data.get("email", None)
    projects = request.data.get("projects", [])

    if email is None:
        return {
            "result": {"status": False, "result": messages.invalid_query},
            "status": 422,
        }

    for project in projects:
        if Project.objects.filter(pk=project).first() is None:
            return {
                "result": {"status": False, "result": messages.no_record_found},
                "status": 404,
            }

    project_manager_object = ProjectManager.objects.filter(Q(pk=identifier) | Q(email=email)).first()

    # New record
    if project_manager_object is None:
        try:
            project_manager_object = ProjectManager(identifier=identifier, email=email, projects=projects)
            project_manager_object.save()
            return {
                "result": {
                    "status": True,
                    "result": "Project manager created",
                    "identifier": project_manager_object.identifier,
                },
                "status": 200,
            }
        except Exception as error:
            return {"result": {"status": False, "result": str(error)}, "status": 422}

    # Update existing record
    else:
        ProjectManager.objects.filter(identifier=identifier).update(
            identifier=identifier, email=email, projects=projects
        )

    return {
        "result": {"status": True, "result": "Project manager updated"},
        "status": 200,
    }


def delete(request):
    """Delete project manager"""
    identifier = request.GET.get("id", None)
    if identifier is None:
        return {
            "result": {"status": False, "result": messages.invalid_query},
            "status": 422,
        }

    # remove project manager from database
    ProjectManager.objects.filter(pk=identifier).delete()
    return {
        "result": {"status": True, "result": "Project manager removed"},
        "status": 200,
    }
