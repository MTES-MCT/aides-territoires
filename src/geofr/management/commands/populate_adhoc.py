import os
import csv

from django.core.management.base import BaseCommand

from geofr.models import Perimeter
from geofr.utils import attach_perimeters


class Command(BaseCommand):
    """Import the list of Adhoc perimeters.

    Our data source:
    https://docs.google.com/spreadsheets/d/13G7hUL-zTqAWRNhz_Pz9sCEJXIrHrqjPO8rj6xP0Rck/edit#gid=50663560
    """

    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs=1, type=str)

    def get_clean_insee_code(self, raw_code):
        code = raw_code
        code = ''.join(c for c in code if c.isprintable())
        code = code.replace(' ', '')
        # Right justify padding to add 0 padding: Insee code is always at least 5 chars
        code = f'{code:0>5}'
        return code

    def handle(self, *args, **options):

        data = {}
        nb_created = 0
        nb_updated = 0

        csv_path = os.path.abspath(options['csv_file'][0])
        with open(csv_path) as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            next(reader, None)  # Skip header
            for row in reader:
                perimeter_id = row[0]
                perimeter_name = row[1]
                insee_code = row[2]
                if perimeter_id not in data:
                    data[perimeter_id] = {
                        'name': perimeter_name,
                        'communes': []
                    }
                insee_code = self.get_clean_insee_code(insee_code)
                try:
                    perimeter_to_attach = Perimeter.objects.get(code=insee_code)
                except Perimeter.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f"Pour le périmetre '{perimeter_name} - {perimeter_id}', "
                        f"le code insee n'existe pas dans la base de données : "
                        f"'{insee_code}'"))
                    continue
                # The perimeter to be attached that we found in the CSV file
                # could be a commune, but also an other type of perimeter,
                # for instance a EPCI, in that case, we need to lookup for
                # the commes that this perimeter contains.
                if perimeter_to_attach.scale != Perimeter.SCALES.commune:
                    communes = perimeter_to_attach.contains \
                        .filter(scale=Perimeter.SCALES.commune) \
                        .values_list('code', flat=True)
                else:
                    communes = [perimeter_to_attach.code]
                data[perimeter_id]['communes'].extend(communes)
        for perimeter_id in data.keys():
            perimeter_code = perimeter_id
            perimeter_name = data[perimeter_id]['name']
            # Create the perimeter or update if it's code exists
            perimeter, created = Perimeter.objects.update_or_create(
                scale=Perimeter.SCALES.adhoc,
                code=perimeter_code,
                defaults={
                    'name': perimeter_name,
                })
            if created:
                nb_created += 1
            else:
                nb_updated += 1
            codes = data[perimeter_id]['communes']
            # Link the perimeter with the related communes
            attach_perimeters(perimeter, codes)

        self.stdout.write(self.style.SUCCESS(
            '%d adhoc perimeters created, %d updated.' % (nb_created, nb_updated)))
