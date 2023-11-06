# pylint: disable=unnecessary-lambda-assignment,expression-not-assigned
""" Views for iprox project pages """
import asyncio
from datetime import datetime, timedelta
from math import ceil

from django.db.models import Max
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from construction_work.api_messages import Messages
from construction_work.generic_functions.gps_utils import address_to_gps, get_distance
from construction_work.generic_functions.memoize import Memoize
from construction_work.generic_functions.project_utils import create_project_news_lookup, get_recent_articles_of_project
from construction_work.generic_functions.request_must_come_from_app import RequestMustComeFromApp
from construction_work.generic_functions.static_data import ARTICLE_MAX_AGE_PARAM, DEFAULT_ARTICLE_MAX_AGE
from construction_work.generic_functions.text_search import (
    MIN_QUERY_LENGTH,
    get_non_related_fields,
    search_text_in_model,
)
from construction_work.models import Article, Project, WarningMessage
from construction_work.models.device import Device
from construction_work.serializers import (
    ArticleMinimalSerializer,
    ArticleSerializer,
    DeviceSerializer,
    ProjectDetailsSerializer,
    ProjectListSerializer,
    WarningMessageMinimalSerializer,
    WarningMessagePublicSerializer,
)
from construction_work.swagger.swagger_views_iprox_projects import (
    as_project_details,
    as_project_follow_delete,
    as_project_follow_post,
    as_projects,
    as_projects_followed_articles,
    as_projects_search,
)

message = Messages()
memoize = Memoize(ttl=300, max_items=300)


def _paginate_data(request, data: list) -> dict:
    """Create pagination of data"""
    page = int(request.GET.get("page", 1)) - 1
    page_size = int(request.GET.get("page_size", 10))

    # Get uri from request
    absolute_uri = request.build_absolute_uri()
    uri = absolute_uri.split("?")[0]

    start_index = page * page_size
    stop_index = page * page_size + page_size
    paginated_result = data[start_index:stop_index]
    pages = int(ceil(len(data) / float(page_size)))

    pagination = {
        "number": page + 1,
        "size": page_size,
        "totalElements": len(data),
        "totalPages": pages,
    }

    # Get query parameters from request
    query_params = dict(request.query_params)
    query_params.pop("page", None)
    query_params.pop("page_size", None)

    query_params_str = ""
    for k, v in query_params.items():
        param_str = f"&{k}={v[0]}"
        query_params_str += param_str

    # Add link without pagination
    links = {"self": {"href": f"{uri}?{query_params_str}"}}

    # Add next page link, if available
    if pagination["number"] < pagination["totalPages"]:
        next_page = str(pagination["number"] + 1)
        links["next"] = {"href": f"{uri}?page={next_page}&page_size={page_size}{query_params_str}"}

    # Add previous page link, if available
    if pagination["number"] > 1:
        previous_page = str(pagination["number"] - 1)
        links["previous"] = {"href": f"{uri}?page={previous_page}&page_size={page_size}{query_params_str}"}

    return {
        "result": paginated_result,
        "page": pagination,
        "_links": links,
    }


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class InvalidQueryError(Exception):
    pass


class NoSuchFieldInModelError(Exception):
    pass


def search(model, text, query_fields, return_fields) -> list:
    """Search model using request parameters"""

    # Get all fields of given model
    model_fields = get_non_related_fields(model)

    # Text length has to be at least 3
    if text is None or len(text) < MIN_QUERY_LENGTH:
        raise InvalidQueryError(message.invalid_query)

    # Check if query_fields and return_field are not None
    if query_fields is None or return_fields is None:
        raise InvalidQueryError(message.invalid_query)

    # Check if given query fields are in model fields
    if query_fields is not None and len([x for x in query_fields.split(",") if x not in model_fields]) > 0:
        raise NoSuchFieldInModelError(message.no_such_field_in_model)

    # Check if given return fields are in model fields, if assigned
    if return_fields is not None and len([x for x in return_fields.split(",") if x not in model_fields]) > 0:
        raise NoSuchFieldInModelError(message.no_such_field_in_model)

    # Perform search
    result = search_text_in_model(model, text, query_fields, return_fields)
    return result


