import requests

from django.utils import timezone
from django.db import transaction

from geofr.constants import OVERSEAS_ALL, OVERSEAS_REGIONS, OVERSEAS_COLLECTIVITIES
from geofr.models import Perimeter, PerimeterData


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
def populate_countries() -> dict:

    nb_created = 0
    nb_updated = 0

    france, created = Perimeter.objects.update_or_create(
        scale=Perimeter.SCALES.country, code="FRA", name="France"
    )

    if created:
        nb_created += 1
    else:
        nb_updated += 1

    europe, created = Perimeter.objects.update_or_create(
        scale=Perimeter.SCALES.continent, code="EU", name="Europe"
    )

    if created:
        nb_created += 1
    else:
        nb_updated += 1

    PerimeterContainedIn = Perimeter.contained_in.through
    PerimeterContainedIn.objects.update_or_create(
        from_perimeter_id=france.id, to_perimeter_id=europe.id
    )

    return {"created": nb_created, "updated": nb_updated}


@transaction.atomic()
def populate_regions() -> dict:
    """Import the list of all regions."""

    france = Perimeter.objects.get(scale=Perimeter.SCALES.country, code="FRA")
    europe = Perimeter.objects.get(scale=Perimeter.SCALES.continent, code="EU")

    PerimeterContainedIn = Perimeter.contained_in.through
    perimeter_links = []

    response = requests.get(get_data_path("regions"))
    data = response.json()
    nb_created = 0
    nb_updated = 0

    for entry in data:
        insee_code = entry["code"]
        if insee_code not in OVERSEAS_COLLECTIVITIES:

            # Create or update the region perimeters
            region, created = Perimeter.objects.update_or_create(
                scale=Perimeter.SCALES.region,
                code=insee_code,
                defaults={
                    "name": entry["nom"],
                    "is_overseas": (insee_code in OVERSEAS_REGIONS),
                    "insee": insee_code,
                },
            )
            if created:
                nb_created += 1
            else:
                nb_updated += 1

            perimeter_links.append(
                PerimeterContainedIn(
                    from_perimeter_id=region.id, to_perimeter_id=europe.id
                )
            )
            perimeter_links.append(
                PerimeterContainedIn(
                    from_perimeter_id=region.id, to_perimeter_id=france.id
                )
            )

            # Add metadata
            _tl_item, _tl_created = PerimeterData.objects.update_or_create(
                perimeter=region,
                prop="type_liaison",
                defaults={"value": entry["typeLiaison"]},
            )

            _cl_item, _cl_created = PerimeterData.objects.update_or_create(
                perimeter=region,
                prop="chef_lieu",
                defaults={"value": entry["chefLieu"]},
            )

    # Create the links between the regions and France / Europe
    PerimeterContainedIn.objects.bulk_create(perimeter_links, ignore_conflicts=True)

    return {"created": nb_created, "updated": nb_updated}


@transaction.atomic()
def populate_departments() -> dict:
    """Import the list of all departments."""

    france = Perimeter.objects.get(scale=Perimeter.SCALES.country, code="FRA")
    europe = Perimeter.objects.get(scale=Perimeter.SCALES.continent, code="EU")
    regions_qs = Perimeter.objects.filter(scale=Perimeter.SCALES.region).values_list(
        "code", "id"
    )
    regions = dict(regions_qs)

    PerimeterContainedIn = Perimeter.contained_in.through
    perimeter_links = []

    response = requests.get(get_data_path("departements"))
    data = response.json()

    nb_created = 0
    nb_updated = 0

    for entry in data:
        insee_code = entry["code"]
        if insee_code not in OVERSEAS_COLLECTIVITIES:
            department, created = Perimeter.objects.update_or_create(
                scale=Perimeter.SCALES.department,
                code=insee_code,
                defaults={
                    "name": entry["nom"],
                    "regions": [entry["region"]],
                    "is_overseas": (entry["region"] in OVERSEAS_REGIONS),
                    "insee": insee_code,
                },
            )
            if created:
                nb_created += 1
            else:
                nb_updated += 1

            perimeter_links.append(
                PerimeterContainedIn(
                    from_perimeter_id=department.id, to_perimeter_id=europe.id
                )
            )
            perimeter_links.append(
                PerimeterContainedIn(
                    from_perimeter_id=department.id, to_perimeter_id=france.id
                )
            )
            for region_code in department.regions:
                perimeter_links.append(
                    PerimeterContainedIn(
                        from_perimeter_id=department.id,
                        to_perimeter_id=regions[region_code],
                    )
                )

            # Add metadata
            _tl_item, _tl_created = PerimeterData.objects.update_or_create(
                perimeter=department,
                prop="type_liaison",
                defaults={"value": entry["typeLiaison"]},
            )

            _cl_item, _cl_created = PerimeterData.objects.update_or_create(
                perimeter=department,
                prop="chef_lieu",
                defaults={"value": entry["chefLieu"]},
            )

    # Create the links between the regions and France / Europe
    PerimeterContainedIn.objects.bulk_create(perimeter_links, ignore_conflicts=True)

    return {"created": nb_created, "updated": nb_updated}


