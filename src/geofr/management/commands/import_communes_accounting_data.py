from datetime import datetime
import logging

from django.core.management.base import BaseCommand
from geofr.services.import_data_from_ofgl import import_ofgl_accounting_data


class Command(BaseCommand):
    """Import municipal accounting data."""

    def add_arguments(self, parser):
        parser.add_argument(
            "--years",
            nargs="+",
            help="Import data for a specific year (eg 2021)",
        )

    def handle(self, *args, **options):
        start_time = datetime.now()
        logger = logging.getLogger("console_log")
        verbosity = int(options["verbosity"])
        if verbosity > 1:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        years = options["years"]

        if years:
            result = import_ofgl_accounting_data(years=years)
        else:
            result = import_ofgl_accounting_data

        end_time = datetime.now()

        logger.info(f"Population imported for {result['nb_communes']} communes.")
        logger.info(f"Import made in {end_time - start_time} seconds.")