@swagger_auto_schema(**as_projects)
@api_view(["GET"])  # keep cached result for 5 minutes in memory
@RequestMustComeFromApp
def projects(request):
    """Get a list of all projects in specific order"""

    device_id = request.META.get("HTTP_DEVICEID", None)
    if device_id is None:
        return Response(data=message.invalid_headers, status=status.HTTP_400_BAD_REQUEST)

    lat = request.GET.get("lat", None)
    lon = request.GET.get("lon", None)
    address = request.GET.get("address", None)

    # NOTE: is 3 days too little, users will miss many article updates
    article_max_age = int(request.GET.get(ARTICLE_MAX_AGE_PARAM, 3))  # Max days since publication date

    @memoize
    def _fetch_projects(_device_id, _article_max_age, _lat, _lon, _address):
        # Convert address into GPS data. Note: This should never happen, the device should already
        if _address is not None and (_lat is None or _lon is None):
            _lat, _lon = address_to_gps(_address)

        # If we've never seen this device, create it lookup device in DB and use it...
        device = Device.objects.filter(device_id=_device_id).first()
        if device is None:
            device_serializer = DeviceSerializer(data={"device_id": _device_id})
            if not device_serializer.is_valid():
                return Response(device_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            device = device_serializer.save()

        # Sort followed projects by project with most recent article
        projects_followed_by_device_qs = (
            device.followed_projects.all()
            .annotate(latest_publication_date=Max("article__publication_date"))
            .order_by("-latest_publication_date")
        )
        projects_followed_by_device = list(projects_followed_by_device_qs)

        def calculate_distance(project: Project, _lat, _lon):
            given_cords = (float(_lat), float(_lon))

            if project.coordinates is not None:
                project_cords = (
                    project.coordinates.get("lat"),
                    project.coordinates.get("lon"),
                )
            else:
                project_cords = (None, None)

            meter, _ = get_distance(given_cords, project_cords)
            if meter is None:
                return float("inf")
            return meter

        all_other_projects_qs = Project.objects.exclude(pk__in=projects_followed_by_device_qs)

        if _lat is not None and _lon is not None:
            # Sort remaining projects by distance from given coordinates
            all_other_projects = sorted(
                all_other_projects_qs,
                key=lambda project: calculate_distance(project, _lat, _lon),
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

        project_news_mapping = create_project_news_lookup(all_projects, _article_max_age)

        context = {
            "device_id": _device_id,
            "lat": _lat,
            "lon": _lon,
            "project_news_mapping": project_news_mapping,
            "followed_projects": projects_followed_by_device,
        }
        serializer = ProjectListSerializer(instance=all_projects, many=True, context=context)
        return serializer.data

    # Create context for project list serializer
    serialized_data = _fetch_projects(device_id, article_max_age, lat, lon, address)

    # Paginate and return data
    paginated_data = _paginate_data(request, serialized_data)
    return Response(data=paginated_data, status=status.HTTP_200_OK)


@swagger_auto_schema(**as_projects_search)
@api_view(["GET"])
@RequestMustComeFromApp
def projects_search(request):
    """Search project"""
    text = request.GET.get("text", None)
    query_fields = request.GET.get("query_fields", None)
    return_fields = request.GET.get("fields", None)

    lat = request.GET.get("lat", None)
    lon = request.GET.get("lon", None)
    address = request.GET.get("address", None)
    if address is not None:
        lat, lon = address_to_gps(address)

    article_max_age = int(request.GET.get(ARTICLE_MAX_AGE_PARAM, 3))

    try:
        found_projects = search(Project, text, query_fields, return_fields)
    except InvalidQueryError as e:
        return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
    except NoSuchFieldInModelError as e:
        return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)

    project_news_mapping = create_project_news_lookup(found_projects, article_max_age)
    context = {
        "lat": lat,
        "lon": lon,
        "article_max_age": article_max_age,
        "project_news_mapping": project_news_mapping,
    }
    serializer = ProjectListSerializer(instance=found_projects, many=True, context=context)

    # Paginate result
    paginated_data = _paginate_data(request, serializer.data)

    return Response(
        data=paginated_data,
        status=status.HTTP_200_OK,
    )


@swagger_auto_schema(**as_project_details)
@api_view(["GET"])
@RequestMustComeFromApp
def project_details(request):
    """
    Get details for a project by identifier
    """

    device_id = request.META.get("HTTP_DEVICEID", None)
    if device_id is None:
        return Response(data=message.invalid_headers, status=status.HTTP_400_BAD_REQUEST)

    project_id = request.GET.get("id", None)
    if project_id is None:
        return Response(data=message.invalid_query, status=status.HTTP_400_BAD_REQUEST)

    article_max_age = request.GET.get(ARTICLE_MAX_AGE_PARAM, None)
    if article_max_age is not None and article_max_age.isdigit() is False:
        return Response(data=message.invalid_query, status=status.HTTP_400_BAD_REQUEST)

    if article_max_age is None:
        article_max_age = DEFAULT_ARTICLE_MAX_AGE
    else:
        article_max_age = int(article_max_age)

    lat = request.GET.get("lat", None)
    lon = request.GET.get("lon", None)
    address = request.GET.get("address", None)  # akkerstraat%2014 -> akkerstraat 14
    if address is not None:
        lat, lon = address_to_gps(address)

    project_obj = Project.objects.filter(pk=project_id, active=True).first()
    if project_obj is None:
        return Response(
            data=message.no_record_found,
            status=status.HTTP_404_NOT_FOUND,
        )

    # Only create device when all required parameters are provided
    device = Device.objects.filter(device_id=device_id).first()
    if device is None:
        device_serializer = DeviceSerializer(data={"device_id": device_id})
        if not device_serializer.is_valid():
            return Response(device_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        device = device_serializer.save()

    context = {
        "lat": lat,
        "lon": lon,
        "device_id": device.device_id,
        "article_max_age": article_max_age,
        "followed_projects": device.followed_projects.all(),
    }
    project_serializer = ProjectDetailsSerializer(
        instance=project_obj,
        partial=True,
        data={},
        context=context,
    )

    # Validation is required to get data from serializer
    if not project_serializer.is_valid():
        return Response(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(data=project_serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(**as_project_follow_post)
@swagger_auto_schema(**as_project_follow_delete)
@api_view(["POST", "DELETE"])
@RequestMustComeFromApp
def project_follow(request):
    """Subscribe or un-subscribe from project"""
    device_id = request.META.get("HTTP_DEVICEID", None)
    if device_id is None:
        return Response(
            data=message.invalid_headers,
            status=status.HTTP_400_BAD_REQUEST,
        )

    project_id = request.data.get("id", None)
    if project_id is None:
        return Response(
            data=message.invalid_parameters,
            status=status.HTTP_400_BAD_REQUEST,
        )

    project = Project.objects.filter(pk=project_id).first()
    if project is None:
        return Response(
            data=message.no_record_found,
            status=status.HTTP_404_NOT_FOUND,
        )

    device = Device.objects.filter(device_id=device_id).first()

    # Clear cache related to device
    memoize.clear_cache_by_key(device_id)

    # Follow flow
    if request.method == "POST":
        if device is None:
            serializer = DeviceSerializer(data={"device_id": device_id, "followed_projects": [project.pk]})
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
        else:
            device.followed_projects.add(project)
            DeviceSerializer(instance=device, partial=True)

        return Response(data="Subscription added", status=status.HTTP_200_OK)

    # Unfollow flow
    # request.method == 'DELETE'
    if device is None:
        return Response(data=message.no_record_found, status=status.HTTP_404_NOT_FOUND)

    device.followed_projects.remove(project)
    return Response(data="Subscription removed", status=status.HTTP_200_OK)


# NOTE: should be moved to articles views?
@swagger_auto_schema(**as_projects_followed_articles)
@api_view(["GET"])
@RequestMustComeFromApp
def projects_followed_articles(request):
    """Get articles for followed projects"""
    device_id = request.META.get("HTTP_DEVICEID", None)

    if device_id is None:
        return Response(
            data=message.invalid_headers,
            status=status.HTTP_400_BAD_REQUEST,
        )

    device = Device.objects.filter(device_id=device_id).first()
    if device is None:
        return Response(
            data=message.no_record_found,
            status=status.HTTP_404_NOT_FOUND,
        )

    article_max_age = request.GET.get(ARTICLE_MAX_AGE_PARAM, 3)

    if not str(article_max_age).isdigit():
        return Response(data=message.invalid_parameters, status=status.HTTP_400_BAD_REQUEST)

    followed_projects: list[Project] = device.followed_projects.all()

    result = {}
    for project in followed_projects:
        recent_articles = get_recent_articles_of_project(project, article_max_age)
        result[project.foreign_id] = recent_articles

    return Response(data=result, status=status.HTTP_200_OK)
