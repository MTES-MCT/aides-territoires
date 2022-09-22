from django.core.management.base import BaseCommand
from geofr.services.import_mayors import import_mayors


class Command(BaseCommand):
    """Import extra municipality data."""

    def handle(self, *args, **options):
        result = import_mayors()
        self.stdout.write(
            self.style.SUCCESS(
                f"""
                {result['nb_treated']} created or updated,
                {result['nb_not_treated']} not treated.
                """
            )
        )
