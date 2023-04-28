"""
Get data from the OFGL database at https://data.ofgl.fr

This is an implementation of OpenDataSoft.
"""

import csv
import logging

from django.db import transaction
from core.utils import download_file_to_tmp

from geofr.models import FinancialData, Perimeter, PerimeterData
from geofr.services.opendatasoft import OpenDataSoftAPI

logger = logging.getLogger("console_log")


def import_ofgl_accounting_data(
    years: list = [2020, 2021], csv_import: bool = False, skip_dl: bool = False
) -> dict:
    nb_created = 0
    nb_updated = 0
    nb_communes = 0

    if csv_import:
        # If the data is imported from a file, there should only be a single year
        year = years[0]
        result = import_ofgl_accounting_data_from_file(year, skip_dl)
        nb_created += result["nb_created_rows"]
        nb_updated += result["nb_updated_rows"]
        nb_communes += result["nb_communes"]

    else:
        for year in years:
            result = import_ofgl_accounting_data_for_year(year)

            nb_created += result["nb_created_rows"]
            nb_updated += result["nb_updated_rows"]
            nb_communes += result["nb_communes"]

    return {
        "nb_communes": nb_communes,
        "nb_created_rows": nb_created,
        "nb_updated_rows": nb_updated,
    }


def import_ofgl_accounting_data_from_file(year: int, skip_dl: bool):
    logger.info("Importing data from the CSV file")

    distant_file_name = f"ofgl-base-communes-consolidee-{year}.csv"
    local_file_name = "accounting_data.csv"
    if not skip_dl:
        logger.info("Downloading the CSV file")
        csv_path = download_file_to_tmp(distant_file_name, local_file_name)
    else:
        logger.info("Using the CSV file already in memory")
        local_folder = "tmp"
        csv_path = f"/{local_folder}/{local_file_name}"

    logger.debug("File downloaded")

    nb_created = 0
    nb_updated = 0
    aggregates = []

    field_names = {
        "insee": f"Code Insee {year} Commune",
        "agregat": "Agrégat",
        "tranche_population": f"Strate population {year}",
        "ordre_affichage": "ordre_affichage",
        "montant_bp": "Montant BP",
        "touristique": "Commune touristique",
        "qpv": "Présence QPV",
        "montagne": "Commune de montagne",
    }

    with open(csv_path) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";")

        row_counter = 0
        for row in reader:
            insee = row[f"Code Insee {year} Commune"]
            name = row[f"Nom {year} Commune"]
            aggregate = row["Agrégat"]

            if aggregate not in aggregates:
                aggregates.append(aggregate)
                logger.info(f"Parsing aggregate {aggregate}")

            row_counter += 1
            logger.debug(f"Parsing row {row_counter} — {aggregate} — {insee} ({name})")
            created = import_record_data(row, year, field_names)

            if created:
                nb_created += 1
            else:
                nb_updated += 1

    return {
        "row_counter": row_counter,
        "nb_created_rows": nb_created,
        "nb_updated_rows": nb_updated,
    }


def import_ofgl_accounting_data_for_year(year: int) -> dict:
    communes = Perimeter.objects.filter(
        scale=Perimeter.SCALES.commune, is_obsolete=False
    ).order_by("code")

    logger.info(f"** Importing data for year {year} **")

    nb_created = 0
    nb_updated = 0

    commune_counter = 0

    for commune in communes:
        logger.debug(f"- Importing data for commune {commune.name} ({commune.insee})")
        result = import_accounting_data_for_commune(insee=commune.insee, year=year)

        nb_created += result["nb_created"]
        nb_updated += result["nb_updated"]

        commune_counter += 1
        if commune_counter % 1000 == 0:
            logger.info(
                f"""{commune_counter} communes treated
                        ({nb_created} rows created,
                        {nb_updated} rows updated)"""
            )

    return {
        "row_counter": nb_created + nb_updated,
        "nb_created_rows": nb_created,
        "nb_updated_rows": nb_updated,
    }


@transaction.atomic
def import_accounting_data_for_commune(insee: str, year: int) -> dict:
    """
    Import the accounting data for a single commune for a given year
    (which represents 48 rows, one per aggregate)
    """
    ofgl_api = OpenDataSoftAPI(instance="https://data.ofgl.fr")

    dataset = "ofgl-base-communes-consolidee"

    payload = {
        "dataset": dataset,
        "rows": 50,
        "start": 0,
        "sort": ["exer"],
        "refine.exer": year,
        "refine.insee": insee,
        "format": "json",
        "timezone": "UTC",
    }

    records = ofgl_api.get_records(payload)

    nb_created = 0
    nb_updated = 0

    for record in records:
        data = record["fields"]
        created = import_record_data(data, year)

        if created:
            nb_created += 1
        else:
            nb_updated += 1

    return {"nb_created": nb_created, "nb_updated": nb_updated}


def import_record_data(data: dict, year: int, field_names: dict = {}):
    """
    Imports the data from a single row
    """

    insee_code = data[get_field_name(field_names=field_names, field="insee")]
    perimeter = Perimeter.objects.filter(
        scale=Perimeter.SCALES.commune, is_obsolete=False, insee=insee_code
    ).first()

    if not perimeter:
        logger.info(f"Perimeter not found in database: {insee_code}")
        return False

    aggregate = data[get_field_name(field_names=field_names, field="agregat")]

    other_fields = {
        "insee_code": insee_code,
        "population_strata": data[
            get_field_name(field_names=field_names, field="tranche_population")
        ],
        "main_budget_amount": data[
            get_field_name(field_names=field_names, field="montant_bp")
        ],
    }

    if "ordre_affichage" in data and data["ordre_affichage"]:
        other_fields["display_order"] = int(float(data["ordre_affichage"]))

    # Create or update the entry
    entry, created = FinancialData.objects.update_or_create(
        perimeter=perimeter,
        year=year,
        aggregate=aggregate,
        defaults=other_fields,
    )

    # Adding extra data to the commune itself
    if aggregate == "Recettes totales":
        keys = ["touristique", "qpv", "montagne"]

        for key in keys:
            field = get_field_name(field_names=field_names, field=key)
            value = True if data[field] == "Oui" else False

            datapoint, datapoint_created = PerimeterData.objects.update_or_create(
                perimeter=perimeter,
                prop=key,
                defaults={"value": value},
            )

    if created:
        return True
    else:
        return False


def get_field_name(field_names: dict, field: str) -> str:
    """
    The generated CSV has localized names, while the API does not.
    """
    if field in field_names:
        return field_names[field]
    else:
        return field
