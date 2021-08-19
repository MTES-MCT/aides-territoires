import os
import csv

from django.core.management.base import BaseCommand

from geofr.models import Perimeter
from geofr.utils import attach_perimeters


class Command(BaseCommand):
    """Import the list of SCoTs.

    Our data source comes from the DGALN.
    https://docs.google.com/spreadsheets/d/15AyNPLNWQMxd7FHayHoQkxhEOSQE-lhp9zezphIXkHU/edit#gid=1277817401
    """

    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs=1, type=str)

    def handle(self, *args, **options):

        scots = {}
        nb_created = 0
        nb_updated = 0

        # TODO Remote all "contained in" scot perimeter links

        # Import data from csv file
        csv_path = os.path.abspath(options['csv_file'][0])
        with open(csv_path) as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            for row in reader:
                scot_id = row[0]
                scot_name = row[1]
                insee_code = row[2]

                if scot_id not in scots:
                    scots[scot_id] = {
                        'name': scot_name,
                        'communes': []
                    }

                scots[scot_id]['communes'].append(insee_code)

        for scot_id in scots.keys():

            # id is just an integer, we use a custom code to make it unique
            scot_code = 'SCOT-{}'.format(scot_id)
            scot_name = scots[scot_id]['name']

            # Create the scot perimeter
            scot, created = Perimeter.objects.update_or_create(
                scale=Perimeter.SCALES.adhoc,
                code=scot_code,
                defaults={
                    'name': scot_name,
                })
            if created:
                nb_created += 1
            else:
                nb_updated += 1

            # Link the scot with the related communes
            codes = scots[scot_id]['communes']
            attach_perimeters(scot, codes)

        self.stdout.write(self.style.SUCCESS(
            '%d scots created, %d updated.' % (nb_created, nb_updated)))