@transaction.atomic
def populate_overseas() -> None:
    france = Perimeter.objects.get(scale=Perimeter.SCALES.country, code="FRA")
    europe = Perimeter.objects.get(scale=Perimeter.SCALES.continent, code="EU")

    perimeter_links = []
    PerimeterContainedIn = Perimeter.contained_in.through

    # Create mainland perimeter
    mainland, _ = Perimeter.objects.update_or_create(
        scale=Perimeter.SCALES.adhoc,
        code="FRA-MET",
        defaults={"name": "France métropolitaine", "is_overseas": False},
    )

    # Link mainland to france and europe
    perimeter_links.append(
        PerimeterContainedIn(from_perimeter_id=mainland.id, to_perimeter_id=france.id)
    )
    perimeter_links.append(
        PerimeterContainedIn(from_perimeter_id=mainland.id, to_perimeter_id=europe.id)
    )

    # Link all mainland perimeters to `mainland`
    mainland_perimeters = Perimeter.objects.filter(is_overseas=False).values_list(
        "id", flat=True
    )
    for perimeter_id in mainland_perimeters:
        perimeter_links.append(
            PerimeterContainedIn(
                from_perimeter_id=perimeter_id, to_perimeter_id=mainland.id
            )
        )

    # Create overseas perimeter
    overseas, _ = Perimeter.objects.update_or_create(
        scale=Perimeter.SCALES.adhoc,
        code="FRA-OM",
        defaults={"name": "Outre-mer", "is_overseas": True},
    )

    # Link overseas to france and europe
    perimeter_links.append(
        PerimeterContainedIn(from_perimeter_id=overseas.id, to_perimeter_id=france.id)
    )
    perimeter_links.append(
        PerimeterContainedIn(from_perimeter_id=overseas.id, to_perimeter_id=europe.id)
    )

    # Link all overseas perimeters to `overseas`
    overseas_perimeters = Perimeter.objects.filter(is_overseas=True).values_list(
        "id", flat=True
    )
    for perimeter_id in overseas_perimeters:
        perimeter_links.append(
            PerimeterContainedIn(
                from_perimeter_id=perimeter_id, to_perimeter_id=overseas.id
            )
        )

    # Create the links between the perimeters
    PerimeterContainedIn.objects.bulk_create(perimeter_links, ignore_conflicts=True)


