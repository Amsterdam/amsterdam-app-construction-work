""" Views for ingestion routes """
import json
from datetime import datetime

from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from construction_work.api_messages import Messages
from construction_work.generic_functions.generic_logger import Logger
from construction_work.generic_functions.is_authorized import IsAuthorized
from construction_work.models import Article, Project
from construction_work.serializers import ArticleSerializer, ProjectCreateSerializer, ProjectDetailsSerializer
from construction_work.swagger.swagger_views_ingestion import as_garbage_collector

message = Messages()
logger = Logger()


@swagger_auto_schema(**as_garbage_collector)
@api_view(["POST"])
@IsAuthorized
def garbage_collector(request):
    """Garbage collector"""
    raw_data = request.data
    data = json.loads(raw_data)

    etl_epoch_string = data.get("etl_epoch_string")
    etl_epoch = datetime.strptime(etl_epoch_string, "%Y-%m-%d %H:%M:%S.%f")
    project_foreign_ids = data.get("project_ids", [])
    article_foreign_ids = data.get("article_ids", [])

    # Skeleton status report
    gc_status = {"projects": {"active": 0, "inactive": 0}, "articles": {"deleted": 0, "active": 0}}

    # Update last_seen and active state for all projects
    projects = Project.objects.all()
    for project in projects:
        if project.project_id in project_foreign_ids:
            serializer = ProjectCreateSerializer(project, data={"active": False}, partial=True)
            gc_status["projects"]["inactive"] += 1
        else:
            serializer = ProjectCreateSerializer(project, data={"last_seen": etl_epoch, "active": True}, partial=True)
            gc_status["projects"]["active"] += 1

        # Check if the data is valid and save the changes
        if not serializer.is_valid():
            Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

    # Remove all un-seen articles from database
    Article.objects.filter(foreign_id__in=article_foreign_ids).delete()
    gc_status["articles"]["deleted"] = len(article_foreign_ids)
    gc_status["articles"]["active"] = Article.objects.all().count()

    # Cleanup inactive projects
    five_days_ago = timezone.now() - timezone.timedelta(days=5)
    Project.objects.filter(last_seen__lt=five_days_ago, active=False).delete()

    # Return Response
    return Response(gc_status, status=200)


@IsAuthorized
@api_view(["GET", "POST"])
def iprox_project(request):
    if request.method == "GET":
        return iprox_project_get()
    if request.method == "POST":
        return iprox_project_post(request)


def iprox_project_get():
    projects = list(Project.objects.all().values_list("project_id", "modification_date"))
    result = {str(x[0]): {"modification_date": str(x[1])} for x in projects}
    return Response(result, status=status.HTTP_200_OK)


def iprox_project_post(request):
    """View for directly importing raw iprox data"""
    iprox_raw_data = request.data
    iprox_data = json.loads(iprox_raw_data)

    project_id = iprox_data.get("id")
    title_and_subtitle = iprox_data.get("title", "").split(": ")
    title = title_and_subtitle[0]
    subtitle = None if len(title_and_subtitle) == 1 else title_and_subtitle[1]

    project_instance = Project.objects.filter(project_id=project_id).first()

    project_data = {
        "title": title,
        "subtitle": subtitle,
        "sections": iprox_data.get("sections"),
        "contacts": iprox_data.get("contacts"),
        "timeline": iprox_data.get("timeline"),
        "image": iprox_data.get("image"),
        "images": iprox_data.get("images"),
        "url": iprox_data.get("url"),
        "project_id": iprox_data.get("id"),
        "creation_date": iprox_data.get("created"),
        "modification_date": iprox_data.get("modified"),
        "publication_date": iprox_data.get("publicationDate"),
        "expiration_date": iprox_data.get("expirationDate"),
    }

    # Use the instance parameter to update the existing article or create a new one
    serializer = ProjectCreateSerializer(instance=project_instance, data=project_data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@IsAuthorized
@api_view(["GET", "POST"])
def iprox_article(request):
    if request.method == "GET":
        return iprox_article_get()
    if request.method == "POST":
        return iprox_article_post(request)


def iprox_article_get():
    articles = list(Article.objects.all().values_list("foreign_id", "modification_date"))
    result = {str(x[0]): {"modification_date": str(x[1])} for x in articles}
    return Response(result, status=status.HTTP_200_OK)


def iprox_article_post(request):
    """View for directly importing raw iprox data"""
    iprox_data_raw = request.data
    iprox_data = json.loads(iprox_data_raw)

    foreign_id = iprox_data.get("id")
    project_ids_iprox = [Project.objects.get(project_id=x) for x in iprox_data.get("projectIds")]
    project_ids = [x.pk for x in project_ids_iprox]

    article_instance = Article.objects.filter(foreign_id=foreign_id).first()
    
    article_data = {
        "foreign_id": iprox_data.get("id"),
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
    serializer = ArticleSerializer(instance=article_instance, data=article_data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)
