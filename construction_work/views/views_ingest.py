""" Views for ingestion routes """
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from construction_work.api_messages import Messages
from construction_work.generic_functions.generic_logger import Logger
from construction_work.generic_functions.is_authorized import IsAuthorized
from construction_work.models import Article, Project
from construction_work.serializers import ArticleCreateSerializer, ProjectSerializer
from construction_work.swagger.swagger_views_ingestion import (
    as_etl_article_post,
    as_etl_get,
    as_etl_project_post,
    as_garbage_collector,
)

message = Messages()
logger = Logger()


@swagger_auto_schema(**as_garbage_collector)
@api_view(["POST"])
@IsAuthorized
def garbage_collector(request):
    """Garbage collector"""
    data = request.data

    # Foreign ids not seen after ETL
    project_foreign_ids = data.get("project_ids", [])
    article_foreign_ids = data.get("article_ids", [])

    # Update last_seen and active state for all projects
    projects = Project.objects.all()
    initial_projects_count = projects.count()
    for project in projects:
        if project.foreign_id in project_foreign_ids:
            project.deactivate()
        else:
            project.save()

    # Remove all un-seen articles from database
    initial_article_count = Article.objects.all().count()
    Article.objects.filter(foreign_id__in=article_foreign_ids).delete()

    # Cleanup inactive projects
    five_days_ago = timezone.now() - timezone.timedelta(days=5)
    Project.objects.filter(last_seen__lt=five_days_ago, active=False).delete()

    # Set status
    gc_status = {
        "projects": {
            "active": Project.objects.filter(active=True).count(),
            "inactive": Project.objects.filter(active=False).count(),
            "deleted": initial_projects_count - Project.objects.all().count(),
            "count": Project.objects.all().count(),
        },
        "articles": {
            "deleted": initial_article_count - Article.objects.all().count(),
            "count": Article.objects.all().count(),
        },
    }

    # Return Response
    return Response(gc_status, status=status.HTTP_200_OK)


@swagger_auto_schema(**as_etl_get)
@swagger_auto_schema(**as_etl_project_post)
@IsAuthorized
@api_view(["GET", "POST"])
def etl_project(request):
    """Discriminate on request method"""
    if request.method == "GET":
        return etl_project_get()
    if request.method == "POST":
        return etl_project_post(request)
    return Response(data=None, status=status.HTTP_400_BAD_REQUEST)


def etl_project_get():
    """Get all project_id with their modification date"""
    projects = list(
        Project.objects.all().values_list("foreign_id", "modification_date")
    )
    result = {str(x[0]): {"modification_date": str(x[1])} for x in projects}
    return Response(result, status=status.HTTP_200_OK)


def etl_project_post(request):
    """Import etl data"""
    etl_iprox_data = request.data

    foreign_id = etl_iprox_data.get("foreign_id")
    title = etl_iprox_data.get("title", "")
    subtitle = etl_iprox_data.get("subtitle", "")

    project_instance = Project.objects.filter(foreign_id=foreign_id).first()

    project_data = {
        "title": title,
        "subtitle": subtitle,
        "sections": etl_iprox_data.get("sections"),
        "contacts": etl_iprox_data.get("contacts"),
        "timeline": etl_iprox_data.get("timeline"),
        "image": etl_iprox_data.get("image"),
        "images": etl_iprox_data.get("images"),
        "url": etl_iprox_data.get("url"),
        "foreign_id": foreign_id,
        "coordinates": etl_iprox_data.get("coordinates"),
        "creation_date": etl_iprox_data.get("created"),
        "modification_date": etl_iprox_data.get("modified"),
        "publication_date": etl_iprox_data.get("publicationDate"),
        "expiration_date": etl_iprox_data.get("expirationDate"),
    }

    # Use the instance parameter to update the existing article or create a new one
    serializer = ProjectSerializer(instance=project_instance, data=project_data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(**as_etl_get)
@swagger_auto_schema(**as_etl_article_post)
@IsAuthorized
@api_view(["GET", "POST"])
def etl_article(request):
    """Discriminate on request method"""
    if request.method == "GET":
        return etl_article_get()
    if request.method == "POST":
        return etl_article_post(request)
    return Response(data=None, status=status.HTTP_400_BAD_REQUEST)


def etl_article_get():
    """Get all article_id with their modification date"""
    articles = list(
        Article.objects.all().values_list("foreign_id", "modification_date")
    )
    result = {str(x[0]): {"modification_date": str(x[1])} for x in articles}
    return Response(result, status=status.HTTP_200_OK)


def etl_article_post(request):
    """Import etl data"""
    iprox_data = request.data

    article_foreign_id = iprox_data.get("foreign_id")
    project_foreign_ids = [
        Project.objects.get(foreign_id=x) for x in iprox_data.get("projectIds")
    ]
    project_ids = [x.pk for x in project_foreign_ids]

    article_instance = Article.objects.filter(foreign_id=article_foreign_id).first()

    article_data = {
        "foreign_id": article_foreign_id,
        "projects": project_ids,
        "title": iprox_data.get("title"),
        "intro": iprox_data.get("intro"),
        "body": iprox_data.get("body"),
        "image": iprox_data.get("image"),
        "type": iprox_data.get("type"),
        "url": iprox_data.get("url"),
        "creation_date": iprox_data.get("created"),
        "modification_date": iprox_data.get("modified"),
        "publication_date": iprox_data.get("publicationDate"),
        "expiration_date": iprox_data.get("expirationDate"),
    }

    # Use the instance parameter to update the existing article or create a new one
    serializer = ArticleCreateSerializer(instance=article_instance, data=article_data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)
