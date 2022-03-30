import logging
import os
from django.core.management.base import BaseCommand

from geofr.models import Perimeter
from geofr.utils import attach_perimeters_classic


class Command(BaseCommand):
    """Attach perimeters that belong in a adhoc perimeter"""

    def add_arguments(self, parser):
        parser.add_argument("--filename", type=str)
        parser.add_argument("--perimeter_id", type=int)

    def handle(self, *args, **options):
        logger = logging.getLogger('console_log')
        verbosity = int(options["verbosity"])
        if verbosity > 1:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        logger.debug("Command attach_perimeters starting")

        file_path = os.path.abspath(options["filename"])
        with open(file_path) as f:
            lines = f.readlines()
            city_codes = []
            for line in lines:
                city_codes.append(line.strip())

        adhoc_perimeter = Perimeter.objects.get(id=options["perimeter_id"])
        logger.debug(
            f"Attaching perimeters for {adhoc_perimeter.name} ({adhoc_perimeter.id})"
        )
        attach_perimeters_classic(adhoc_perimeter, city_codes, logger)
