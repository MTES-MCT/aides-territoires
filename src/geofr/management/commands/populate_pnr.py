import logging

from django.core.management.base import BaseCommand

from geofr.services.populate_pnr import populate_pnr


class Command(BaseCommand):
    """Import the list of Parcs naturels régionaux (PNR)."""

    def handle(self, *args, **options):
        logger = logging.getLogger("console_log")
        verbosity = int(options["verbosity"])
        if verbosity > 1:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        populate_pnr()
