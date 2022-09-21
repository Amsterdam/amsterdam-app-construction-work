import base64
import datetime

from amsterdam_app_api.GenericFunctions.IsAuthorized import IsAuthorized
from amsterdam_app_api.GenericFunctions.Logger import Logger
from amsterdam_app_api.GarbageCollector.GarbageCollector import GarbageCollector
from amsterdam_app_api.api_messages import Messages
from amsterdam_app_api.models import Image, Assets
# from amsterdam_app_api.models import CityOffices
from amsterdam_app_api.models import ProjectDetails, Projects, News
from amsterdam_app_api.serializers import ProjectsSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

message = Messages()


""" Image ingestion route
"""


@IsAuthorized
@api_view(['GET', 'POST'])
def image(request):
    if request.method == 'GET':
        identifier = request.GET.get('identifier', '')
        image_data = Image.objects.filter(pk=identifier).values('identifier').first()
        if image_data is not None:
            return Response({'status': True, 'result': image_data}, status=200)
        else:
            return Response({'status': False, 'result': image_data}, status=200)
    elif request.method == 'POST':
        try:
            image_data = dict(request.data)
            image_data['data'] = base64.b64decode(image_data['data'])
            image_object = Image(**image_data)
            image_object.save()
            return Response({'status': True, 'result': True}, status=200)
        except Exception as error:
            logger = Logger()
            logger.error('ingest/image: {error}'.format(error=error))
            return Response({'status': False, 'result': str(error)}, status=500)


""" Assets ingestion route
"""


@IsAuthorized
@api_view(['GET', 'POST'])
def asset(request):
    if request.method == 'GET':
        identifier = request.GET.get('identifier', '')
        asset_data = Assets.objects.filter(pk=identifier).values('identifier').first()
        if asset_data is not None:
            return Response({'status': True, 'result': asset_data}, status=200)
        else:
            return Response({'status': False, 'result': asset_data}, status=200)
    elif request.method == 'POST':
        try:
            asset_data = dict(request.data)
            asset_data['data'] = base64.b64decode(asset_data['data'])
            asset_data = Assets(**asset_data)
            asset_data.save()
            return Response({'status': True, 'result': True}, status=200)
        except Exception as error:
            logger = Logger()
            logger.error('ingest/assets: {error}'.format(error=error))
            return Response({'status': False, 'result': str(error)}, status=500)


""" City office(s) and contact 
"""


# @IsAuthorized
# @api_view(['POST'])
# def city_offices(request):
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


""" Project(s) and News
"""


@IsAuthorized
@api_view(['POST'])
def project(request):
    created = False
    try:
        data = dict(request.data)

        # New record or update existing
        project_details_object, created = ProjectDetails.objects.update_or_create(identifier=data.get('identifier'))
        if created is True:
            project_details_object = ProjectDetails(**data)  # Update last scrape time is done implicitly
            project_details_object.save()
        else:
            data['last_seen'] = datetime.datetime.now()  # Update last scrape time
            ProjectDetails.objects.filter(pk=data.get('identifier')).update(**data)
        return Response({'status': True, 'result': True}, status=200)
    except Exception as error:
        if created is True:
            ProjectDetails.objects.filter(pk='').delete()
        logger = Logger()
        logger.error('ingest/project: {error}'.format(error=error))
        return Response({'status': False, 'result': str(error)}, status=500)


@IsAuthorized
@api_view(['GET', 'POST', 'DELETE'])
def projects(request):
    if request.method == 'GET':
        identifier = request.GET.get('identifier', None)
        projects_object = Projects.objects.filter(pk=identifier).first()
        if projects_object is None:
            return Response({'status': True, 'result': None}, status=200)
        serializer = ProjectsSerializer(projects_object, many=False)
        return Response({'status': True, 'result': serializer.data}, status=200)

    elif request.method == 'POST':
        created = False
        try:
            # Get POST data
            data = dict(request.data)

            # New record or update existing
            project_details_object, created = Projects.objects.update_or_create(identifier=data.get('identifier'))
            if created is True:
                project_object = Projects(**data)
                project_object.save()  # Update last scrape time is done implicitly
            else:
                data['last_seen'] = datetime.datetime.now()
                Projects.objects.filter(pk=data.get('identifier')).update(**data)
            return Response({'status': True, 'result': True}, status=200)
        except Exception as error:
            if created is True:
                Projects.objects.filter(pk='').delete()
            logger = Logger()
            logger.error('ingest/projects (POST): {error}'.format(error=error))
            return Response({'status': False, 'result': str(error)}, status=500)

    elif request.method == 'DELETE':
        try:
            # Delete record
            data = dict(request.data)
            Projects.objects.filter(pk=data.get('identifier')).delete()
            return Response({'status': True, 'result': True}, status=200)
        except Exception as error:
            logger = Logger()
            logger.error('ingest/projects (DELETE): {error}'.format(error=error))
            return Response({'status': False, 'result': str(error)}, status=500)


@IsAuthorized
@api_view(['GET', 'POST', 'DELETE'])
def news(request):
    try:
        data = dict(request.data)
        news_item_object, created = News.objects.update_or_create(identifier=data.get('identifier'))
        if created is True:
            news_item_object = News(**data)  # Update last scrape time is done implicitly
            news_item_object.save()
        else:
            data['last_seen'] = datetime.datetime.now()  # Update last scrape time
            News.objects.filter(pk=data.get('identifier')).update(**data)
        return Response({'status': True, 'result': True}, status=200)
    except Exception as error:
        logger = Logger()
        logger.error('ingest/news: {error}'.format(error=error))
        return Response({'status': False, 'result': str(error)}, status=500)


""" Garbage collector
"""


@IsAuthorized
@api_view(['GET'])
def garbage_collector(request):
    project_type = request.GET.get('project_type')
    collector = GarbageCollector(last_scrape_time=(datetime.datetime.now() - datetime.timedelta(hours=1)))
    collector.collect_iprox(project_type=project_type)

    return Response({'status': True, 'result': 'Garbage collection done'}, status=200)
