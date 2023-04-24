"""
Get data from the OFGL database at https://data.ofgl.fr

This is an implementation of OpenDataSoft.
"""

import logging
from django.db import transaction
from geofr.models import FinancialData, Perimeter, PerimeterData

from geofr.services.opendatasoft import OpenDataSoftAPI

logger = logging.getLogger("console_log")


@transaction.atomic
def import_ofgl_accounting_data(years: list = [2020, 2021]) -> dict:
    nb_created = 0
    nb_updated = 0
    nb_communes = 0

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


@transaction.atomic
def import_ofgl_accounting_data_for_year(year: int) -> dict:
    communes = Perimeter.objects.filter(
        scale=Perimeter.SCALES.commune, is_obsolete=False
    )

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
        "nb_communes": commune_counter,
        "nb_created_rows": nb_created,
        "nb_updated_rows": nb_updated,
    }


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
        insee_code = data["insee"]
        perimeter = Perimeter.objects.filter(
            scale=Perimeter.SCALES.commune, is_obsolete=False, insee=insee_code
        ).first()
        aggregate = data["agregat"]

        other_fields = {
            "insee_code": insee_code,
            "population_strata": data["tranche_population"],
            "main_budget_amount": data["montant_bp"],
        }

        if "ordre_affichage" in data:
            other_fields["display_order"] = data["ordre_affichage"]

        # Create or update the entry
        entry, created = FinancialData.objects.update_or_create(
            perimeter=perimeter,
            year=year,
            aggregate=aggregate,
            defaults=other_fields,
        )
        if created:
            nb_created += 1
        else:
            nb_updated += 1

        # Adding extra data to the commune itself
        if aggregate == "Recettes totales":
            keys = ["touristique", "qpv", "montagne"]

            for key in keys:
                value = True if data[key] == "Oui" else False

                datapoint, datapoint_created = PerimeterData.objects.update_or_create(
                    perimeter=perimeter,
                    prop=key,
                    defaults={"value": value},
                )

    return {"nb_created": nb_created, "nb_updated": nb_updated}
