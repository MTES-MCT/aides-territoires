import json

from django.db import transaction
from django.core.management.base import BaseCommand
from django.conf import settings

from geofr.models import Perimeter
from geofr.constants import OVERSEAS_REGIONS


DATA_PATH = '/node_modules/@etalab/decoupage-administratif/data/departements.json'  # noqa


class Command(BaseCommand):
    """Import the list of all departments."""

    @transaction.atomic()
    def handle(self, *args, **options):

        france = Perimeter.objects.get(
            scale=Perimeter.SCALES.country,
            code='FRA')
        europe = Perimeter.objects.get(
            scale=Perimeter.SCALES.continent,
            code='EU')
        regions_qs = Perimeter.objects \
            .filter(scale=Perimeter.SCALES.region) \
            .values_list('code', 'id')
        regions = dict(regions_qs)

        PerimeterContainedIn = Perimeter.contained_in.through
        perimeter_links = []

        data_file = settings.DJANGO_ROOT + DATA_PATH
        data = json.loads(data_file.read_file())
        nb_created = 0
        nb_updated = 0

        for entry in data:
            department, created = Perimeter.objects.update_or_create(
                scale=Perimeter.SCALES.department,
                code=entry['code'],
                defaults={
                    'name': entry['nom'],
                    'regions': [entry['region']],
                    'is_overseas': (entry['region'] in OVERSEAS_REGIONS)
                }
            )
            if created:
                nb_created += 1
            else:
                nb_updated += 1

            perimeter_links.append(PerimeterContainedIn(
                from_perimeter_id=department.id,
                to_perimeter_id=europe.id))
            perimeter_links.append(PerimeterContainedIn(
                from_perimeter_id=department.id,
                to_perimeter_id=france.id))
            for region_code in department.regions:
                perimeter_links.append(PerimeterContainedIn(
                    from_perimeter_id=department.id,
                    to_perimeter_id=regions[region_code]))

        # Create the links between the regions and France / Europe
        PerimeterContainedIn.objects.bulk_create(
            perimeter_links, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS(
            '%d departments created, %d updated.' % (nb_created, nb_updated)))
