import logging
from django.core.management.base import BaseCommand
from django.utils import timezone

from geofr.models import PerimeterImport
from geofr.utils import attach_perimeters


class Command(BaseCommand):
    """Attach perimeters that belong in a adhoc perimeter"""

    def handle(self, *args, **options):
        logger = logging.getLogger('console_log')
        verbosity = int(options["verbosity"])
        if verbosity > 1:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        logger.debug("Command attach_perimeters starting")

        perimeters_to_import = PerimeterImport.objects.filter(is_imported=False)

        for perimeter_to_import in perimeters_to_import:
            logger.info(
                f"Attaching perimeters for {perimeter_to_import}"
            )
            attach_perimeters(
                perimeter_to_import.adhoc_perimeter,
                perimeter_to_import.city_codes,
                logger)

            perimeter_to_import.is_imported = True
            perimeter_to_import.date_imported = timezone.now()
            perimeter_to_import.save()
