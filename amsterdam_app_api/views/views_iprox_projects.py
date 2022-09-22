from amsterdam_app_api.swagger.swagger_views_iprox_projects import as_projects
from amsterdam_app_api.swagger.swagger_views_iprox_projects import as_project_details
from amsterdam_app_api.swagger.swagger_views_iprox_projects import as_projects_follow_post
from amsterdam_app_api.swagger.swagger_views_iprox_projects import as_projects_follow_delete
from amsterdam_app_api.swagger.swagger_views_iprox_projects import as_projects_followed_articles
from amsterdam_app_api.swagger.swagger_views_search import as_search
from amsterdam_app_api.api_messages import Messages
from amsterdam_app_api.models import Projects
from amsterdam_app_api.models import ProjectDetails
from amsterdam_app_api.models import FollowedProjects
from amsterdam_app_api.models import News
from amsterdam_app_api.models import WarningMessages
from amsterdam_app_api.serializers import ProjectsSerializer
from amsterdam_app_api.serializers import ProjectDetailsSerializer
from amsterdam_app_api.serializers import NewsSerializer
from amsterdam_app_api.serializers import WarningMessagesExternalSerializer
from amsterdam_app_api.GenericFunctions.Distance import Distance
from amsterdam_app_api.GenericFunctions.SetFilter import SetFilter
from amsterdam_app_api.GenericFunctions.Sort import Sort
from amsterdam_app_api.GenericFunctions.StaticData import StaticData
from amsterdam_app_api.GenericFunctions.TextSearch import TextSearch
from amsterdam_app_api.GenericFunctions.RequestMustComeFromApp import RequestMustComeFromApp
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.db import IntegrityError
from datetime import datetime, timedelta
import json
import requests
import urllib.parse

message = Messages()


def search(model, request):
    text = request.GET.get('text', None)
    query_fields = request.GET.get('query_fields', '')
    fields = request.GET.get('fields', None)
    page_size = int(request.GET.get('page_size', 10))
    page = int(request.GET.get('page', 1)) - 1

    # Get Model fields
    model_fields = [x.name for x in model._meta.get_fields()]

    if text is None:
        return Response({'status': False, 'result': message.invalid_query}, status=422)
    if len([x for x in query_fields.split(',') if x not in model_fields]) > 0:
        return Response({'status': False, 'result': message.no_such_field_in_model}, status=422)
    if fields is not None and len([x for x in fields.split(',') if x not in model_fields]) > 0:
        return Response({'status': False, 'result': message.no_such_field_in_model}, status=422)

    text_search = TextSearch(model, text, query_fields, return_fields=fields, page_size=page_size, page=page)
    result = text_search.search()
    return Response({'status': True, 'result': result['page'], 'pages': result['pages']}, status=200)


