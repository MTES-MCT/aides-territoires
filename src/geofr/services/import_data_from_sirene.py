"""
Get data about public structures from an export file of the Sirene database.

The file is generated through
https://www.sirene.fr/sirene/public/creation-fichier#activite-principale

with the following parameters:
- État administratif des établissements: Établissements actifs
- Type d’établissement: L’établissement siège seulement
- Liste de siren/siret:
    - 84.11Z - Administration publique générale
    - 84.13Z - Administration publique (tutelle) des activités économiques

The extracted data is:
- SIRET number of the headquarters
- APE code
- Postal address of the headquarters
"""
import csv
import requests
import io
import logging
from contextlib import closing

from django.conf import settings
from django.db import transaction

from geofr.models import Perimeter, PerimeterData

logger = logging.getLogger("console_log")


def get_source_file_url() -> str:
    cloud_root = getattr(settings, "AWS_S3_ENDPOINT_URL", "")
    bucket_name = getattr(settings, "AWS_STORAGE_BUCKET_NAME", "")
    file_name = "siren-etablissements-publics.csv"
    return f"{cloud_root}/{bucket_name}/resources/{file_name}"


@transaction.atomic
def import_sirene_data() -> dict:
    file_url = get_source_file_url()

    siren_entries = {}

    with closing(requests.get(file_url, stream=True)) as response:
        response.encoding = response.apparent_encoding
        file_data = io.StringIO(response.text)
        reader = csv.DictReader(file_data)
        for row in reader:
            siren = row["siren"]
            siren_entries[siren] = row

    perimeters_qs = Perimeter.objects.filter(
        is_obsolete=False, siren__isnull=False
    ).exclude(siren__exact="")

    missing_entries = []
    counter = 0

    for perimeter in perimeters_qs:
        if perimeter.siren in siren_entries:
            entry = siren_entries[perimeter.siren]
            import_siret_for_perimeter(perimeter, entry)
            counter += 1

            if counter % 1000 == 0:
                logger.info(f"{counter} rows treated")
        else:
            missing_entries.append(f"{perimeter} - {perimeter.siren}")

    return {"missing_entries": missing_entries, "counter": counter}


def import_siret_for_perimeter(perimeter: Perimeter, entry: dict) -> None:
    perimeter.siret = entry["siret"]
    perimeter.save()

    address_parts = {
        entry["numeroVoieEtablissement"],
        entry["indiceRepetitionEtablissement"],
        entry["typeVoieEtablissement"],
        entry["libelleVoieEtablissement"],
    }
    address_street = " ".join(filter(None, address_parts))

    if address_street:
        address_item, address_created = PerimeterData.objects.update_or_create(
            perimeter=perimeter,
            prop="address_street",
            defaults={"value": address_street},
        )

    if entry["codePostalEtablissement"]:
        zipcode_item, zipcode_created = PerimeterData.objects.update_or_create(
            perimeter=perimeter,
            prop="address_zipcode",
            defaults={"value": entry["codePostalEtablissement"]},
        )

    if entry["libelleCommuneEtablissement"]:
        city_item, city_created = PerimeterData.objects.update_or_create(
            perimeter=perimeter,
            prop="address_city_name",
            defaults={"value": entry["libelleCommuneEtablissement"]},
        )

    if entry["activitePrincipaleUniteLegale"]:
        ape_item, ape_created = PerimeterData.objects.update_or_create(
            perimeter=perimeter,
            prop="ape_code",
            defaults={"value": entry["activitePrincipaleUniteLegale"]},
        )
