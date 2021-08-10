import json

from django.db import transaction
from django.core.management.base import BaseCommand
from django.conf import settings

from geofr.models import Perimeter
from geofr.constants import OVERSEAS_REGIONS


DATA_PATH = '/node_modules/@etalab/decoupage-administratif/data/regions.json'


class Command(BaseCommand):
    """Import the list of all regions."""

    @transaction.atomic()
    def handle(self, *args, **options):

        france = Perimeter.objects.get(
            scale=Perimeter.SCALES.country,
            code='FRA')
        europe = Perimeter.objects.get(
            scale=Perimeter.SCALES.continent,
            code='EU')

        PerimeterContainedIn = Perimeter.contained_in.through
        perimeter_links = []

        data_file = settings.DJANGO_ROOT + DATA_PATH
        data = json.loads(data_file.read_file())
        nb_created = 0
        nb_updated = 0

        for entry in data:

            # Create or update the region perimeters
            region, created = Perimeter.objects.update_or_create(
                scale=Perimeter.SCALES.region,
                code=entry['code'],
                defaults={
                    'name': entry['nom'],
                    'is_overseas': (entry['code'] in OVERSEAS_REGIONS),
                }
            )
            if created:
                nb_created += 1
            else:
                nb_updated += 1

            perimeter_links.append(PerimeterContainedIn(
                from_perimeter_id=region.id,
                to_perimeter_id=europe.id))
            perimeter_links.append(PerimeterContainedIn(
                from_perimeter_id=region.id,
                to_perimeter_id=france.id))

        # Create the links between the regions and France / Europe
        PerimeterContainedIn.objects.bulk_create(
            perimeter_links, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS(
            '%d regions created, %d updated.' % (nb_created, nb_updated)))
