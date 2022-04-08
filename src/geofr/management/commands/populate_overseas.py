import json
import urllib.request

from django.core.management.base import BaseCommand
from django.db import transaction

from geofr.services.populate import populate_overseas


class Command(BaseCommand):
    """Populate overseas related perimeters."""

    @transaction.atomic
    def handle(self, *args, **options):
        result = populate_overseas()
        self.stdout.write(self.style.SUCCESS(
            f"{result['created']} created, {result['updated']} updated."
        ))
