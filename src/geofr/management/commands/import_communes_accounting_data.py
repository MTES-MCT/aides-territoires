from datetime import datetime
import logging

from django.core.management.base import BaseCommand
from geofr.services.import_data_from_ofgl import import_ofgl_accounting_data


class Command(BaseCommand):
    """Import municipal accounting data.

    When using file mode, the export file must be located in the bucket at
    the path "/resources/ofgl-base-communes-consolidee-xxxx.csv" and the
    years parameter must be specified with the year x
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--years",
            nargs="+",
            help="Import data for a specific year (eg 2021)",
        )
        parser.add_argument(
            "--csv",
            action="store_true",
            help="Import import from a CSV file instead of the API",
        )
        parser.add_argument(
            "--skipdl",
            action="store_true",
            help="Skip the download of the file and use the one already stored",
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
        csv_import = options["csv"]
        skip_dl = options["skipdl"]

        if years:
            result = import_ofgl_accounting_data(
                years=years, csv_import=csv_import, skip_dl=skip_dl
            )
        else:
            result = import_ofgl_accounting_data()

        end_time = datetime.now()

        logger.info(f"{result['row_counter']} rows imported.")
        logger.info(f"Import made in {end_time - start_time}.")
