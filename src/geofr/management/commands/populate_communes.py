from django.core.management.base import BaseCommand
from geofr.services.populate import populate_communes


class Command(BaseCommand):
    """Import the list of all communes."""

    def handle(self, *args, **options):
        result = populate_communes()
        self.stdout.write(
            self.style.SUCCESS(
                f"{result['created']} created, {result['updated']} updated."
            )
        )
