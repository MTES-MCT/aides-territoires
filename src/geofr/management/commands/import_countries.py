from django.core.management.base import BaseCommand

from geofr.models import Perimeter


class Command(BaseCommand):
    """Import the list of all regions."""

    def handle(self, *args, **options):

        Perimeter.objects.create(
            scale=Perimeter.TYPES.country,
            code='FRA',
            name='France')
        Perimeter.objects.create(
            scale=Perimeter.TYPES.continent,
            code='EU',
            name='Europe')
