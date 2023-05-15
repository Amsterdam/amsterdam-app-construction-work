""" Views for distance API's """
import json
import urllib.parse
import requests
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from amsterdam_app_api.GenericFunctions.StaticData import StaticData
from amsterdam_app_api.GenericFunctions.Distance import Distance
from amsterdam_app_api.GenericFunctions.Sort import Sort
from amsterdam_app_api.api_messages import Messages
from amsterdam_app_api.models import ProjectDetails, Projects
from amsterdam_app_api.serializers import ProjectsSerializer
from amsterdam_app_api.swagger.swagger_views_distance import as_distance

messages = Messages()


@swagger_auto_schema(**as_distance)
@api_view(['GET'])
def distance(request):
    """ Get distance 'in bird flight' from user to projects
    """
    def get_projects_data(_identifier, _model_items, _distance):
        projects_object = Projects.objects.filter(pk=_identifier).first()

        if _model_items is not None:
            fields = _model_items.split(',')
            serializer = ProjectsSerializer(projects_object, context={'fields': fields}, many=False)
        else:
            serializer = ProjectsSerializer(projects_object, many=False)

        result = serializer.data
        result['meter'] = int(_distance.meter) if _distance.meter is not None else None
        result['strides'] = int(_distance.strides) if _distance.strides is not None else None
        return result

    lat = request.GET.get('lat', None)
    lon = request.GET.get('lon', None)
    radius = request.GET.get('radius', None)
    address = request.GET.get('address', None)  # akkerstraat%2014 -> akkerstraat 14
    model_items = request.GET.get('fields', None)

    if address is not None:
        apis = StaticData.urls()
        url = '{api}{address}'.format(api=apis['address_to_gps'], address=urllib.parse.quote_plus(address))
        result = requests.get(url=url, timeout=1)
        data = json.loads(result.content)
        if len(data['results']) == 1:
            lon = data['results'][0]['centroid'][0]
            lat = data['results'][0]['centroid'][1]

    if lat is None or lon is None:
        return Response({'status': False, 'result': messages.distance_params}, 422)

    try:
        cords_1 = (float(lat), float(lon))
    except Exception as error:
        return Response({'status': False, 'result': str(error)}, 500)

    results = []
    projects = list(ProjectDetails.objects.filter().all())
    for project in projects:
        cords_2 = (project.coordinates['lat'], project.coordinates['lon'])
        if project.coordinates['lat'] is None or project.coordinates['lon'] is None:
            cords_2 = (None, None)
        elif (0, 0) == (int(project.coordinates['lat']), int(project.coordinates['lon'])):
            cords_2 = (None, None)
        this_distance = Distance(cords_1, cords_2)

        result = None
        if radius is None:
            result = get_projects_data(project.identifier_id, model_items, this_distance)
        elif this_distance.meter is not None and this_distance.meter < float(radius):
            result = get_projects_data(project.identifier_id, model_items, this_distance)

        # Append the results
        if result is not None and result['identifier'] != "":
            results.append(result)

    sorted_results = Sort().list_of_dicts(results, key='meter', sort_order='asc')
    return Response({'status': True, 'result': sorted_results})
