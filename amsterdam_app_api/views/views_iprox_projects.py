# pylint: disable=unnecessary-lambda-assignment,expression-not-assigned
""" Views for iprox project pages """
import json
import urllib.parse
from datetime import datetime, timedelta
from math import ceil

import requests
from django.db import IntegrityError
from django.db.models import BooleanField, Case, OuterRef, Subquery, Value, When
from django.db.models.functions import Coalesce
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from amsterdam_app_api.api_messages import Messages
from amsterdam_app_api.GenericFunctions.Distance import GeoPyDistance
from amsterdam_app_api.GenericFunctions.Memoize import Memoize
from amsterdam_app_api.GenericFunctions.RequestMustComeFromApp import RequestMustComeFromApp
from amsterdam_app_api.GenericFunctions.StaticData import StaticData
from amsterdam_app_api.GenericFunctions.TextSearch import TextSearch
from amsterdam_app_api.models import FollowedProjects, News, ProjectDetails, Projects, WarningMessages
from amsterdam_app_api.serializers import NewsSerializer, ProjectDetailsSerializer, WarningMessagesExternalSerializer
from amsterdam_app_api.swagger.swagger_views_iprox_projects import (
    as_project_details,
    as_projects,
    as_projects_follow_delete,
    as_projects_follow_post,
    as_projects_followed_articles,
)
from amsterdam_app_api.swagger.swagger_views_search import as_search

message = Messages()
memoize = Memoize(ttl=300, max_items=128)


def set_next_previous_links(request, result):
    """Pagination defaults"""
    path_info = request.META.get("PATH_INFO")
    http_prefix = "https://" if request.is_secure() else "http://"
    http_host = request.META.get("HTTP_HOST", "localhost")
    host = http_prefix + http_host + path_info
    links = {"self": {"href": host}}
    if result["number"] < result["totalPages"]:
        _next = str(result["number"] + 1)
        links["next"] = {"href": host + "?page=" + _next}
    if result["number"] > 1:
        previous = str(result["number"] - 1)
        links["previous"] = {"href": host + "?page=" + previous}
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
        return Response({"status": False, "result": message.no_such_field_in_model}, status=422)
    if fields is not None and len([x for x in fields.split(",") if x not in model_fields]) > 0:
        return Response({"status": False, "result": message.no_such_field_in_model}, status=422)

    text_search = TextSearch(model, text, query_fields, return_fields=fields, page_size=page_size, page=page)
    result = text_search.search()
    links = set_next_previous_links(request, result["page"])
    return Response({"status": True, "result": result["result"], "page": result["page"], "_links": links}, status=200)


