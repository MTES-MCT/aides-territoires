import requests
import re
from zipfile import ZipFile, ZipExtFile
from io import BytesIO

from tablib.core import Databook, Dataset
from typing import Pattern

from logging import Logger
from django.db import transaction

from geofr.models import Perimeter

"""
Imports the population
Our data source comes from BANATIC
https://www.banatic.interieur.gouv.fr/V5/accueil/index.php

"""
MAYORS_URL = (
    "https://www.data.gouv.fr/fr/datasets/r/2876a346-d50c-4911-934e-19ee07b0e503"
)
EP_API = "https://etablissements-publics.api.gouv.fr/v3/"


@transaction.atomic
def import_commune_data_from_banatic(logger: Logger) -> dict:
    # Imports the Siren <-> Insee table for Communes
    # Communes must have been imported beforehand from COG

    zip_url = "https://www.banatic.interieur.gouv.fr/V5/ressources/documents/document_reference/TableCorrespondanceSirenInsee.zip"  # noqa
    logger.debug(f"Parsing archive {zip_url}")

    zip_name = requests.get(zip_url).content

    with ZipFile(BytesIO(zip_name)) as zip_file:
        title_regex = re.compile(r"Banatic_SirenInsee(?P<year>\d{4})\.xlsx")
        annual_files = match_filenames_in_zip(zip_file, title_regex, starting_year=2014)

        year = max(annual_files)

        logger.debug(f"Importing data for year {year}")

        result = {"nb_treated": 0, "not_found": []}

        with zip_file.open(annual_files[year]) as xlsx_file:
            dataset = get_spreadsheet_content(xlsx_file, "insee_siren")
            headers = dataset.headers

            for row in dataset:
                name = row[headers.index("nom_com")]
                insee = row[headers.index("insee")]
                population = row[headers.index(f"pmun_{year}")]

                row_result = import_row_from_banatic(insee, population)
                if row_result:
                    result["nb_treated"] += 1
                else:
                    result["not_found"].append(f"{name} ({insee})")

        return result


def import_row_from_banatic(insee: str, population: int) -> bool:
    try:
        commune = Perimeter.objects.get(code=insee)

        commune.population = population
        commune.save()
        return True
    except Perimeter.DoesNotExist:
        return False


def match_filenames_in_zip(
    zip_file: ZipFile, title_regex: Pattern[str], starting_year: int = 0
) -> dict:
    """List the filenames in the zip matching a specific regex"""
    files_in_zip = zip_file.namelist()
    annual_files = {}

    for f in files_in_zip:
        m = title_regex.match(f)
        if m:
            matched_year = int(m.group("year"))
            if matched_year >= starting_year:
                annual_files[matched_year] = f

    return annual_files


def get_spreadsheet_content(xlsx_file: ZipExtFile, spreasheet: str) -> Dataset:
    """Return the content of a specific spreasheet"""
    databook = Databook()
    imported_data = databook.load(xlsx_file.read(), format="xlsx")
    for dataset in imported_data.sheets():
        if dataset.title == spreasheet:
            return dataset
