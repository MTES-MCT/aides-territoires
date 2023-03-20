from django.db import transaction
from django.core.management.base import BaseCommand

from geofr.models import Perimeter
from organizations.models import Organization


class Command(BaseCommand):
    """Populate the Organization's inhabitants_number field when organization is a commune."""

    @transaction.atomic()
    def handle(self, *args, **options):
        nb_commune_modified = 0
        communes = (
            Organization.objects.filter(perimeter__scale=Perimeter.SCALES.commune)
            .filter(organization_type=["commune"])
            .exclude(inhabitants_number__isnull=False)
        )
        for commune in communes:
            commune.inhabitants_number = commune.perimeter.population
            commune.save()
            nb_commune_modified += 1

        self.stdout.write(
            self.style.SUCCESS(f"{nb_commune_modified} organizations modified.")
        )
