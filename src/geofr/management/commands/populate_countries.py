from django.core.management.base import BaseCommand

from geofr.services.populate import populate_countries


class Command(BaseCommand):
    """Import the list of countries."""

    def handle(self, *args, **options):
        result = populate_countries()
        self.stdout.write(self.style.SUCCESS(
            f"{result['created']} created, {result['updated']} updated."
        ))
