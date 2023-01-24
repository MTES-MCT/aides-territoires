from django.core.management.base import BaseCommand
from projects.services.import_validated_projects import import_validated_projects


class Command(BaseCommand):
    help = "Import multiple validated projects from a distant csv"

    def handle(self, *args, **options):
        import_validated_projects()
