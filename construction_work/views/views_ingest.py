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


@IsAuthorized
@api_view(["POST"])
def project(request):
    """Create or update a project"""
    data = request.data
    project_id = data.get("project_id")
    _project = Project.objects.filter(pk=project_id).first()

    data["last_seen"] = datetime.now()
    serializer = ProjectCreateSerializer(instance=_project, data=data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()

    return Response(serializer.data, status=status.HTTP_200_OK)


@IsAuthorized
@api_view(["GET", "POST", "DELETE"])
def article(request):
    """Article ingestion point (news and roadworks)"""
    try:
        data = dict(request.data)
        data["active"] = True
        _type = data["type"]
        _project = Project.objects.filter(pk=data.get("project_identifier")).first()
        news_item_object = Article.objects.filter(
            identifier=data.get("identifier"), project_identifier=_project
        ).first()
        if news_item_object is None:
            data["project_identifier"] = _project
            news_item_object = Article(**data)  # Update last scrape time is done implicitly
            news_item_object.save()
            return Response({"status": True, "result": f"{_type} item saved"}, status=200)

        # Else...
        data["last_seen"] = datetime.now()  # Update last scrape time
        Article.objects.filter(identifier=data.get("identifier"), project_identifier=_project).update(**data)
        return Response({"status": True, "result": f"{_type} item updated"}, status=200)
    except Exception as error:
        logger.error("ingest/news: {error}".format(error=error))
        return Response({"status": False, "result": str(error)}, status=500)


@swagger_auto_schema(**as_garbage_collector)
@api_view(["GET"])
@IsAuthorized
def garbage_collector(request):
    """Garbage collector"""
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

    title_and_subtitle = iprox_data.get("title", "").split(": ")
    title = title_and_subtitle[0]
    subtitle = "" if len(title_and_subtitle) == 1 else title_and_subtitle[1]

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

    serializer = ProjectCreateSerializer(data=project_data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_200_OK)


@IsAuthorized
@api_view(["POST"])
def iprox_article(request):
    """View for directly importing raw iprox data"""
    iprox_data = request.data

    article_data = {
        "article_id": iprox_data.get("id"),
        "projects": iprox_data.get("projectIds"),
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

    serializer = ArticleSerializer(data=article_data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_200_OK)
