import requests
from django.core.management.base import BaseCommand, CommandError

from geofr.models import Perimeter
from geofr.constants import OVERSEAS_REGIONS


API_URL = 'https://geo.api.gouv.fr/regions/'


class Command(BaseCommand):
    """Import the list of all regions."""

    def handle(self, *args, **options):

        api_result = requests.get(API_URL)
        if api_result.status_code != 200:
            raise CommandError('Failed to reach geo api.')

        data = api_result.json()

        regions = []
        for entry in data:
            region = Perimeter(
                scale=Perimeter.TYPES.region,
                code=entry['code'],
                name=entry['nom'],
                is_overseas=(entry['code'] in OVERSEAS_REGIONS),
            )
            regions.append(region)

        results = Perimeter.objects.bulk_create(regions)
        self.stdout.write(self.style.SUCCESS(
            '%d regions imported.' % len(results)))
