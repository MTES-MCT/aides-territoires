import json
import urllib.request

from django.db import transaction
from django.core.management.base import BaseCommand
from django.conf import settings

from geofr.models import Perimeter
from geofr.constants import OVERSEAS_REGIONS


class Command(BaseCommand):
    """Import the list of all communes."""

    @transaction.atomic()
    def handle(self, *args, **options):

        france = Perimeter.objects.get(
            scale=Perimeter.SCALES.country,
            code='FRA')
        europe = Perimeter.objects.get(
            scale=Perimeter.SCALES.continent,
            code='EU')
        mainland = Perimeter.objects.get(
            scale=Perimeter.SCALES.adhoc,
            code='FRA-MET')
        overseas = Perimeter.objects.get(
            scale=Perimeter.SCALES.adhoc,
            code='FRA-OM')
        regions_qs = Perimeter.objects \
            .filter(scale=Perimeter.SCALES.region) \
            .values_list('code', 'id')
        regions = dict(regions_qs)
        departments_qs = Perimeter.objects \
            .filter(scale=Perimeter.SCALES.department) \
            .values_list('code', 'id')
        departments = dict(departments_qs)
        adhoc_qs = Perimeter.objects \
            .filter(scale=Perimeter.SCALES.adhoc) \
            .values_list('code', 'id')
        adhoc = dict(adhoc_qs)

        PerimeterContainedIn = Perimeter.contained_in.through
        perimeter_links = []

        with urllib.request.urlopen("https://unpkg.com/@etalab/decoupage-administratif/data/communes.json") as url:
            data = json.loads(url.read_file())
            nb_created = 0
            nb_updated = 0

            for entry in data:

                # There are several types of entries in the file:
                #  - communes
                #  - communes déléguées
                #  - arrondissements municipaux
                # At this stage, we only handle communes
                if entry['type'] != 'commune-actuelle':
                    continue

                # In the files, actual communes can be of two types:
                # 1. Communes that belong in a region / department
                # 2. Communes from "collectivités d'Outre-mer"

                if 'region' in entry:
                    data = {
                        'regions': [entry['region']],
                        'departments': [entry['departement']],
                        'zipcodes': entry['codesPostaux'],
                        'is_overseas': (entry['region'] in OVERSEAS_REGIONS)
                    }
                else:
                    data = {
                        'zipcodes': entry.get('codesPostaux', []),
                        'is_overseas': True
                    }

                defaults = {
                    'name': entry['nom']
                }
                defaults.update(data)

                # Create or update the commune perimeter
                commune, created = Perimeter.objects.update_or_create(
                    scale=Perimeter.SCALES.commune,
                    code=entry['code'],
                    defaults=defaults)
                if created:
                    nb_created += 1
                else:
                    nb_updated += 1

                # Link perimeter to france, europe, regions, departements,
                # "collectivités d'outre-mer", mainland / overseas, etc.
                perimeter_links.append(PerimeterContainedIn(
                    from_perimeter_id=commune.id,
                    to_perimeter_id=europe.id))
                perimeter_links.append(PerimeterContainedIn(
                    from_perimeter_id=commune.id,
                    to_perimeter_id=france.id))

                for region_code in commune.regions:
                    perimeter_links.append(PerimeterContainedIn(
                        from_perimeter_id=commune.id,
                        to_perimeter_id=regions[region_code]))
                for department_code in commune.departments:
                    perimeter_links.append(PerimeterContainedIn(
                        from_perimeter_id=commune.id,
                        to_perimeter_id=departments[department_code]))

                if commune.is_overseas:
                    perimeter_links.append(PerimeterContainedIn(
                        from_perimeter_id=commune.id,
                        to_perimeter_id=overseas.id))
                else:
                    perimeter_links.append(PerimeterContainedIn(
                        from_perimeter_id=commune.id,
                        to_perimeter_id=mainland.id))

                if 'collectiviteOutremer' in entry:
                    code = entry['collectiviteOutremer']['code']
                    perimeter_links.append(PerimeterContainedIn(
                        from_perimeter_id=commune.id,
                        to_perimeter_id=adhoc[code]))

            # Create the links between the perimeters
            PerimeterContainedIn.objects.bulk_create(
                perimeter_links, ignore_conflicts=True)

            self.stdout.write(self.style.SUCCESS(
                '%d communes created, %d updated.' % (nb_created, nb_updated)))
