import pytest
import re
from unittest import mock

from geofr.models import Perimeter
from geofr.services.import_communes_population import (
    get_spreadsheet_content,
    import_row_from_banatic,
    match_filenames_in_zip,
)

pytestmark = pytest.mark.django_db


def test_import_row_from_banatic(client, perimeters) -> None:
    # Montpellier is in the sample perimeters, Mamoudzou is not
    import_montpellier = import_row_from_banatic("34172", 298933)
    import_mamoudzou = import_row_from_banatic("97611", 72974)

    assert import_montpellier is True
    assert import_mamoudzou is False

    commune = Perimeter.objects.get(code="34172")
    assert commune.population == 298933


def test_match_filenames_in_zip() -> None:
    MOCK_LISTING = [
        "Banatic_SirenInsee2011.xlsx",
        "Banatic_SirenInsee2014.xlsx",
        "Banatic_SirenInsee2015.xlsx",
        "Banatic_SirenInsee2021.xlsx",
    ]

    title_regex = re.compile(r"Banatic_SirenInsee(?P<year>\d{4})\.xlsx")
    with mock.patch("geofr.services.import_communes_population.ZipFile") as MockZipFile:
        MockZipFile.return_value.namelist.return_value = MOCK_LISTING
        zip_file = MockZipFile()

        annual_files = match_filenames_in_zip(zip_file, title_regex, starting_year=2014)
        expected_result = {
            2014: "Banatic_SirenInsee2014.xlsx",
            2015: "Banatic_SirenInsee2015.xlsx",
            2021: "Banatic_SirenInsee2021.xlsx",
        }
        assert annual_files == expected_result


def test_get_spreadsheet_content() -> None:
    with open("geofr/tests/samples/sample_banatic_sheet.xlsx", "rb") as xlsx_file:
        dataset = get_spreadsheet_content(xlsx_file, "insee_siren")

        assert dataset.headers == [
            "Reg_com",
            "dep_com",
            "siren",
            "insee",
            "nom_com",
            "ptot_2022",
            "pmun_2022",
            "pcap_2022",
        ]
        assert dataset.height == 4
