# pylint: disable=unnecessary-lambda-assignment,expression-not-assigned
""" Views for iprox project pages """
from math import ceil

from django.db.models import Max
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from construction_work.api_messages import Messages
from construction_work.generic_functions.gps_utils import address_to_gps, get_distance
from construction_work.generic_functions.memoize import Memoize
from construction_work.generic_functions.project_utils import get_recent_articles_of_project
from construction_work.generic_functions.request_must_come_from_app import (
    RequestMustComeFromApp,
)
from construction_work.generic_functions.static_data import (
    DEFAULT_ARTICLE_MAX_AGE,
)
from construction_work.generic_functions.text_search import MIN_QUERY_LENGTH, get_non_related_fields, search_text_in_model
from construction_work.models import Project
from construction_work.models.device import Device
from construction_work.serializers import (
    DeviceSerializer,
    ProjectDetailsSerializer,
    ProjectListSerializer,
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


def _paginate_data(request, data: list, extra_params: dict=None) -> dict:
    """Create pagination of data"""
    page = int(request.GET.get("page", 1)) - 1
    page_size = int(request.GET.get("page_size", 10))

    path_info = request.META.get("PATH_INFO")
    http_prefix = "https://" if request.is_secure() else "http://"
    http_host = request.META.get("HTTP_HOST", "localhost")
    host = http_prefix + http_host + path_info

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

    links = {"self": {"href": host}}

    extra_params_str = ""
    if extra_params is not None:
        for k, v in extra_params.items():
            param_str = f"&{k}={v}"
            extra_params_str += param_str

    # Add next page link, if available
    if pagination["number"] < pagination["totalPages"]:
        next_page = str(pagination["number"] + 1)
        links["next"] = {"href": f"{host}?page={next_page}&page_size={page_size}{extra_params_str}"}
    # Add previous page link, if available
    if pagination["number"] > 1:
        previous_page = str(pagination["number"] - 1)
        links["previous"] = {"href": f"{host}?page={previous_page}&page_size={page_size}{extra_params_str}"}    

    return {
        "result": paginated_result,
        "page": pagination,
        "_links": links,
    }


def search(model, request) -> Response:
    """Search model using request parameters"""
    text = request.GET.get("text", None)
    query_fields = request.GET.get("query_fields", None)
    return_fields = request.GET.get("fields", None)

    # Get all fields of given model
    model_fields = get_non_related_fields(model)

    # Text length has to be at least 3
    if text is None or len(text) < MIN_QUERY_LENGTH:
        return Response(data=message.invalid_query, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if given query fields are in model fields
    if (
        query_fields is not None
        and len([x for x in query_fields.split(",") if x not in model_fields]) > 0
    ):
        return Response(
            data=message.no_such_field_in_model, status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if given return fields are in model fields, if assigned
    if (
        return_fields is not None
        and len([x for x in return_fields.split(",") if x not in model_fields]) > 0
    ):
        return Response(
            data=message.no_such_field_in_model, status=status.HTTP_400_BAD_REQUEST
        )

    # Perform search
    result = search_text_in_model(model, text, query_fields, return_fields)

    # Paginate result
    extra_params = {}
    if text:
        extra_params["text"] = text
    if query_fields:
        extra_params["query_fields"] = query_fields
    if return_fields:
        extra_params["fields"] = return_fields

    paginated_data = _paginate_data(request, result, extra_params=extra_params)
    
    return Response(
        data=paginated_data,
        status=status.HTTP_200_OK,
    )


@swagger_auto_schema(**as_projects)
@api_view(["GET"])  # keep cached result for 5 minutes in memory
def projects(request):
    """Get a list of all projects in specific order"""

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
        article_max_age = int(
            request.GET.get("article_max_age", 3)
        ) # Max days since publication date

        # Convert address into GPS data. Note: This should never happen, the device should already
        if address is not None and (lat is None or lon is None):
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

            meter, _ = get_distance(given_cords, project_cords)
            # distance = GeoPyDistance(given_cords, project_cords)
            if meter is None:
                return float("inf")
            return meter

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
            "article_max_age": article_max_age,
        }
        serializer = ProjectListSerializer(instance=all_projects, many=True, context=context)
        
        return serializer.data

    # Call _fetch_projects
    result = _fetch_projects(device_id)

    paginated_data = _paginate_data(request, result)
    return Response(data=paginated_data, status=status.HTTP_200_OK)


@swagger_auto_schema(**as_search)
@api_view(["GET"])
def projects_search(request):
    """Search project"""
    return search(Project, request)


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

    article_max_age = request.GET.get("article_max_age", None)
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
            "article_max_age": article_max_age,
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
            data=message.invalid_headers,
            status=status.HTTP_400_BAD_REQUEST,
        )

    foreign_id = request.data.get("foreign_id", None)
    if foreign_id is None:
        return Response(
            data=message.invalid_parameters,
            status=status.HTTP_400_BAD_REQUEST,
        )

    project = Project.objects.filter(foreign_id=foreign_id).first()
    if project is None:
        return Response(
            data=message.no_record_found,
            status=status.HTTP_404_NOT_FOUND,
        )

    device = Device.objects.filter(device_id=device_id).first()

    # Follow flow
    if request.method == "POST":
        if device is None:
            serializer = DeviceSerializer(
                data={"device_id": device_id, "followed_projects": [project.pk]}
            )
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
        else:
            device.followed_projects.add(project)
            serializer = DeviceSerializer(
                instance=device, partial=True
            )
        
        return Response(data="Subscription added", status=status.HTTP_200_OK)

    # Unfollow flow
    # request.method == 'DELETE'
    if device is None:
        return Response(
            data=message.no_record_found,
            status=status.HTTP_404_NOT_FOUND,
        )

    device.followed_projects.remove(project)
    return Response(
        data="Subscription removed", status=status.HTTP_200_OK
    )


# NOTE: should be moved to articles views?
@swagger_auto_schema(**as_projects_followed_articles)
@api_view(["GET"])
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

    article_max_age = request.GET.get("article_max_age", 3)
    
    if not str(article_max_age).isdigit():
        return Response(data=message.invalid_parameters, status=status.HTTP_400_BAD_REQUEST)

    followed_projects: list[Project] = device.followed_projects.all()

    result = {}
    for project in followed_projects:
        recent_articles = get_recent_articles_of_project(project, article_max_age)
        result[project.foreign_id] = recent_articles

    return Response(data=result, status=status.HTTP_200_OK)
