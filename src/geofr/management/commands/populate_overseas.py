import json
import urllib.request

from django.core.management.base import BaseCommand
from django.db import transaction

from geofr.models import Perimeter

DATA_PATH = "https://unpkg.com/@etalab/decoupage-administratif/data/communes.json"


class Command(BaseCommand):
    """Populate overseas related perimeters."""

    @transaction.atomic
    def handle(self, *args, **options):

        france = Perimeter.objects.get(
            scale=Perimeter.SCALES.country,
            code='FRA')
        europe = Perimeter.objects.get(
            scale=Perimeter.SCALES.continent,
            code='EU')

        perimeter_links = []
        PerimeterContainedIn = Perimeter.contained_in.through

        # Create mainland perimeter
        mainland, _ = Perimeter.objects.update_or_create(
            scale=Perimeter.SCALES.adhoc,
            code='FRA-MET',
            defaults={
                'name': 'France métropolitaine',
                'is_overseas': False})

        # Link mainland to france and europe
        perimeter_links.append(PerimeterContainedIn(
            from_perimeter_id=mainland.id,
            to_perimeter_id=france.id))
        perimeter_links.append(PerimeterContainedIn(
            from_perimeter_id=mainland.id,
            to_perimeter_id=europe.id))

        # Link all mainland perimeters to `mainland`
        mainland_perimeters = Perimeter.objects \
            .filter(is_overseas=False) \
            .values_list('id', flat=True)
        for perimeter_id in mainland_perimeters:
            perimeter_links.append(PerimeterContainedIn(
                from_perimeter_id=perimeter_id,
                to_perimeter_id=mainland.id))

        # Create overseas perimeter
        overseas, _ = Perimeter.objects.update_or_create(
            scale=Perimeter.SCALES.adhoc,
            code='FRA-OM',
            defaults={
                'name': 'Outre-mer',
                'is_overseas': True})

        # Link overseas to france and europe
        perimeter_links.append(PerimeterContainedIn(
            from_perimeter_id=overseas.id,
            to_perimeter_id=france.id))
        perimeter_links.append(PerimeterContainedIn(
            from_perimeter_id=overseas.id,
            to_perimeter_id=europe.id))

        # Link all overseas perimeters to `overseas`
        overseas_perimeters = Perimeter.objects \
            .filter(is_overseas=True) \
            .values_list('id', flat=True)
        for perimeter_id in overseas_perimeters:
            perimeter_links.append(PerimeterContainedIn(
                from_perimeter_id=perimeter_id,
                to_perimeter_id=overseas.id))

        # Import the "collectivités d'Outre-Mer"
        with urllib.request.urlopen(DATA_PATH) as url:
            data = json.loads(url.read_file())
            coms = filter(lambda entry: 'collectiviteOutremer' in entry, data)
            for entry in coms:
                com, created = Perimeter.objects.update_or_create(
                    scale=Perimeter.SCALES.adhoc,
                    code=entry['collectiviteOutremer']['code'],
                    defaults={
                        'name': entry['collectiviteOutremer']['nom'],
                        'is_overseas': True
                    })
                perimeter_links.append(PerimeterContainedIn(
                    from_perimeter_id=com.id,
                    to_perimeter_id=overseas.id))
                perimeter_links.append(PerimeterContainedIn(
                    from_perimeter_id=com.id,
                    to_perimeter_id=france.id))
                perimeter_links.append(PerimeterContainedIn(
                    from_perimeter_id=com.id,
                    to_perimeter_id=europe.id))

            # Create the links between the perimeters
            PerimeterContainedIn.objects.bulk_create(
                perimeter_links, ignore_conflicts=True)
