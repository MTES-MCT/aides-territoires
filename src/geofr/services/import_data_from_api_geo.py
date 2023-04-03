import requests
from logging import Logger

from django.db import transaction

from geofr.models import Perimeter
from geofr.utils import list_insee_codes_for_departments_and_coms

"""
Imports data from API GEO

https://api.gouv.fr/documentation/api-geo

"""

ENDPOINT_URL = "https://geo.api.gouv.fr"


def api_call(api_url: str, payload: dict) -> dict:
    """The actual API call"""
    req = requests.get(api_url, params=payload)
    return req.json()


@transaction.atomic
def import_communes_extra_data(
    logger: Logger, departments_codes: list | None = None
) -> dict:
    """
    Import all data relative to communes that is not
    on our main source (see populate.py) :

    - post code (codesPostaux)
    - localization (centre/coordinates)
    - surface
    - codeEpci
    """
    if not departments_codes:
        departments_codes = list_insee_codes_for_departments_and_coms()

    total_treated = 0
    not_found = []
    for code in departments_codes:
        logger.debug(f"Importing data for department {code}")
        row_total_treated, row_not_found = get_extra_data_for_department(code)
        total_treated += row_total_treated
        not_found += row_not_found

    return {"nb_treated": total_treated, "not_found": not_found}


def get_extra_data_for_department(code: str) -> tuple:
    """Import the coordinates for the communes of said department"""
    api_url = f"{ENDPOINT_URL}/departements/{code}/communes"
    payload = {
        "fields": "nom,code,centre,codesPostaux,codeEpci,surface",
        "format": "json",
        "geometry": "centre",
    }

    result = api_call(api_url, payload)

    nb_treated = 0
    not_found = []
    for commune_entry in result:
        is_imported = import_commune_extra_data(commune_entry)
        if is_imported:
            nb_treated += 1
        else:
            not_found.append(f"{commune_entry['nom']} ({code})")

    return (nb_treated, not_found)


def import_commune_extra_data(commune_entry: dict) -> bool:
    insee = commune_entry["code"]

    # 2023 specific: Les Trois Lacs changed insee code, and the API is not
    # yet up to date
    if insee == "27058":
        insee = "27676"

    commune = Perimeter.objects.filter(
        code=insee, scale=Perimeter.SCALES.commune, is_obsolete=False
    ).first()

    coordinates = commune_entry["centre"]["coordinates"]

    if commune:
        commune.epci = commune_entry.get("codeEpci", "")
        commune.zipcodes = commune_entry["codesPostaux"]
        commune.longitude = coordinates[0]
        commune.latitude = coordinates[1]
        commune.surface = commune_entry.get("surface")

        commune.save()
        return True
    else:
        return False


@transaction.atomic
def import_communes_coordinates(
    logger: Logger, departments_codes: list | None = None
) -> dict:
    """Import specificially the geolocalisation data"""
    if not departments_codes:
        departments_codes = list_insee_codes_for_departments_and_coms()

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
            not_found.append(f"{commune_entry['nom']} ({code})")

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
