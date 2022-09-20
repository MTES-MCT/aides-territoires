from django.db import transaction
from django.core.management.base import BaseCommand

from geofr.services.populate import populate_departments


class Command(BaseCommand):
    """Import the list of all departments."""

    @transaction.atomic()
    def handle(self, *args, **options):
        result = populate_departments()
        self.stdout.write(
            self.style.SUCCESS(
                f"{result['created']} created, {result['updated']} updated."
            )
        )
