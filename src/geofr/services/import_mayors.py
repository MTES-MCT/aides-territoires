from django.db import transaction

from geofr.models import Perimeter, PerimeterData

import csv
import requests
import io
from contextlib import closing

"""
Imports the list of mayors
Our data source comes from the Répertoire national des élus for the mayors themselves
https://www.data.gouv.fr/fr/datasets/repertoire-national-des-elus-1/

Email of municipalities come from the API Établissements publics
https://api.gouv.fr/documentation/api_etablissements_publics
"""
MAYORS_URL = (
    "https://www.data.gouv.fr/fr/datasets/r/2876a346-d50c-4911-934e-19ee07b0e503"
)
EP_API = "https://etablissements-publics.api.gouv.fr/v3/"


@transaction.atomic
def import_mayors() -> dict:
    """
    Imports data abouts mayors of communes
    """
    nb_treated = 0
    nb_not_treated = 0

    # Parse the file
    with closing(requests.get(MAYORS_URL, stream=True)) as response:
        response.encoding = response.apparent_encoding
        file_data = io.StringIO(response.text)
        reader = csv.DictReader(file_data, delimiter="\t")
        for row in reader:
            created = insert_mayor_row(row)
            if created is True:
                nb_treated += 1
            else:
                nb_not_treated += 1

    return {"nb_treated": nb_treated, "nb_not_treated": nb_not_treated}


def insert_mayor_row(row: dict) -> bool:
    """
    Inserts a row of the mayors list
    """
    commune_insee = row["Code de la commune"]
    commune_name = row["Libellé de la commune"]
    mayor_first_name = row["Prénom de l'élu"]
    mayor_last_name = row["Nom de l'élu"]

    matching_perimeters = Perimeter.objects.filter(
        code=commune_insee, scale=Perimeter.SCALES.commune, is_obsolete=False
    )

    if matching_perimeters.count() == 1:
        commune_perimeter = matching_perimeters.first()

        first_name_item, first_name_created = PerimeterData.objects.update_or_create(
            perimeter=commune_perimeter,
            prop="mayor_first_name",
            defaults={"value": mayor_first_name},
        )
        last_name_item, last_name_created = PerimeterData.objects.update_or_create(
            perimeter=commune_perimeter,
            prop="mayor_last_name",
            defaults={"value": mayor_last_name},
        )

        return True

    elif matching_perimeters.count() == 0:
        print(
            f"WARNING: Commune perimeter not found for row {commune_name} ({commune_insee})"
        )
    else:
        print(
            f"WARNING: several Commune perimeters found for row {commune_name} ({commune_insee})"
        )

    return False


def import_emails_of_municipalities():
    """
    Imports emails from the établissements publics API
    """
    nb_treated = 0
    nb_not_treated = 0

    departments = Perimeter.objects.filter(
        scale=Perimeter.SCALES.department, is_obsolete=False
    )

    for department in departments:
        print(f"Retrieving data for department {department.name} ({department.code})")
        endpoint_url = f"{EP_API}departements/{department.code}/mairie"

        response = requests.get(url=endpoint_url)
        data = response.json()

        communes = data["features"]
        print(f"{len(communes)} found, processing...")
        for commune in communes:
            created = insert_email_row(commune)

            if created is True:
                nb_treated += 1
            else:
                nb_not_treated += 1

    return {"nb_treated": nb_treated, "nb_not_treated": nb_not_treated}


def insert_email_row(commune: dict) -> bool:
    """
    Inserts a row for the email of the mayor
    """
    commune_insee = commune["properties"]["codeInsee"]
    mairie_name = commune["properties"]["nom"]

    if "email" in commune["properties"]:
        mairie_email = commune["properties"]["email"]

        matching_perimeters = Perimeter.objects.filter(
            code=commune_insee, scale=Perimeter.SCALES.commune, is_obsolete=False
        )

        if matching_perimeters.count() == 1:
            commune_perimeter = matching_perimeters.first()

            email_item, email_created = PerimeterData.objects.update_or_create(
                perimeter=commune_perimeter,
                prop="mairie_email",
                defaults={"value": mairie_email},
            )

            return True

        elif matching_perimeters.count() == 0:
            print(
                f"WARNING: Commune perimeter not found for row {mairie_name} ({commune_insee})"
            )
        else:
            print(
                f"WARNING: several Commune perimeters found for row {mairie_name} ({commune_insee})"
            )
    else:
        f"WARNING: the commune {mairie_name} has no registered email address"

    return False
