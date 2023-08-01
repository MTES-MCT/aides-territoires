import logging

from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand

logger = logging.getLogger("console_log")


class Command(BaseCommand):
    """
    Command to make the site use the local defined in the .env.local
    after a DB descent
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--site_path",
            type=str,
            help="The path to set",
        )

    def handle(self, *args, **options):
        site_path = options["site_path"]

        if site_path:
            print(site_path)
            site = Site.objects.first()
            site.domain = site_path
            site.save()

        logger.info(f"Site {site.id} domain set to {site_path}.")
