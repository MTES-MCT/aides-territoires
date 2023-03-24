from django.core.management.base import BaseCommand
from geofr.services.import_sirets import import_sirets


class Command(BaseCommand):
    """Import extra municipality data."""

    def handle(self, *args, **options):
        result = import_sirets()
        self.stdout.write(
            self.style.SUCCESS(f"{result['counter']} entries added or updated.")
        )
        if result["missing_entries"]:
            self.stdout.write(self.style.WARNING("Missing entries:"))
            for me in result["missing_entries"]:
                self.stdout.write(self.style.WARNING(me))
