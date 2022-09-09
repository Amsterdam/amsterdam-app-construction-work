from django.db import models

DAYS = [
    (0, 'Zondag'),
    (1, 'Maandag'),
    (2, 'Dinsdag'),
    (3, 'Woensdag'),
    (4, 'Donderdag'),
    (5, 'Vrijdag'),
    (6, 'Zaterdag')
]

HOURS = [(x, x) for x in range(0, 24)]
MINUTES = [(x, x) for x in range(0, 60)]


class CityOffices(models.Model):
    identifier = models.CharField(max_length=100, blank=False, unique=True, primary_key=True)
    title = models.CharField(max_length=100, blank=False)
    images = models.JSONField(null=True, default=dict)
    street_name = models.CharField(max_length=100, blank=False)
    street_number = models.CharField(max_length=100, blank=False)
    postal_code = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=100, blank=False)
    lat = models.FloatField(blank=False)
    lon = models.FloatField(blank=False)
    directions_url = models.CharField(max_length=100, blank=True)
    appointment = models.JSONField(null=True, blank=True, default=dict)
    visiting_hours_content = models.TextField(null=True, blank=True)
    address_content = models.JSONField(null=True, blank=True, default=dict)

    class Meta:
        unique_together = [['lat', 'lon']]


class CityOfficesOpeningHoursRegular(models.Model):
    city_office_id = models.ForeignKey('CityOffices', on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=DAYS, blank=False, unique=False)
    opens_hours = models.IntegerField(choices=HOURS, blank=False, unique=False)
    opens_minutes = models.IntegerField(choices=MINUTES, blank=False, unique=False)
    closes_hours = models.IntegerField(choices=HOURS, blank=False, unique=False)
    closes_minutes = models.IntegerField(choices=MINUTES, blank=False, unique=False)


class CityOfficesOpeningHoursExceptions(models.Model):
    city_office_id = models.ForeignKey('CityOffices', on_delete=models.CASCADE)
    date = models.DateField(null=False)  # YYYY-MM-DD format
    opens_hours = models.IntegerField(choices=HOURS, null=True, blank=True, unique=False)
    opens_minutes = models.IntegerField(choices=MINUTES, null=True, blank=True, unique=False)
    closes_hours = models.IntegerField(choices=HOURS, null=True, blank=True, unique=False)
    closes_minutes = models.IntegerField(choices=MINUTES, null=True, blank=True, unique=False)
