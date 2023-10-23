# pylint: disable=unnecessary-lambda-assignment,expression-not-assigned
""" Views for iprox project pages """
import json
import urllib.parse
from datetime import datetime, timedelta
from math import ceil
from typing import List

import requests
from django.db.models import Max, BooleanField, Case, OuterRef, Subquery, Value, When
from django.db.models.functions import Coalesce
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from construction_work.api_messages import Messages
from construction_work.generic_functions.distance import GeoPyDistance
from construction_work.generic_functions.memoize import Memoize
from construction_work.generic_functions.request_must_come_from_app import (
    RequestMustComeFromApp,
)
from construction_work.generic_functions.static_data import (
    DEFAULT_ARTICLE_MAX_AGE,
    StaticData,
)
from construction_work.generic_functions.text_search import TextSearch
from construction_work.models import Article, Project, WarningMessage
from construction_work.models.device import Device
from construction_work.serializers import (
    ArticleSerializer,
    DeviceSerializer,
    ProjectDetailsSerializer,
    ProjectListSerializer,
    ProjectSerializer,
    WarningMessagePublicSerializer,
)
from construction_work.swagger.swagger_views_iprox_projects import (
    as_project_details,
    as_projects,
    as_projects_follow_delete,
    as_projects_follow_post,
    as_projects_followed_articles,
)
from construction_work.swagger.swagger_views_search import as_search

message = Messages()
memoize = Memoize(ttl=300, max_items=128)

FollowedProject = None


def create_next_previous_links(request, pagination):
    """Pagination defaults"""
    path_info = request.META.get("PATH_INFO")
    http_prefix = "https://" if request.is_secure() else "http://"
    http_host = request.META.get("HTTP_HOST", "localhost")
    host = http_prefix + http_host + path_info
    page_size = pagination["size"]
    links = {"self": {"href": host}}
    if pagination["number"] < pagination["totalPages"]:
        _next = str(pagination["number"] + 1)
        links["next"] = {"href": f"{host}?page={_next}&page_size={page_size}"}
    if pagination["number"] > 1:
        previous = str(pagination["number"] - 1)
        links["previous"] = {"href": f"{host}?page={previous}&page_size={page_size}"}
    return links


def search(model, request):
    """Pagination defaults"""
    text = request.GET.get("text", None)
    query_fields = request.GET.get("query_fields", "")
    fields = request.GET.get("fields", None)
    page_size = int(request.GET.get("page_size", 10))
    page = int(request.GET.get("page", 1)) - 1

    # Get Model fields
    model_fields = [x.name for x in model._meta.get_fields()]

    if text is None or len(text) < 3:
        return Response({"status": False, "result": message.invalid_query}, status=422)
    if len([x for x in query_fields.split(",") if x not in model_fields]) > 0:
        return Response(
            {"status": False, "result": message.no_such_field_in_model}, status=422
        )
    if (
        fields is not None
        and len([x for x in fields.split(",") if x not in model_fields]) > 0
    ):
        return Response(
            {"status": False, "result": message.no_such_field_in_model}, status=422
        )

    text_search = TextSearch(
        model, text, query_fields, return_fields=fields, page_size=page_size, page=page
    )
    result = text_search.search()
    links = create_next_previous_links(request, result["page"])
    return Response(
        {
            "status": True,
            "result": result["result"],
            "page": result["page"],
            "_links": links,
        },
        status=200,
    )


def address_to_gps(address):
    """Convert address to GPS info via API call"""
    apis = StaticData.urls()
    url = "{api}{address}".format(
        api=apis["address_to_gps"], address=urllib.parse.quote_plus(address)
    )
    result = requests.get(url=url, timeout=1)
    data = json.loads(result.content)
    if len(data["results"]) == 1:
        lon = data["results"][0]["centroid"][0]
        lat = data["results"][0]["centroid"][1]
        return lat, lon
    return None, None


def get_distance(project_data, lat, lon):
    """Calculate distance from app-users-address to project (python based). Efficiency: ~0.08s for 304 projects"""
    if lat is not None and lon is not None:
        cords_1 = (float(lat), float(lon))
        for project in project_data:
            gps_data = project.get("coordinates", (None, None))

            cords_2 = (gps_data["lat"], gps_data["lon"])
            if (0, 0) == cords_2:
                cords_2 = (None, None)
            distance = GeoPyDistance(cords_1, cords_2)
            project["meter"] = distance.meter
            project["strides"] = distance.strides

    return project_data


