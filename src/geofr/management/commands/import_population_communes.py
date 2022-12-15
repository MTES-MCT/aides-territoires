import logging

from django.core.management.base import BaseCommand
from geofr.services.import_population_communes import import_commune_data_from_banatic


class Command(BaseCommand):
    """Import extra municipality data."""

    def handle(self, *args, **options):
        logger = logging.getLogger("console_log")
        verbosity = int(options["verbosity"])
        if verbosity > 1:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        result = import_commune_data_from_banatic(logger)
        logger.info(f"Population imported for {result['nb_treated']} communes.")

        if len(result["not_found"]):
            logger.error("The following communes were not found in Aides-territoires:")
            for commune in result["not_found"]:
                logger.error(f"* {commune}")
