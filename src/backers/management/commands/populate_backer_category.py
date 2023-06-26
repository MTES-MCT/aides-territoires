import logging

from django.core.management.base import BaseCommand

from backers.services.populate_backer_category import (
    create_backer_category,
    create_and_attached_backer_subcategory,
    attached_backer_group_to_subcategory,
)


class Command(BaseCommand):
    """Import the list of BackerCategories and BackerSubCategories."""

    def handle(self, *args, **options):
        logger = logging.getLogger("console_log")
        verbosity = int(options["verbosity"])
        if verbosity > 1:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        create_backer_category()
        create_and_attached_backer_subcategory()
        attached_backer_group_to_subcategory()