@swagger_auto_schema(**as_projects)
@api_view(['GET'])
def projects(request):
    """
    Get a list of all projects. Narrow down by query param: project-type
    """
    import time
    now = time.time()
    if request.method == 'GET':
        deviceid = request.META.get('HTTP_DEVICEID', None)
        if deviceid is None:
            return Response({'status': False, 'result': message.invalid_headers}, status=422)

        project_type = request.GET.get('project-type', None)
        sort_by = request.GET.get('sort-by', None)
        sort_order = request.GET.get('sort-order', None)
        model_items = request.GET.get('fields', None)
        articles_max_age = request.GET.get('articles_max_age', None)
        lat = request.GET.get('lat', None)
        lon = request.GET.get('lon', None)
        radius = request.GET.get('radius', None)
        address = request.GET.get('address', None)

        if address is not None:
            apis = StaticData.urls()
            url = '{api}{address}'.format(api=apis['address_to_gps'], address=urllib.parse.quote_plus(address))
            result = requests.get(url=url, timeout=1)
            data = json.loads(result.content)
            if len(data['results']) == 1:
                lon = data['results'][0]['centroid'][0]
                lat = data['results'][0]['centroid'][1]

        fields = [] if model_items is None else model_items.split(',')
        if articles_max_age is not None and 'identifier' not in fields:
            fields.append('identifier')

        followed = False
        if 'followed' in fields:
            fields.remove('followed')
            if 'identifier' in fields:
                followed = True

        # Check query parameters
        if project_type is not None and project_type not in ['brug', 'kade', 'bouw-en-verkeer']:
            return Response({'status': False, 'result': message.invalid_query}, status=422)

        # Get list of projects by district
        try:
            district_id = int(request.GET.get('district-id', None))
        except Exception as error:
            district_id = None

        # Set filter
        query_filter = SetFilter(district_id=district_id, project_type=project_type, active=True).get()

        # Return filtered result or all projects

        projects_object = Projects.objects.filter(**query_filter).all()

        # Get followers for projects
        following = [x['projectid'] for x in FollowedProjects.objects.filter(deviceid__iexact=deviceid).values('projectid')]
        if len(fields) != 0:
            model_fields = [x.name for x in Projects._meta.fields]
            serializer_fields = [x for x in fields if x in model_fields]
            serializer = ProjectsSerializer(projects_object, context={'fields': serializer_fields}, many=True)
            if followed is True:
                for i in range(len(serializer.data)):
                    serializer.data[i]['followed'] = False
                    if serializer.data[i]['identifier'] in following:
                        serializer.data[i]['followed'] = True
        else:
            serializer = ProjectsSerializer(projects_object, many=True)
            for i in range(len(serializer.data)):
                serializer.data[i]['followed'] = False
                if serializer.data[i]['identifier'] in following:
                    serializer.data[i]['followed'] = True

        # Get results from serializer
        results = serializer.data

        # Get distance
        if lat is not None and lon is not None:
            project_details = ProjectDetails.objects.values('identifier', 'coordinates').all()
            coordinates = {x['identifier']: (x['coordinates']['lat'], x['coordinates']['lon']) for x in project_details}
            for i in range(len(serializer.data) - 1, -1, -1):
                identifier = results[i]['identifier']
                cords_1 = (float(lat), float(lon))
                cords_2 = coordinates.get(identifier, (None, None))
                if None in cords_2:
                    cords_2 = (None, None)
                elif (0, 0) == cords_2:
                    cords_2 = (None, None)
                distance = Distance(cords_1, cords_2)
                results[i]['meter'] = distance.meter
                results[i]['strides'] = distance.strides

                if radius is not None and distance.meter is not None:
                    if distance.meter > float(radius):
                        del results[i]

        if articles_max_age is not None:
            articles_max_age = int(articles_max_age)
            start_date = datetime.now() - timedelta(days=articles_max_age)
            end_date = datetime.now()
            start_date_str = start_date.strftime('%Y-%m-%d')

            news_articles_all = list(News.objects.all())
            serializer_news = NewsSerializer(news_articles_all, many=True)
            news_articles = [x for x in serializer_news.data if x['publication_date'] >= start_date_str]
            warning_articles_all = list(WarningMessages.objects.filter(publication_date__range=[start_date, end_date]).all())
            serializer_warnings = WarningMessagesExternalSerializer(warning_articles_all, many=True)
            all_articles = news_articles + serializer_warnings.data
            articles = dict()
            for article in all_articles:
                payload = {'identifier': article['identifier'], 'publication_date': article['publication_date']}
                try:
                    if article['project_identifier'] in articles:
                        articles[article['project_identifier']].append(payload)
                    else:
                        articles[article['project_identifier']] = [payload]
                except Exception as error:
                    print(error)

            for i in range(len(results)):
                results[i]['recent_articles'] = []
                if results[i]['identifier'] in articles:
                    results[i]['recent_articles'] = articles[results[i]['identifier']]

        result = Sort().list_of_dicts(results, key=sort_by, sort_order=sort_order)
        return Response({'status': True, 'result': result}, status=200)


@swagger_auto_schema(**as_search)
@api_view(['GET'])
def projects_search(request):
    model = Projects
    result = search(model, request)
    return result


