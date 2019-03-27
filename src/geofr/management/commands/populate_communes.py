import requests
from django.core.management.base import BaseCommand, CommandError

from geofr.models import Perimeter
from geofr.constants import OVERSEAS_REGIONS


API_URL = 'https://geo.api.gouv.fr/departements/{}/communes/'


class Command(BaseCommand):
    """Import the list of all communes."""

    def handle(self, *args, **options):

        departments = Perimeter.objects.filter(
            scale=Perimeter.TYPES.department)

        communes = []
        for department in departments:
            self.stdout.write(
                'Importing communes for {}.'.format(department.name))
            api_result = requests.get(API_URL.format(department.code))
            if api_result.status_code != 200:
                raise CommandError('Failed to reach geo api.')

            data = api_result.json()

            for entry in data:
                commune = Perimeter(
                    scale=Perimeter.TYPES.commune,
                    code=entry['code'],
                    name=entry['nom'],
                    departments=[entry['codeDepartement']],
                    regions=[entry['codeRegion']],
                    zipcodes=entry['codesPostaux'],
                    is_overseas=(entry['codeRegion'] in OVERSEAS_REGIONS))
                communes.append(commune)

        results = Perimeter.objects.bulk_create(communes)
        self.stdout.write(self.style.SUCCESS(
            '%d communes imported.' % len(results)))