def address_to_gps(address):
    """Convert address to GPS info via API call"""
    apis = StaticData.urls()
    url = "{api}{address}".format(api=apis["address_to_gps"], address=urllib.parse.quote_plus(address))
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

    # @memoize
    def _fetch_projects(deviceid):
        # Get query parameters
        lat = request.GET.get("lat", None)
        lon = request.GET.get("lon", None)
        address = request.GET.get("address", None)
        articles_max_age = int(request.GET.get("articles_max_age", 3))  # Max days since publication date

        # Convert address into GPS data. Note: This should never happen, the device should already
        if address is not None:
            if lat is None or lon is None:
                lat, lon = address_to_gps(address)

        # For each project in the database get the following data:
        # "identifier", "images", "publication_date", "subtitle", "title", "followed", "coordinates"

        followed_projects = FollowedProjects.objects.filter(projectid=OuterRef("identifier"), deviceid=deviceid).values(
            "projectid"
        )

        coordinates_projects = ProjectDetails.objects.filter(identifier=OuterRef("identifier")).values("coordinates")

        _projects = list(
            Projects.objects.filter(active=True)
            .annotate(
                followed=Case(
                    When(identifier__in=Subquery(followed_projects), then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                ),
                coordinates=Subquery(coordinates_projects[:1]),
            )
            .annotate(followed=Coalesce("followed", Value(False)))
            .values("identifier", "images", "publication_date", "subtitle", "title", "followed", "coordinates")
            .all()
        )

        # Get news and warning articles from the last 'articles_max_age' days
        start_date = datetime.now() - timedelta(days=articles_max_age)
        end_date = datetime.now()
        start_date_str = start_date.strftime("%Y-%m-%d")

        news_articles = list(
            News.objects.filter(publication_date__gte=start_date_str)
            .values("project_identifier", "identifier", "publication_date")
            .order_by("publication_date")
            .all()
        )

        warning_articles = list(
            WarningMessages.objects.filter(publication_date__range=[start_date, end_date])
            .values("project_identifier", "identifier", "publication_date")
            .order_by("publication_date")
            .all()
        )

        articles = news_articles + warning_articles

        # Add articles to 'projects', sorted descending on publication_date
        for project in _projects:
            project["recent_articles"] = sorted(
                [
                    {"identifier": article["identifier"], "publication_date": article["publication_date"]}
                    for article in articles
                    if article["project_identifier"] == project["identifier"]
                ],
                key=lambda x: x["publication_date"],
                reverse=True,
            )

        # Calculate distance from app-users-address to project (python based)
        # efficiency: ~0.08s for 304 projects
        _projects = get_distance(_projects, lat, lon)

        # Sort projects Algorithm (articles have been pre-sorted (desc) by publication date):

        # Divide the projects in two lists, followed projects and all others
        data = {"follow": [], "others": []}
        [data["follow"].append(x) if x["followed"] is True else data["others"].append(x) for x in _projects]

        # Next: → Sort the followed projects by most recent articles, (data["follow"] can be an empty list)
        lambda_expression = (
            lambda x: x["recent_articles"][0]["publication_date"]
            if "recent_articles" in x and len(x["recent_articles"]) > 0
            else ""
        )
        if len(data["follow"]) != 0:
            data["follow"] = sorted(data["follow"], key=lambda_expression, reverse=True)

        # Next: → If the user has not provided an address, sort on publication date of most recent news-article
        if lat is None and lon is None:
            data["others"] = sorted(data["others"], key=lambda_expression, reverse=True)
        # Else: → If the user has provided an address, sort on increasing distance between address and project
        else:
            # Magic number "10000000" if meter is None, use a really high number...
            data["others"] = sorted(data["others"], key=lambda x: x["meter"] if x["meter"] else 10000000, reverse=False)

        # Next: → Concatenate the two lists and return the result
        return data["follow"] + data["others"]

    # Guard clause
    deviceid = request.META.get("HTTP_DEVICEID", None)
    if deviceid is None:
        return Response({"status": False, "result": message.invalid_headers}, status=422)

    # Call _fetch_projects
    result = _fetch_projects(deviceid)

    # Set paginated result and calculate number of pages
    page_size = int(request.GET.get("page_size", 10))
    page = int(request.GET.get("page", 1)) - 1
    start_index = page * page_size
    stop_index = page * page_size + page_size
    paginated_result = result[start_index:stop_index]
    pages = int(ceil(len(result) / float(page_size)))
    pagination = {"number": page + 1, "size": page_size, "totalElements": len(result), "totalPages": pages}
    links = set_next_previous_links(request, pagination)

    return Response({"status": True, "result": paginated_result, "page": pagination, "_links": links}, status=200)


@swagger_auto_schema(**as_search)
@api_view(["GET"])
def projects_search(request):
    """Search project"""
    model = Projects
    return search(model, request)


@swagger_auto_schema(**as_project_details)
@api_view(["GET"])
def project_details(request):
    """
    Get details for a project by identifier
    """
    deviceid = request.META.get("HTTP_DEVICEID", None)
    if deviceid is None:
        return Response({"status": False, "result": message.invalid_headers}, status=422)

    identifier = request.GET.get("id", None)
    if identifier is None:
        return Response({"status": False, "result": message.invalid_query}, status=422)

    articles_max_age = request.GET.get("articles_max_age", None)

    lat = request.GET.get("lat", None)
    lon = request.GET.get("lon", None)
    address = request.GET.get("address", None)  # akkerstraat%2014 -> akkerstraat 14
    if address is not None:
        apis = StaticData.urls()
        url = "{api}{address}".format(api=apis["address_to_gps"], address=urllib.parse.quote_plus(address))
        result = requests.get(url=url, timeout=1)
        data = json.loads(result.content)
        if len(data["results"]) == 1:
            lon = data["results"][0]["centroid"][0]
            lat = data["results"][0]["centroid"][1]

    project_object = ProjectDetails.objects.filter(pk=identifier, active=True).first()
    if project_object is None:
        return Response({"status": False, "result": message.no_record_found}, status=404)

    # Get followers
    count = FollowedProjects.objects.filter(projectid=identifier).count()
    followed = FollowedProjects.objects.filter(deviceid=deviceid, projectid=identifier).first()
    project_data = dict(ProjectDetailsSerializer(project_object, many=False).data)
    project_data["followers"] = count
    project_data["followed"] = bool(followed is not None)

    # Get distance
    project_data["meter"] = None
    project_data["strides"] = None
    if lat is not None and lon is not None:
        cords_1 = (float(lat), float(lon))
        cords_2 = (project_object.coordinates["lat"], project_object.coordinates["lon"])
        if None in cords_2:
            cords_2 = (None, None)
        elif (0, 0) == cords_2:
            cords_2 = (None, None)
        distance = GeoPyDistance(cords_1, cords_2)
        project_data["meter"] = distance.meter
        project_data["strides"] = distance.strides

    # Get recent articles
    if articles_max_age is not None:
        articles_max_age = int(articles_max_age)
        start_date = datetime.now() - timedelta(days=articles_max_age)
        end_date = datetime.now()
        start_date_str = start_date.strftime("%Y-%m-%d")
        news_articles_all = list(News.objects.filter(project_identifier=identifier, active=True).all())
        serializer_news = NewsSerializer(news_articles_all, many=True)
        news_articles = [x["identifier"] for x in serializer_news.data if x["publication_date"] >= start_date_str]
        warning_articles = list(
            WarningMessages.objects.filter(
                project_identifier=identifier, publication_date__range=[start_date, end_date]
            ).all()
        )
        serializer_warning = WarningMessagesExternalSerializer(warning_articles, many=True)
        project_data["recent_articles"] = news_articles + [x["identifier"] for x in serializer_warning.data]
    return Response({"status": True, "result": project_data}, status=200)


@swagger_auto_schema(**as_search)
@api_view(["GET"])
def project_details_search(request):
    """Search in project details"""
    model = ProjectDetails
    return search(model, request)


@swagger_auto_schema(**as_projects_follow_post)
@swagger_auto_schema(**as_projects_follow_delete)
@api_view(["POST", "DELETE"])
@RequestMustComeFromApp
def projects_follow(request):
    """Subscribe or un-subscribe from project"""
    deviceid = request.META.get("HTTP_DEVICEID", None)
    if deviceid is None:
        return Response({"status": False, "result": message.invalid_headers}, status=422)

    if request.method == "POST":
        project_id = request.data.get("project_id", None)
        if project_id is not None:
            project = ProjectDetails.objects.filter(identifier=project_id).first()
            if project is None:
                return Response({"status": False, "result": message.no_record_found}, status=404)
        try:
            follow_project = FollowedProjects(projectid=project_id, deviceid=deviceid)
            follow_project.save()
        except IntegrityError:  # Double request with same data, discard...
            pass
        return Response({"status": False, "result": "Subscription added"}, status=200)

    # request.method == 'DELETE'
    project_id = request.data.get("project_id", None)
    follow_project = FollowedProjects.objects.filter(projectid=project_id, deviceid=deviceid).first()
    if follow_project is not None:
        follow_project.delete()
    return Response({"status": False, "result": "Subscription removed"}, status=200)


@swagger_auto_schema(**as_projects_followed_articles)
@api_view(["GET"])
def projects_followed_articles(request):
    """Get articles for followed projects"""
    deviceid = request.META.get("HTTP_DEVICEID", None)
    article_max_age = int(request.GET.get("article-max-age", 3))
    if deviceid is None:
        return Response({"status": False, "result": message.invalid_headers}, status=422)

    followed_projects = list(FollowedProjects.objects.filter(deviceid=deviceid).values("projectid").all())
    project_identifiers = [x["projectid"] for x in followed_projects]

    result = {}
    # Get recent articles
    for identifier in project_identifiers:
        start_date = datetime.now() - timedelta(days=article_max_age)
        end_date = datetime.now()
        start_date_str = start_date.strftime("%Y-%m-%d")
        news_articles_all = list(News.objects.filter(project_identifier=identifier).all())
        serializer_news = NewsSerializer(news_articles_all, many=True)
        news_articles = [x["identifier"] for x in serializer_news.data if x["publication_date"] >= start_date_str]
        warning_articles = list(
            WarningMessages.objects.filter(
                project_identifier=identifier, publication_date__range=[start_date, end_date]
            ).all()
        )
        result[identifier] = news_articles + [x.identifier for x in warning_articles]

    return Response({"status": True, "result": {"projects": result}})
