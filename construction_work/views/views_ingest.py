""" Views for ingestion routes """
import json
from datetime import datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from construction_work.api_messages import Messages
from construction_work.garbage_collector.garbage_collector import GarbageCollector
from construction_work.generic_functions.generic_logger import Logger
from construction_work.generic_functions.is_authorized import IsAuthorized
from construction_work.models import Article, Project
from construction_work.serializers import ArticleSerializer, ProjectCreateSerializer
from construction_work.swagger.swagger_views_ingestion import as_garbage_collector

message = Messages()
logger = Logger()


@swagger_auto_schema(**as_garbage_collector)
@api_view(["GET"])
@IsAuthorized
def garbage_collector(request):
    """Garbage collector"""

    # NOTE: Wellicht autonoom maken via een 'scrape' table met een last-scraped erin...
    date = request.GET.get("date", str(datetime.now()))
    last_scrape_time = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
    collector = GarbageCollector(last_scrape_time=last_scrape_time)
    result = collector.collect_iprox()

    return Response({"status": True, "result": result}, status=200)


@IsAuthorized
@api_view(["POST"])
def iprox_project(request):
    """View for directly importing raw iprox data"""
    iprox_raw_data = request.data
    iprox_data = json.loads(iprox_raw_data)

    project_id = iprox_data.get("id")
    title_and_subtitle = iprox_data.get("title", "").split(": ")
    title = title_and_subtitle[0]
    subtitle = None if len(title_and_subtitle) == 1 else title_and_subtitle[1]

    # Try to get an article with the provided article_id
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
@api_view(["POST"])
def iprox_article(request):
    """View for directly importing raw iprox data"""
    iprox_data_raw = request.data
    iprox_data = json.loads(iprox_data_raw)

    article_id = iprox_data.get("id")
    project_ids_iprox = [Project.objects.get(project_id=x) for x in iprox_data.get("projectIds")]
    project_ids = [x.pk for x in project_ids_iprox]

    # Try to get an article with the provided article_id
    article_instance = Article.objects.filter(article_id=article_id).first()

    article_data = {
        "article_id": iprox_data.get("id"),
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