@transaction.atomic()
def populate_communes() -> dict:
    """Import the list of all communes."""

    start_time = timezone.now()

    france = Perimeter.objects.get(scale=Perimeter.SCALES.country, code="FRA")
    europe = Perimeter.objects.get(scale=Perimeter.SCALES.continent, code="EU")
    mainland = Perimeter.objects.get(scale=Perimeter.SCALES.adhoc, code="FRA-MET")
    overseas = Perimeter.objects.get(scale=Perimeter.SCALES.adhoc, code="FRA-OM")
    regions_qs = Perimeter.objects.filter(scale=Perimeter.SCALES.region).values_list(
        "code", "id"
    )
    regions = dict(regions_qs)
    departments_qs = Perimeter.objects.filter(
        scale=Perimeter.SCALES.department
    ).values_list("code", "id")
    departments = dict(departments_qs)
    adhoc_qs = Perimeter.objects.filter(scale=Perimeter.SCALES.adhoc).values_list(
        "code", "id"
    )
    adhoc = dict(adhoc_qs)

    PerimeterContainedIn = Perimeter.contained_in.through
    perimeter_links = []

    response = requests.get(get_data_path("communes"))
    data = response.json()

    nb_created = 0
    nb_updated = 0

    for entry in data:

        # There are several types of entries in the file:
        #  - communes
        #  - communes déléguées
        #  - arrondissements municipaux
        # At this stage, we only handle actual communes
        if entry["type"] != "commune-actuelle":
            continue

        region = entry["region"]
        is_overseas = region in OVERSEAS_ALL
        if region in OVERSEAS_COLLECTIVITIES:
            data = {
                "zipcodes": entry.get("codesPostaux", []),
                "is_overseas": is_overseas,
            }
        else:
            data = {
                "regions": [region],
                "departments": [entry["departement"]],
                "zipcodes": entry.get("codesPostaux", []),
                "is_overseas": is_overseas,
            }

        # Communes in COM don't have a Siren number in the source
        # Clipperton doesn't have a population value
        defaults = {
            "name": entry["nom"],
            "population": entry.get("population"),
            "insee": entry["code"],
            "siren": entry.get("siren", ""),
        }
        defaults.update(data)

        # Create or update the commune perimeter
        commune, created = Perimeter.objects.update_or_create(
            scale=Perimeter.SCALES.commune, code=entry["code"], defaults=defaults
        )
        if created:
            nb_created += 1
        else:
            nb_updated += 1

        # Add metadata
        if "typeLiaison" in entry:
            _tl_item, _tl_created = PerimeterData.objects.update_or_create(
                perimeter=commune,
                prop="type_liaison",
                defaults={"value": entry["typeLiaison"]},
            )

        # Link perimeter to france, europe, regions, departements,
        # "collectivités d'outre-mer", mainland / overseas, etc.
        perimeter_links.append(
            PerimeterContainedIn(
                from_perimeter_id=commune.id, to_perimeter_id=europe.id
            )
        )
        perimeter_links.append(
            PerimeterContainedIn(
                from_perimeter_id=commune.id, to_perimeter_id=france.id
            )
        )

        for region_code in commune.regions:
            perimeter_links.append(
                PerimeterContainedIn(
                    from_perimeter_id=commune.id,
                    to_perimeter_id=regions[region_code],
                )
            )
        for department_code in commune.departments:
            perimeter_links.append(
                PerimeterContainedIn(
                    from_perimeter_id=commune.id,
                    to_perimeter_id=departments[department_code],
                )
            )

        if commune.is_overseas:
            perimeter_links.append(
                PerimeterContainedIn(
                    from_perimeter_id=commune.id, to_perimeter_id=overseas.id
                )
            )
        else:
            perimeter_links.append(
                PerimeterContainedIn(
                    from_perimeter_id=commune.id, to_perimeter_id=mainland.id
                )
            )

        if region in OVERSEAS_COLLECTIVITIES:
            code = region
            perimeter_links.append(
                PerimeterContainedIn(
                    from_perimeter_id=commune.id, to_perimeter_id=adhoc[code]
                )
            )

    # Create the links between the perimeters
    PerimeterContainedIn.objects.bulk_create(perimeter_links, ignore_conflicts=True)

    nb_obsolete = Perimeter.objects.filter(date_updated__lt=start_time).count()
    Perimeter.objects.filter(date_updated__lt=start_time).filter(scale=1).update(
        is_obsolete=True, date_obsolete=start_time
    )

    return {"created": nb_created, "updated": nb_updated, "obsolete": nb_obsolete}


