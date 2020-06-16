import os
import csv

from django.core.management.base import BaseCommand

from geofr.models import Perimeter


class Command(BaseCommand):
    """Import the list of SCoTs.

    Our data source was manually transmitted and is a csv file with two columns:
    1 - Scot name
    2 - INSEE code of a perimeter that belongs to the scot.
    """

    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs=1, type=str)

    def handle(self, *args, **options):

        scots = {}

        # TODO Remote all "contained in" scot perimeter links

        # Import data from csv file
        csv_path = os.path.abspath(options['csv_file'][0])
        with open(csv_path) as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            for row in reader:
                scot_name = row[0]
                insee_code = row[1]

                if scot_name not in scots:
                    scots[scot_name] = []

                scots[scot_name].append(insee_code)

        for scot_name, codes in scots:
            scot_perimeters = Perimeter.objects.filter(code__in=codes)
            perimeter_ids = [p.id for p in scot_perimeters]

            scot_code = scot_name   # for now
            scot, created = Perimeter.objects.update_or_create(
                scale=Perimeter.TYPES.adhoc,
                code=scot_code,
                defaults={
                    'name': scot_name,
                })
