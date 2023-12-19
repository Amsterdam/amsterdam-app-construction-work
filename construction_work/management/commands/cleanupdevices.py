""" Iprox garbage collector """
from django.core.management.base import BaseCommand
from django.utils import timezone

from construction_work.models import Device

ONE_YEAR_AGO = one_year_ago = timezone.now() - timezone.timedelta(days=365)


class Command(BaseCommand):
    """Remove old devices"""

    help = "Remove old devices"

    def handle(self, *args, **options):
        old_devices = Device.objects.filter(last_access__lt=ONE_YEAR_AGO)
        count = old_devices.count()
        old_devices.delete()
        self.stdout.write(self.style.SUCCESS(f"Removed {count} devices"))
