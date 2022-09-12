from django.db import transaction
from django.core.management.base import BaseCommand

from geofr.models import Perimeter
from organizations.models import Organization


class Command(BaseCommand):
    """Denormalize the Organization's relation to regions and departments."""

    @transaction.atomic()
    def handle(self, *args, **options):
        nb_organization_modified = 0
        for organization in Organization.objects.exclude(
            perimeter__isnull=True
        ).exclude(
            perimeter__scale__in=[
                Perimeter.SCALES.basin,
                Perimeter.SCALES.overseas,
                Perimeter.SCALES.mainland,
                Perimeter.SCALES.adhoc,
                Perimeter.SCALES.country,
                Perimeter.SCALES.continent,
            ]
        ):
            organization.save()
            nb_organization_modified += 1

        self.stdout.write(
            self.style.SUCCESS(f"{nb_organization_modified} organizations modified.")
        )
