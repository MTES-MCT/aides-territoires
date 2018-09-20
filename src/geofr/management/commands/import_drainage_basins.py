import os

from django.core.management.base import BaseCommand

from geofr.models import Perimeter
from geofr.constants import OVERSEAS_DEPARTMENTS, DEPARTMENT_TO_REGION


# Field column indexes
NAME = 2
DEPARTMENT = 0
CODE = 1
MEMBER = 9

DRAINAGE_BASINS = {
    'FR000001': 'Rhin-Meuse',
    'FR000002': 'Artois-Picardie',
    'FR000003': 'Seine-Normandie',
    'FR000004': 'Loire-Bretagne',
    'FR000005': 'Adour-Garonne',
    'FR000006': 'Rhône- Méditérannée',
    'FR000007': 'Corse',
    'FR000008': 'Guadeloupe',
    'FR000009': 'Martinique',
    'FR000010': 'Guyane',
    'FR000011': 'Réunion',
    'FR000012': 'Mayotte',
}


class Command(BaseCommand):
    """Import the list of drainage basins.

    This task is highly inefficient (no batch saving, updating every row one by
    one, etc.) but it will be ran only once, so it's not a big deal.

    The file can be downloaded at this address:
    http://www.data.eaufrance.fr/jdd/689a5b99-8d4e-488d-9305-c970b18ad64c
    """

    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs=1, type=str)

    def handle(self, *args, **options):

        for code, basin_name in DRAINAGE_BASINS.items():
            Perimeter.objects.create(
                scale=Perimeter.TYPES.basin,
                code=code,
                name=basin)


        csv_path = os.path.abspath(options['csv_file'])


    def import_epci_member(self, row_index):
        """Process a single line in the file.

        Every line describes one member (e.g a commune) for one EPCI.

        Hence, EPCI description is duplicated in several lines.

        """
        pass
