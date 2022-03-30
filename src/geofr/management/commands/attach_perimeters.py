import csv
import os
from django.core.management.base import BaseCommand

from geofr.models import Perimeter
from geofr.utils import attach_perimeters_classic

class Command(BaseCommand):
    """For every French department, check how many backers and programs have live aids"""

    def add_arguments(self, parser):
        parser.add_argument('--filename', type=str)
        parser.add_argument('--perimeter_id', type=int)

    def handle(self, *args, **options):
        file_path = os.path.abspath(options['filename'])
        with open(file_path) as f:
            lines = f.readlines()
            city_codes = []
            for line in lines:
                city_codes.append(line.strip())

        adhoc_perimeter = Perimeter.objects.get(id=options['perimeter_id'])
        attach_perimeters_classic(adhoc_perimeter, city_codes)
