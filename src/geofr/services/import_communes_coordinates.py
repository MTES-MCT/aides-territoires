import requests
from logging import Logger

from django.db import transaction

from geofr.models import Perimeter

"""
Imports the coordinates
Our data source comes from API GEO

https://api.gouv.fr/documentation/api-geo
"""

ENDPOINT_URL = "https://geo.api.gouv.fr"


@transaction.atomic
def import_communes_coordinates(logger: Logger) -> dict:
    departments_codes = Perimeter.objects.filter(
        scale=Perimeter.SCALES.department, is_obsolete=False
    ).values_list("code", flat=True)

    total_treated = 0
    not_found = []
    for code in departments_codes:
        row_total_treated, row_not_found = get_coordinates_for_department(code)
        total_treated += row_total_treated
        not_found += row_not_found

    return {"nb_treated": total_treated, "not_found": not_found}


def get_coordinates_for_department(code: str) -> tuple:
    api_url = f"{ENDPOINT_URL}/departements/{code}/communes"
    payload = {"fields": "nom,code,centre", "format": "json", "geometry": "centre"}
    req = requests.get(api_url, params=payload)

    result = req.json()

    nb_treated = 0
    not_found = []
    for commune_row in result:
        is_imported = import_commune_row_coordinates(commune_row)
        if is_imported:
            nb_treated += 1
        else:
            not_found.append(commune_row["nom"])

    return (nb_treated, not_found)


def import_commune_row_coordinates(commune_row: dict) -> bool:
    insee = commune_row["code"]
    coordinates = commune_row["centre"]["coordinates"]
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
