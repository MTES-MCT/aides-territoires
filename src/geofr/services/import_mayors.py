from django.db import transaction
from django.utils import timezone

from geofr.models import Perimeter, PerimeterData

import csv
import requests
import io
from contextlib import closing


"""
Imports the list of mayors
Our data source comes from the Répertoire national des élus.
https://www.data.gouv.fr/fr/datasets/repertoire-national-des-elus-1/
"""
DATA_URL = "https://www.data.gouv.fr/fr/datasets/r/2876a346-d50c-4911-934e-19ee07b0e503"


@transaction.atomic
def import_mayors() -> dict:
    """
    Imports data abouts mayors of communes
    """
    nb_treated = 0
    nb_not_treated = 0

    # Parse the file
    with closing(requests.get(DATA_URL, stream=True)) as response:
        response.encoding = response.apparent_encoding
        file_data = io.StringIO(response.text)
        reader = csv.DictReader(file_data, delimiter="\t")
        for row in reader:
            created = import_row(row)
            if created is True:
                nb_treated += 1
            else:
                nb_not_treated += 1

    return {"nb_treated": nb_treated, "nb_not_treated": nb_not_treated}


def import_row(row: dict) -> bool:
    """
    Imports a row of the mayors list
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
