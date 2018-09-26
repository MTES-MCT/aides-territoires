import os
import csv

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

OVERSEAS_BASINS = ('FR000008', 'FR000009', 'FR000010', 'FR000011', 'FR000012')


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

        # Create basin perimeters
        basin_to_commune = {}
        basin_to_epci = {}
        for code, basin_name in DRAINAGE_BASINS.items():
            Perimeter.objects.get_or_create(
                scale=Perimeter.TYPES.basin,
                code=code,
                name=basin_name,
                is_overseas=code in OVERSEAS_BASINS)
            basin_to_commune[code] = list()
            basin_to_epci[code] = list()

        # Import data from csv file
        csv_path = os.path.abspath(options['csv_file'][0])
        with open(csv_path) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',')
            for row in reader:
                commune_code = row['CdCommune']
                basin_code = row['CdComiteBassin']
                basin_to_commune[basin_code].append(commune_code)

        # Update communes with the correct basin codes
        for basin_code in basin_to_commune.keys():
            Perimeter.objects \
                .filter(scale=Perimeter.TYPES.commune) \
                .filter(code__in=basin_to_commune[basin_code]) \
                .update(basin=basin_code)

        # Update epcis with basin codes
        epcis = Perimeter.objects \
            .filter(scale=Perimeter.TYPES.commune) \
            .values_list('epci', 'basin')
        for epci_code, basin_code in epcis:
            basin_to_epci[basin_code].append(epci_code)

        for basin_code in basin_to_epci.keys():
            Perimeter.objects \
                .filter(scale=Perimeter.TYPES.epci) \
                .filter(code__in=basin_to_epci[basin_code]) \
                .update(basin=basin_code)
