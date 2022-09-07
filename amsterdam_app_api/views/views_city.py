from amsterdam_app_api.api_messages import Messages
from amsterdam_app_api.models import CityOffices
from amsterdam_app_api.models import CityOfficesOpeningHoursRegular, CityOfficesOpeningHoursExceptions
from amsterdam_app_api.swagger.swagger_views_iprox_stadsloketten import as_city_offices
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


messages = Messages()


def get_opening_hours(identifier):
    regular = [
        {
            'dayOfWeek': x.day_of_week,
            'opening': {'hours': x.opens_hours, 'minutes': x.opens_minutes},
            'closing': {'hours': x.closes_hours, 'minutes': x.closes_minutes}
        }
        for x in list(CityOfficesOpeningHoursRegular.objects.filter(city_office_id=identifier).all())
    ]
    exceptions = [
        {
            'date': x.date,
            'opening': {'hours': x.opens_hours, 'minutes': x.opens_minutes},
            'closing': {'hours': x.closes_hours, 'minutes': x.closes_minutes}
        }
        if x.opens_hours is not None else {'date': x.date}
        for x in list(CityOfficesOpeningHoursExceptions.objects.filter(city_office_id=identifier).all())
    ]
    return {'regular': regular, 'exceptions': exceptions}


@swagger_auto_schema(**as_city_offices)
@api_view(['GET'])
def city_offices(request):
    offices = list(CityOffices.objects.all())
    result = []
    for office in offices:
        opening_hours = get_opening_hours(office.identifier)
        data = {
            'identifier': office.identifier,
            'title': office.title,
            'image': office.images,
            'address': {
                'streetName': office.street_name,
                'streetNumber': office.street_number,
                'postalCode': office.postal_code,
                'city': office.city
            },
            'addressContent': office.address_content,
            'coordinates': {
                'lat': office.lat,
                'lon': office.lon
            },
            'directionsUrl': office.directions_url,
            'appointment': office.appointment,
            'visitingHoursContent': office.visiting_hours_content,
            'openingHours': opening_hours
        }
        result.append(data)
    return Response({'status': True, 'result': result})
