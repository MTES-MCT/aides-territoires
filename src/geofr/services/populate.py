import json
import urllib.request

from django.db import transaction

from geofr.models import Perimeter
from geofr.constants import OVERSEAS_REGIONS


"""
This module contains functions used to populate the database of `Perimeter`
objects


We use Etalab's `decoupage-administratif` package which contains the raw
json data used by the geo API:

https://github.com/etalab/decoupage-administratif

The functions in this module MUST be idempotent, so running them several times
does not produce any side effect.

The fuctions MUST be able to create new Perimeters or update existing ones.

The functions MUST fill the `contained_in` fields for new perimeters.

The functions MUST NOT delete existing perimeters even if they are not listed
in the data files. They MAY mark those existing perimeters at a given level as
obsolete.

Also, most of those functions are written in a readable but very inefficient way,
because they are supposed to be ran at most once or twice a year. Indeed, the
raw data is unlikely to change very regularly.
"""

def get_data_path(fragment: str) -> str:
    return f"https://unpkg.com/@etalab/decoupage-administratif/data/{fragment}.json"


@transaction.atomic
def populate_countries() -> None:

    nb_created = 0
    nb_updated = 0

    france, created = Perimeter.objects.update_or_create(
        scale=Perimeter.SCALES.country,
        code='FRA',
        name='France')

    if created:
        nb_created += 1
    else:
        nb_updated += 1


    europe, created = Perimeter.objects.update_or_create(
        scale=Perimeter.SCALES.continent,
        code='EU',
        name='Europe')

    if created:
        nb_created += 1
    else:
        nb_updated += 1

    PerimeterContainedIn = Perimeter.contained_in.through
    PerimeterContainedIn.objects.update_or_create(
        from_perimeter_id=france.id,
        to_perimeter_id=europe.id)

    return {"created": nb_created, "updated": nb_updated}


@transaction.atomic()
def populate_regions() -> dict:
    """Import the list of all regions."""

    france = Perimeter.objects.get(
        scale=Perimeter.SCALES.country,
        code='FRA')
    europe = Perimeter.objects.get(
        scale=Perimeter.SCALES.continent,
        code='EU')

    PerimeterContainedIn = Perimeter.contained_in.through
    perimeter_links = []

    with urllib.request.urlopen(get_data_path("regions")) as url:
        data = json.loads(url.read().decode())
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

        return {"created": nb_created, "updated": nb_updated}


@transaction.atomic()
def populate_departments() -> dict:
    """Import the list of all departments."""

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

    with urllib.request.urlopen(get_data_path("departements")) as url:
        data = json.loads(url.read().decode())
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

        return {"created": nb_created, "updated": nb_updated}


@transaction.atomic
def populate_overseas() -> dict:

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
    with urllib.request.urlopen(get_data_path("communes")) as url:
        data = json.loads(url.read().decode())
        coms = filter(lambda entry: 'collectiviteOutremer' in entry, data)
        nb_created = 0
        nb_updated = 0

        for entry in coms:

            com, created = Perimeter.objects.update_or_create(
                scale=Perimeter.SCALES.adhoc,
                code=entry['collectiviteOutremer']['code'],
                defaults={
                    'name': entry['collectiviteOutremer']['nom'],
                    'is_overseas': True
                })

            if created:
                nb_created += 1
            else:
                nb_updated += 1

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

        return {"created": nb_created, "updated": nb_updated}


@transaction.atomic()
def populate_communes() -> dict:
    """Import the list of all communes."""

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

    with urllib.request.urlopen(get_data_path("communes")) as url:
        data = json.loads(url.read().decode())
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

        return {"created": nb_created, "updated": nb_updated}


@transaction.atomic()
def populate_epcis() -> dict:
    """Import all epcis."""

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

    PerimeterContainedIn = Perimeter.contained_in.through
    perimeter_links = []

    with urllib.request.urlopen(get_data_path("epci")) as url:
        data = json.loads(url.read().decode())
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
                scale=Perimeter.SCALES.epci,
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

        return {"created": nb_created, "updated": nb_updated}
