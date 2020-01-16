import json

from django.db import transaction
from django.core.management.base import BaseCommand
from django.conf import settings

from geofr.models import Perimeter


DATA_PATH = '/node_modules/@etalab/decoupage-administratif/data/epci.json'


class Command(BaseCommand):
    """Import all epcis."""

    @transaction.atomic()
    def handle(self, *args, **options):

        france = Perimeter.objects.get(
            scale=Perimeter.TYPES.country,
            code='FRA')
        europe = Perimeter.objects.get(
            scale=Perimeter.TYPES.continent,
            code='EU')
        mainland = Perimeter.objects.get(
            scale=Perimeter.TYPES.adhoc,
            code='FRA-MET')
        overseas = Perimeter.objects.get(
            scale=Perimeter.TYPES.adhoc,
            code='FRA-OM')
        regions_qs = Perimeter.objects \
            .filter(scale=Perimeter.TYPES.region) \
            .values_list('code', 'id')
        regions = dict(regions_qs)
        departments_qs = Perimeter.objects \
            .filter(scale=Perimeter.TYPES.department) \
            .values_list('code', 'id')
        departments = dict(departments_qs)

        PerimeterContainedIn = Perimeter.contained_in.through
        perimeter_links = []

        data_file = settings.DJANGO_ROOT + DATA_PATH
        data = json.loads(data_file.read_file())
        nb_created = 0
        nb_updated = 0

        for entry in data:

            member_codes = [m['code'] for m in entry['membres']]
            members = Perimeter.objects.filter(code__in=member_codes)
            member_depts = []
            member_regions = []
            for member in members:
                member_depts += member.departments
                member_regions += member.regions

            epci_name = entry['nom']
            epci_code = entry['code']
            is_overseas = members[0].is_overseas

            epci, created = Perimeter.objects.update_or_create(
                scale=Perimeter.TYPES.epci,
                code=epci_code,
                defaults={
                    'name': epci_name,
                    'departments': list(set(member_depts)),
                    'regions': list(set(member_regions)),
                    'is_overseas': is_overseas,
                })
            if created:
                nb_created += 1
            else:
                nb_updated += 1

            # Link perimeter to france, europe, regions, departements,
            # "collectivités d'outre-mer", mainland / overseas, etc.
            perimeter_links.append(PerimeterContainedIn(
                from_perimeter_id=epci.id,
                to_perimeter_id=europe.id))
            perimeter_links.append(PerimeterContainedIn(
                from_perimeter_id=epci.id,
                to_perimeter_id=france.id))

            for region_code in epci.regions:
                perimeter_links.append(PerimeterContainedIn(
                    from_perimeter_id=epci.id,
                    to_perimeter_id=regions[region_code]))
            for department_code in epci.departments:
                perimeter_links.append(PerimeterContainedIn(
                    from_perimeter_id=epci.id,
                    to_perimeter_id=departments[department_code]))

            if epci.is_overseas:
                perimeter_links.append(PerimeterContainedIn(
                    from_perimeter_id=epci.id,
                    to_perimeter_id=overseas.id))
            else:
                perimeter_links.append(PerimeterContainedIn(
                    from_perimeter_id=epci.id,
                    to_perimeter_id=mainland.id))

            # Link epci members to the epci
            for member in members:
                perimeter_links.append(PerimeterContainedIn(
                    from_perimeter_id=member.id,
                    to_perimeter_id=epci.id))

        # Create the links between the perimeters
        PerimeterContainedIn.objects.bulk_create(
            perimeter_links, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS(
            '%d epci created, %d updated.' % (nb_created, nb_updated)))