@swagger_auto_schema(**as_projects)
@api_view(["GET"])  # keep cached result for 5 minutes in memory
def projects(request):
    """
    Get a list of all projects. Narrow down by query param: project-type
    """

    device_id = request.META.get("HTTP_DEVICEID", None)
    if device_id is None:
        return Response(data=message.invalid_headers, status=status.HTTP_400_BAD_REQUEST)

    # @memoize
    def _fetch_projects(device_id):
        # Get query parameters
        lat = request.GET.get("lat", None)
        lon = request.GET.get("lon", None)
        address = request.GET.get("address", None)

        # NOTE: is 3 days too little, users will miss many article updates
        articles_max_age = int(
            request.GET.get("articles_max_age", 3)
        ) # Max days since publication date

        # Convert address into GPS data. Note: This should never happen, the device should already
        if address is not None:
            if lat is None or lon is None:
                lat, lon = address_to_gps(address)

        device = Device.objects.filter(device_id=device_id).first()
        if device is None:
            device_serializer = DeviceSerializer(data={"device_id": device_id})
            if not device_serializer.is_valid():
                return Response(
                    device_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            device = device_serializer.save()

        # Sort followed projects by project with most recent article
        projects_followed_by_device_qs = device.followed_projects.all().annotate(
            latest_publication_date=Max("article__publication_date")
        ).order_by("-latest_publication_date")
        projects_followed_by_device = list(projects_followed_by_device_qs)

        def calculate_distance(project: Project, lat, lon):
            given_cords = (float(lat), float(lon))

            if project.coordinates is not None:
                project_cords = (project.coordinates["lat"], project.coordinates["lon"])
            else:
                project_cords = (None, None)

            distance = GeoPyDistance(given_cords, project_cords)
            if distance.meter is None:
                return float("inf")
            return distance.meter

        all_other_projects_qs = Project.objects.exclude(pk__in=projects_followed_by_device_qs)

        if lat is not None and lon is not None:
            # Sort remaining projects by distance from given coordinates
            all_other_projects = sorted(
                all_other_projects_qs,
                key=lambda project: calculate_distance(project, lat, lon),
            )
        else:
            # Sort projects by project with most recent article
            all_other_projects_qs = all_other_projects_qs.annotate(
                latest_publication_date=Max("article__publication_date")
            ).order_by("-latest_publication_date")
            all_other_projects = list(all_other_projects_qs)

        all_projects = []
        all_projects.extend(projects_followed_by_device)
        all_projects.extend(all_other_projects)

        context = {
            "device_id": device_id,
            "articles_max_age": articles_max_age,
        }
        serializer = ProjectListSerializer(instance=all_projects, many=True, context=context)
        
        return serializer.data

    # Call _fetch_projects
    result = _fetch_projects(device_id)

    # Set paginated result and calculate number of pages
    page_size = int(request.GET.get("page_size", 10))
    page = int(request.GET.get("page", 1)) - 1
    start_index = page * page_size
    stop_index = page * page_size + page_size
    paginated_result = result[start_index:stop_index]
    pages = int(ceil(len(result) / float(page_size)))
    pagination = {
        "number": page + 1,
        "size": page_size,
        "totalElements": len(result),
        "totalPages": pages,
    }
    links = create_next_previous_links(request, pagination)

    return Response(
        {
            "result": paginated_result,
            "page": pagination,
            "_links": links,
        },
        status=status.HTTP_200_OK,
    )


@swagger_auto_schema(**as_search)
@api_view(["GET"])
def projects_search(request):
    """Search project"""
    model = Project
    return search(model, request)


@swagger_auto_schema(**as_project_details)
@api_view(["GET"])
def project_details(request):
    """
    Get details for a project by identifier
    """
    device_id = request.META.get("HTTP_DEVICEID", None)
    if device_id is None:
        return Response(data=message.invalid_headers, status=status.HTTP_400_BAD_REQUEST)
    
    foreign_id = request.GET.get("foreign_id", None)
    if foreign_id is None:
        return Response(data=message.invalid_query, status=status.HTTP_400_BAD_REQUEST)

    articles_max_age = request.GET.get("articles_max_age", None)
    if articles_max_age is not None and articles_max_age.isdigit() is False:
        return Response(data=message.invalid_query, status=status.HTTP_400_BAD_REQUEST)

    if articles_max_age is None:
        articles_max_age = DEFAULT_ARTICLE_MAX_AGE
    else:
        articles_max_age = int(articles_max_age)

    lat = request.GET.get("lat", None)
    lon = request.GET.get("lon", None)
    address = request.GET.get("address", None)  # akkerstraat%2014 -> akkerstraat 14
    if address is not None:
        apis = StaticData.urls()
        url = "{api}{address}".format(
            api=apis["address_to_gps"], address=urllib.parse.quote_plus(address)
        )
        result = requests.get(url=url, timeout=1)
        data = json.loads(result.content)
        if len(data["results"]) == 1:
            lon = data["results"][0]["centroid"][0]
            lat = data["results"][0]["centroid"][1]

    project_obj = Project.objects.filter(foreign_id=foreign_id, active=True).first()
    if project_obj is None:
        return Response(
            data=message.no_record_found,
            status=status.HTTP_404_NOT_FOUND,
        )

    # Only create device when all required paramaters are provided 
    device = Device.objects.filter(device_id=device_id).first()
    if device is None:
        device_serializer = DeviceSerializer(data={"device_id": device_id})
        if not device_serializer.is_valid():
            return Response(
                device_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        device = device_serializer.save()

    project_serializer = ProjectDetailsSerializer(
        instance=project_obj,
        partial=True,
        data={},
        context={
            "lat": lat,
            "lon": lon,
            "device_id": device.device_id,
            "articles_max_age": articles_max_age,
        },
    )
    # Validation is required to get data from serializer
    if not project_serializer.is_valid():
        return Response(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(data=project_serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(**as_projects_follow_post)
@swagger_auto_schema(**as_projects_follow_delete)
@api_view(["POST", "DELETE"])
@RequestMustComeFromApp
def projects_follow(request):
    """Subscribe or un-subscribe from project"""
    device_id = request.META.get("HTTP_DEVICEID", None)
    if device_id is None:
        return Response(
            {"status": False, "result": message.invalid_headers},
            status=status.HTTP_400_BAD_REQUEST,
        )

    foreign_id = request.data.get("foreign_id", None)
    if foreign_id is None:
        return Response(
            {"status": False, "result": message.invalid_parameters},
            status=status.HTTP_400_BAD_REQUEST,
        )

    project = Project.objects.filter(foreign_id=foreign_id).first()
    if project is None:
        return Response(
            {"status": False, "result": message.no_record_found},
            status=status.HTTP_404_NOT_FOUND,
        )

    device = Device.objects.filter(device_id=device_id).first()

    # Follow flow
    if request.method == "POST":
        # TODO: if device is not none: add project to followed projects of device

        if device is None:
            serializer = DeviceSerializer(
                data={"device_id": device_id, "followed_projects": [project.pk]}
            )
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    # Unfollow flow
    # request.method == 'DELETE'
    if device is None:
        return Response(
            {"status": False, "result": message.no_record_found},
            status=status.HTTP_404_NOT_FOUND,
        )

    device.followed_projects.remove(project)
    return Response(
        {"status": False, "result": "Subscription removed"}, status=status.HTTP_200_OK
    )


# TODO: change view when article gets remodelled
# TODO: write unit tests
@swagger_auto_schema(**as_projects_followed_articles)
@api_view(["GET"])
def projects_followed_articles(request):
    """Get articles for followed projects"""
    device_id = request.META.get("HTTP_DEVICEID", None)
    article_max_age = int(request.GET.get("article-max-age", 3))
    if device_id is None:
        return Response(
            {"status": False, "result": message.invalid_headers},
            status=status.HTTP_400_BAD_REQUEST,
        )

    device = Device.objects.filter(device_id=device_id).first()
    if device is None:
        return Response(
            {"status": False, "result": message.no_record_found},
            status=status.HTTP_404_NOT_FOUND,
        )

    followed_projects: List[Project] = device.followed_projects.all()
    project_identifiers = [x.foreign_id for x in followed_projects]

    result = {}
    # Get recent articles
    for project_id in project_identifiers:
        start_date = datetime.now() - timedelta(days=article_max_age)
        end_date = datetime.now()
        start_date_str = start_date.strftime("%Y-%m-%d")
        news_articles_all = list(
            Article.objects.filter(project_identifier=project_id).all()
        )
        serializer_news = ArticleSerializer(news_articles_all, many=True)
        news_articles = [
            x["identifier"]
            for x in serializer_news.data
            if x["publication_date"] >= start_date_str
        ]
        warning_articles = list(
            WarningMessage.objects.filter(
                project_identifier=project_id,
                publication_date__range=[start_date, end_date],
            ).all()
        )
        result[project_id] = news_articles + [x.identifier for x in warning_articles]

    return Response({"status": True, "result": {"projects": result}})
