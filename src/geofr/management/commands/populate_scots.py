from django.core.management.base import BaseCommand

from geofr.services.populate_scots import populate_scots


class Command(BaseCommand):
    """Import the list of SCoTs."""

    def handle(self, *args, **options):
        result = populate_scots()
        self.stdout.write(self.style.SUCCESS(
            f"{result['created']} created, {result['updated']} updated, {result['obsolete']} obsolete."
        ))
