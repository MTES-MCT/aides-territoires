import logging
from django.core.management.base import BaseCommand
from projects.services.import_validated_projects import import_validated_projects


class Command(BaseCommand):
    help = "Import multiple validated projects from a distant csv"

    def add_arguments(self, parser):
        parser.add_argument("--url")

    def handle(self, *args, **options):
        csv_url = options["url"]

        logger = logging.getLogger("console_log")
        verbosity = int(options["verbosity"])
        if verbosity > 1:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        import_validated_projects(logger, csv_url=csv_url)