@swagger_auto_schema(**as_project_details)
@api_view(['GET'])
def project_details(request):
    """
    Get details for a project by identifier
    """
    if request.method == 'GET':
        deviceid = request.META.get('HTTP_DEVICEID', None)
        if deviceid is None:
            return Response({'status': False, 'result': message.invalid_headers}, status=422)

        identifier = request.GET.get('id', None)
        if identifier is None:
            return Response({'status': False, 'result': message.invalid_query}, status=422)

        articles_max_age = request.GET.get('articles_max_age', None)

        lat = request.GET.get('lat', None)
        lon = request.GET.get('lon', None)
        address = request.GET.get('address', None)  # akkerstraat%2014 -> akkerstraat 14
        if address is not None:
            apis = StaticData.urls()
            url = '{api}{address}'.format(api=apis['address_to_gps'], address=urllib.parse.quote_plus(address))
            result = requests.get(url=url, timeout=1)
            data = json.loads(result.content)
            if len(data['results']) == 1:
                lon = data['results'][0]['centroid'][0]
                lat = data['results'][0]['centroid'][1]

        project_object = ProjectDetails.objects.filter(pk=identifier, active=True).first()
        if project_object is not None:
            # Get followers
            count = FollowedProjects.objects.filter(projectid=identifier).count()
            followed = FollowedProjects.objects.filter(deviceid=deviceid, projectid=identifier).first()
            project_data = dict(ProjectDetailsSerializer(project_object, many=False).data)
            project_data['followers'] = count
            project_data['followed'] = False if followed is None else True

            # Get distance
            project_data['meter'] = None
            project_data['strides'] = None
            if lat is not None and lon is not None:
                cords_1 = (float(lat), float(lon))
                cords_2 = (project_object.coordinates['lat'], project_object.coordinates['lon'])
                if None in cords_2:
                    cords_2 = (None, None)
                elif (0, 0) == cords_2:
                    cords_2 = (None, None)
                distance = Distance(cords_1, cords_2)
                project_data['meter'] = distance.meter
                project_data['strides'] = distance.strides

            # Get recent articles
            if articles_max_age is not None:
                articles_max_age = int(articles_max_age)
                start_date = datetime.now() - timedelta(days=articles_max_age)
                end_date = datetime.now()
                start_date_str = start_date.strftime('%Y-%m-%d')
                news_articles_all = list(News.objects.filter(project_identifier=identifier).all())
                serializer_news = NewsSerializer(news_articles_all, many=True)
                news_articles = [x['identifier'] for x in serializer_news.data if x['publication_date'] >= start_date_str]
                warning_articles = list(WarningMessages.objects.filter(project_identifier=identifier, publication_date__range=[start_date, end_date]).all())
                serializer_warning = WarningMessagesExternalSerializer(warning_articles, many=True)
                project_data['recent_articles'] = news_articles + [x['identifier'] for x in serializer_warning.data]
            return Response({'status': True, 'result': project_data}, status=200)
        else:
            return Response({'status': False, 'result': message.no_record_found}, status=404)


@swagger_auto_schema(**as_search)
@api_view(['GET'])
def project_details_search(request):
    model = ProjectDetails
    result = search(model, request)
    return result


@swagger_auto_schema(**as_projects_follow_post)
@swagger_auto_schema(**as_projects_follow_delete)
@api_view(['POST', 'DELETE'])
@RequestMustComeFromApp
def projects_follow(request):
    deviceid = request.META.get('HTTP_DEVICEID', None)
    if deviceid is None:
        return Response({'status': False, 'result': message.invalid_headers}, status=422)

    if request.method == 'POST':
        project_id = request.data.get('project_id', None)
        if project_id is not None:
            project = ProjectDetails.objects.filter(identifier=project_id).first()
            if project is None:
                return Response({'status': False, 'result': message.no_record_found}, status=404)
        try:
            follow_project = FollowedProjects(projectid=project_id, deviceid=deviceid)
            follow_project.save()
        except IntegrityError:  # Double request with same data, discard...
            pass
        return Response({'status': False, 'result': 'Subscription added'}, status=200)

    if request.method == 'DELETE':
        project_id = request.data.get('project_id', None)
        follow_project = FollowedProjects.objects.filter(projectid=project_id, deviceid=deviceid).first()
        if follow_project is not None:
            follow_project.delete()
        return Response({'status': False, 'result': 'Subscription removed'}, status=200)


@swagger_auto_schema(**as_projects_followed_articles)
@api_view(['GET'])
def projects_followed_articles(request):
    deviceid = request.META.get('HTTP_DEVICEID', None)
    article_max_age = int(request.GET.get('article-max-age', 3))
    if deviceid is None:
        return Response({'status': False, 'result': message.invalid_headers}, status=422)

    followed_projects = list(FollowedProjects.objects.filter(deviceid=deviceid).values('projectid').all())
    project_identifiers = [x['projectid'] for x in followed_projects]

    result = {}
    # Get recent articles
    for identifier in project_identifiers:
        start_date = datetime.now() - timedelta(days=article_max_age)
        end_date = datetime.now()
        start_date_str = start_date.strftime('%Y-%m-%d')
        news_articles_all = list(News.objects.filter(project_identifier=identifier).all())
        serializer_news = NewsSerializer(news_articles_all, many=True)
        news_articles = [x['identifier'] for x in serializer_news.data if x['publication_date'] >= start_date_str]
        warning_articles = list(WarningMessages.objects.filter(project_identifier=identifier,
                                                               publication_date__range=[start_date, end_date]).all())
        result[identifier] = news_articles + [x.identifier for x in warning_articles]

    return Response({'status': True, 'result': {'projects': result}})
