""" Views for ingestion routes """
import base64
from datetime import datetime
from django.forms import ValidationError

from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from construction_work.api_messages import Messages
from construction_work.garbage_collector.garbage_collector import GarbageCollector
from construction_work.generic_functions.generic_logger import Logger
from construction_work.generic_functions.is_authorized import IsAuthorized

# from construction_work.models import CityOffices
from construction_work.models import Article, Asset, Image, Project
from construction_work.serializers import ProjectSerializer
from construction_work.swagger.swagger_views_ingestion import as_garbage_collector

message = Messages()


@IsAuthorized
@api_view(["GET", "POST"])
def image(request):
    """Image ingestion route"""
    if request.method == "GET":
        identifier = request.GET.get("identifier", "")
        image_data = Image.objects.filter(pk=identifier).values("identifier").first()
        if image_data is not None:
            return Response({"status": True, "result": image_data}, status=200)
        return Response({"status": False, "result": image_data}, status=200)

    # request.method == 'POST':
    try:
        image_data = dict(request.data)
        image_data["data"] = base64.b64decode(image_data["data"])
        image_object = Image(**image_data)
        image_object.save()
        return Response({"status": True, "result": True}, status=200)
    except Exception as error:
        logger = Logger()
        logger.error("ingest/image: {error}".format(error=error))
        return Response({"status": False, "result": str(error)}, status=500)


@IsAuthorized
@api_view(["GET", "POST"])
def asset(request):
    """Assets ingestion route"""
    if request.method == "GET":
        identifier = request.GET.get("identifier", "")
        asset_data = Asset.objects.filter(pk=identifier).values("identifier").first()
        if asset_data is not None:
            return Response({"status": True, "result": asset_data}, status=200)
        return Response({"status": False, "result": asset_data}, status=200)

    # request.method == 'POST':
    try:
        asset_data = dict(request.data)
        asset_data["data"] = base64.b64decode(asset_data["data"])
        asset_data = Asset(**asset_data)
        asset_data.save()
        return Response({"status": True, "result": True}, status=200)
    except Exception as error:
        logger = Logger()
        logger.error("ingest/assets: {error}".format(error=error))
        return Response({"status": False, "result": str(error)}, status=500)


# @IsAuthorized
# @api_view(['POST'])
# def city_offices(request):
#     """ City office(s) and contact
#     """
#     try:
#         # save method is overridden to allow only 1 single record
#         data = request.data
#         city_offices = CityOffices(offices=data)
#         city_offices.save()
#         return Response({'status': True, 'result': True}, status=200)
#     except Exception as error:
#         logger = Logger()
#         logger.error('ingest/cityoffices: {error}'.format(error=error))
#         return Response({'status': False, 'result': 'Caught error ingesting city offices'}, status=500)


@IsAuthorized
@api_view(["POST"])
def project(request):
    """Project(s) and News"""
    success = False
    data = dict(request.data)
    project = Project.objects.filter(pk=data.get("project_id")).first()
    
    # New record or update existing
    if project is None:
        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            success = True
        else:
            success = False
    else:
        # TODO: check if this updates the right project
        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            project.last_seen = datetime.now()
            project.save()

    response = None
    if success:
        response = Response({"status": True, "result": True}, status=200)
    else:
        response = Response({"status": True, "result": True}, status=404)
    return response


@IsAuthorized
@api_view(["GET", "POST", "DELETE"])
def projects(request):
    """Projects"""
    if request.method == "GET":
        identifier = request.GET.get("identifier", None)
        projects_object = Project.objects.filter(pk=identifier).first()
        if projects_object is None:
            return Response({"status": True, "result": None}, status=200)
        serializer = ProjectSerializer(projects_object, many=False)
        return Response({"status": True, "result": serializer.data}, status=200)

    if request.method == "POST":
        created = False
        try:
            # Get POST data
            data = dict(request.data)

            # New record or update existing
            project_object = Project.objects.filter(identifier=data.get("identifier")).first()
            if project_object is None:
                project_object = Project(**data)
                project_object.save()  # Update last scrape time is done implicitly
            else:
                data["last_seen"] = datetime.now()
                Project.objects.filter(pk=data.get("identifier")).update(**data)
            return Response({"status": True, "result": True}, status=200)
        except Exception as error:
            if created is True:
                Project.objects.filter(pk="").delete()
            logger = Logger()
            logger.error("ingest/projects (POST): {error}".format(error=error))
            return Response({"status": False, "result": str(error)}, status=500)

    # request.method == 'DELETE':
    try:
        # Delete record
        data = dict(request.data)
        Project.objects.filter(pk=data.get("identifier")).delete()
        return Response({"status": True, "result": True}, status=200)
    except Exception as error:
        logger = Logger()
        logger.error("ingest/projects (DELETE): {error}".format(error=error))
        return Response({"status": False, "result": str(error)}, status=500)


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
        logger = Logger()
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
