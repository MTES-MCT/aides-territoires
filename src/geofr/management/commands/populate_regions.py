from django.core.management.base import BaseCommand

from geofr.services.populate import populate_regions

class Command(BaseCommand):
    """Import the list of all regions."""

    def handle(self, *args, **options):
        result = populate_regions()
        self.stdout.write(self.style.SUCCESS(
            f"{result['created']} created, {result['updated']} updated."
        ))
