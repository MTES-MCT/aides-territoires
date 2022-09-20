from django.core.management.base import BaseCommand

from geofr.services.populate import populate_epcis


class Command(BaseCommand):
    """Import all epcis."""

    def handle(self, *args, **options):
        result = populate_epcis()
        self.stdout.write(
            self.style.SUCCESS(
                f"{result['created']} created, {result['updated']} updated."
            )
        )
