import requests
from logging import Logger

from django.db import transaction

from geofr.models import Perimeter

"""
Imports data from API GEO

https://api.gouv.fr/documentation/api-geo

Currently only used for the coordinates
"""

ENDPOINT_URL = "https://geo.api.gouv.fr"


def api_call(api_url: str, payload: dict) -> dict:
    """The actual API call"""
    req = requests.get(api_url, params=payload)
    return req.json()


@transaction.atomic
def import_communes_coordinates(
    logger: Logger, departments_codes: list | None = None
) -> dict:
    if not departments_codes:
        departments_codes = list(
            Perimeter.objects.filter(
                scale=Perimeter.SCALES.department, is_obsolete=False
            ).values_list("code", flat=True)
        )

        # Add the COMs
        departments_codes.append("975")  # Saint-Pierre-et-Miquelon
        departments_codes.append("977")  # Saint-Barthélemy
        departments_codes.append("978")  # Saint-Martin
        departments_codes.append("984")  # TAAF
        departments_codes.append("986")  # Wallis et Futuna
        departments_codes.append("987")  # Polynésie française
        departments_codes.append("988")  # Nouvelle-Calédonie
        departments_codes.append("989")  # Clipperton

    total_treated = 0
    not_found = []
    for code in departments_codes:
        logger.debug(f"Importing data for department {code}")
        row_total_treated, row_not_found = get_coordinates_for_department(code)
        total_treated += row_total_treated
        not_found += row_not_found

    return {"nb_treated": total_treated, "not_found": not_found}


def get_coordinates_for_department(code: str) -> tuple:
    """Import the coordinates for the communes of said department"""
    api_url = f"{ENDPOINT_URL}/departements/{code}/communes"
    payload = {"fields": "nom,code,centre", "format": "json", "geometry": "centre"}

    result = api_call(api_url, payload)

    nb_treated = 0
    not_found = []
    for commune_entry in result:
        is_imported = import_commune_entry_coordinates(commune_entry)
        if is_imported:
            nb_treated += 1
        else:
            not_found.append(commune_entry["nom"])

    return (nb_treated, not_found)


def import_commune_entry_coordinates(commune_entry: dict) -> bool:
    insee = commune_entry["code"]
    coordinates = commune_entry["centre"]["coordinates"]
    try:
        commune = Perimeter.objects.get(
            code=insee, scale=Perimeter.SCALES.commune, is_obsolete=False
        )

        commune.longitude = coordinates[0]
        commune.latitude = coordinates[1]
        commune.save()
        return True
    except Perimeter.DoesNotExist:
        return False
