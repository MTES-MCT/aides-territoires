import requests
from django.core.management.base import BaseCommand, CommandError

from geofr.models import Perimeter
from geofr.constants import OVERSEAS_REGIONS


API_URL = 'https://geo.api.gouv.fr/departements/'


class Command(BaseCommand):
    """Import the list of all departments."""

    def handle(self, *args, **options):

        api_result = requests.get(API_URL)
        if api_result.status_code != 200:
            raise CommandError('Failed to reach geo api.')

        data = api_result.json()

        departments = []
        for entry in data:
            department = Perimeter(
                scale=Perimeter.TYPES.department,
                code=entry['code'],
                name=entry['nom'],
                region=entry['codeRegion'],
                is_overseas=(entry['codeRegion'] in OVERSEAS_REGIONS))
            departments.append(department)

        results = Perimeter.objects.bulk_create(departments)
        self.stdout.write(self.style.SUCCESS(
            '%d departments imported.' % len(results)))