@transaction.atomic()
def populate_epcis() -> dict:
    """Import all epcis."""

    start_time = timezone.now()

    france = Perimeter.objects.get(scale=Perimeter.SCALES.country, code="FRA")
    europe = Perimeter.objects.get(scale=Perimeter.SCALES.continent, code="EU")
    mainland = Perimeter.objects.get(scale=Perimeter.SCALES.adhoc, code="FRA-MET")
    overseas = Perimeter.objects.get(scale=Perimeter.SCALES.adhoc, code="FRA-OM")
    regions_qs = Perimeter.objects.filter(scale=Perimeter.SCALES.region).values_list(
        "code", "id"
    )
    regions = dict(regions_qs)
    departments_qs = Perimeter.objects.filter(
        scale=Perimeter.SCALES.department
    ).values_list("code", "id")
    departments = dict(departments_qs)

    PerimeterContainedIn = Perimeter.contained_in.through
    perimeter_links = []

    response = requests.get(get_data_path("epci"))
    data = response.json()

    nb_created = 0
    nb_updated = 0

    for entry in data:
        member_codes = [m["code"] for m in entry["membres"]]
        members = Perimeter.objects.filter(code__in=member_codes)
        member_depts = []
        member_regions = []
        for member in members:
            member_depts += member.departments
            member_regions += member.regions

        epci_name = entry["nom"]
        epci_code = entry["code"]
        is_overseas = members[0].is_overseas

        epci, created = Perimeter.objects.update_or_create(
            scale=Perimeter.SCALES.epci,
            code=epci_code,
            defaults={
                "name": epci_name,
                "departments": list(set(member_depts)),
                "regions": list(set(member_regions)),
                "is_overseas": is_overseas,
                "siren": epci_code,
                "population": entry["populationTotale"],
            },
        )
        if created:
            nb_created += 1
        else:
            nb_updated += 1

        # Link perimeter to france, europe, regions, departements,
        # "collectivités d'outre-mer", mainland / overseas, etc.
        perimeter_links.append(
            PerimeterContainedIn(from_perimeter_id=epci.id, to_perimeter_id=europe.id)
        )
        perimeter_links.append(
            PerimeterContainedIn(from_perimeter_id=epci.id, to_perimeter_id=france.id)
        )

        for region_code in epci.regions:
            perimeter_links.append(
                PerimeterContainedIn(
                    from_perimeter_id=epci.id, to_perimeter_id=regions[region_code]
                )
            )
        for department_code in epci.departments:
            perimeter_links.append(
                PerimeterContainedIn(
                    from_perimeter_id=epci.id,
                    to_perimeter_id=departments[department_code],
                )
            )

        if epci.is_overseas:
            perimeter_links.append(
                PerimeterContainedIn(
                    from_perimeter_id=epci.id, to_perimeter_id=overseas.id
                )
            )
        else:
            perimeter_links.append(
                PerimeterContainedIn(
                    from_perimeter_id=epci.id, to_perimeter_id=mainland.id
                )
            )

        # Link epci members to the epci
        for member in members:
            perimeter_links.append(
                PerimeterContainedIn(
                    from_perimeter_id=member.id, to_perimeter_id=epci.id
                )
            )

        # Add metadata
        _type_item, _type_created = PerimeterData.objects.update_or_create(
            perimeter=epci,
            prop="type_epci",
            defaults={"value": entry["type"]},
        )

        _mf_item, _mf_created = PerimeterData.objects.update_or_create(
            perimeter=epci,
            prop="mode_financement",
            defaults={"value": entry["modeFinancement"]},
        )

    # Create the links between the perimeters
    PerimeterContainedIn.objects.bulk_create(perimeter_links, ignore_conflicts=True)

    nb_obsolete = Perimeter.objects.filter(date_updated__lt=start_time).count()
    Perimeter.objects.filter(date_updated__lt=start_time).filter(scale=5).update(
        is_obsolete=True, date_obsolete=start_time
    )

    return {
        "created": nb_created,
        "updated": nb_updated,
        "nb_obsolete": nb_obsolete,
    }
