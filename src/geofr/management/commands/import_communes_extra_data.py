import logging

from django.core.management.base import BaseCommand
from geofr.services.import_data_from_api_geo import import_communes_extra_data


class Command(BaseCommand):
    """Import extra municipality data."""

    def add_arguments(self, parser):
        parser.add_argument(
            "--departments",
            nargs="+",
            help='Department or COM codes like "2A" or "987"',
        )

    def handle(self, *args, **options):
        logger = logging.getLogger("console_log")
        verbosity = int(options["verbosity"])
        if verbosity > 1:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        departments_codes = options["departments"]

        if departments_codes:
            result = import_communes_extra_data(logger, departments_codes)
        else:
            result = import_communes_extra_data(logger)
        logger.info(f"Population imported for {result['nb_treated']} communes.")

        if len(result["not_found"]):
            logger.error("The following communes were not found in Aides-territoires:")
            for commune in result["not_found"]:
                logger.error(f"* {commune}")
