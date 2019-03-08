import requests
from operator import attrgetter
from django.core.management.base import BaseCommand, CommandError

from geofr.models import Perimeter
from geofr.constants import OVERSEAS_REGIONS


API_URL = 'https://geo.api.gouv.fr/departements/{}/communes/'


FORMAT_STR = '{c.name};{c.code};{c.departments};{c.zipcodes}\n'


class Command(BaseCommand):
    """Import the list of all communes."""

    def handle(self, *args, **options):

        # Let's serialize and dump existing communes in a file
        communes = Perimeter.objects \
            .filter(scale=Perimeter.TYPES.commune) \
            .order_by('name')
        list_communes = list(communes)
        list_communes.sort(key=attrgetter('name', 'code'))
        with open('/tmp/existing_communes.dump', 'w') as f:
            for commune in list_communes:
                f.write(FORMAT_STR.format(c=commune))

        # Now, let's fetch updated data, and dump it with the same format
        departments = Perimeter.objects.filter(
            scale=Perimeter.TYPES.department)
        new_communes = []
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
                new_communes.append(commune)

        new_communes.sort(key=attrgetter('name', 'code'))
        with open('/tmp/new_communes.dump', 'w') as f:
            for commune in new_communes:
                f.write(FORMAT_STR.format(c=commune))

        print('Existing communes: {}'.format(len(list_communes)))
        print('New communes: {}'.format(len(new_communes)))