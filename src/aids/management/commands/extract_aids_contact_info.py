from datetime import datetime
import logging

from django.core.management.base import BaseCommand
from aids.services.contacts import extract_aids_contact_info


class Command(BaseCommand):
    """
    Find the emails and phone numbers of aids contacts.
    """

    def handle(self, *args, **options):
        start_time = datetime.now()
        logger = logging.getLogger("console_log")
        verbosity = int(options["verbosity"])
        if verbosity > 1:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        extract_aids_contact_info()

        end_time = datetime.now()

        logger.info(f"Command ran in {end_time - start_time}.")
