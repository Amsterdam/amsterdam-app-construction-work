from amsterdam_app_api.api_messages import Messages
from amsterdam_app_api.models import CityContact
from amsterdam_app_api.models import CityOffice
from amsterdam_app_api.models import CityOffices
from amsterdam_app_api.serializers import CityContactSerializer
from amsterdam_app_api.serializers import CityOfficeSerializer
from amsterdam_app_api.serializers import CityOfficesSerializer
from amsterdam_app_api.swagger.swagger_views_iprox_stadsloketten import as_city_contact
from amsterdam_app_api.swagger.swagger_views_iprox_stadsloketten import as_city_office
from amsterdam_app_api.swagger.swagger_views_iprox_stadsloketten import as_city_offices
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


messages = Messages()


@swagger_auto_schema(**as_city_contact)
@api_view(['GET'])
def city_contact(request):
    data = CityContact.objects.first()
    serializer = CityContactSerializer(data, many=False)
    return Response({'status': True, 'result': serializer.data})


@swagger_auto_schema(**as_city_offices)
@api_view(['GET'])
def city_offices(request):
    data = CityOffices.objects.first()
    serializer = CityOfficesSerializer(data, many=False)
    return Response({'status': True, 'result': serializer.data})


@swagger_auto_schema(**as_city_office)
@api_view(['GET'])
def city_office(request):
    identifier = request.GET.get('id', None)
    if identifier is None:
        return Response({'status': False, 'result': messages.invalid_query}, 422)

    data = CityOffice.objects.filter(pk=identifier).first()
    if data is None:
        return Response({'status': False, 'result': messages.no_record_found}, 404)

    serializer = CityOfficeSerializer(data, many=False)
    return Response({'status': True, 'result': serializer.data}, 200)
