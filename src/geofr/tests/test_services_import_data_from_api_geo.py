import pytest

from unittest import mock

from geofr.models import Perimeter
from geofr.services.import_data_from_api_geo import (
    import_commune_entry_coordinates,
    get_coordinates_for_department,
    import_commune_extra_data,
)

pytestmark = pytest.mark.django_db


SAMPLE_COORDINATES = [
    {
        "nom": "Abeilhan",
        "code": "34001",
        "centre": {"type": "Point", "coordinates": [3.3026, 43.46]},
    },
    {
        "nom": "Béziers",
        "code": "34032",
        "centre": {"type": "Point", "coordinates": [3.2342, 43.3481]},
    },
    {
        "nom": "Montpellier",
        "code": "34172",
        "centre": {"type": "Point", "coordinates": [3.8742, 43.61]},
    },
    {
        "nom": "Vic-la-Gardiole",
        "code": "34333",
        "centre": {"type": "Point", "coordinates": [3.8046, 43.4838]},
    },
]

SAMPLE_COMMUNE_DATA = {
    "nom": "Montpellier",
    "code": "34172",
    "codesPostaux": ["34000", "34070", "34080", "34090"],
    "centre": {"type": "Point", "coordinates": [3.8742, 43.61]},
    "codeEpci": "243400017",
}


def test_import_commune_entry_coordinates(perimeters):
    result = import_commune_entry_coordinates(SAMPLE_COORDINATES[0])

    assert result is True

    abeilhan = Perimeter.objects.get(code="34001")

    assert abeilhan.longitude == 3.3026
    assert abeilhan.latitude == 43.46


def test_get_coordinates_for_department(perimeters) -> None:
    with mock.patch("geofr.services.import_data_from_api_geo.api_call") as MockApiCall:
        MockApiCall.return_value = SAMPLE_COORDINATES

        result = get_coordinates_for_department(code="34")

        assert result == (4, [])


def test_import_commune_extra_data(perimeters) -> None:
    result = import_commune_extra_data(SAMPLE_COMMUNE_DATA)

    montpellier = Perimeter.objects.get(code="34172")

    assert result is True

    assert montpellier.zipcodes == SAMPLE_COMMUNE_DATA["codesPostaux"]
    assert montpellier.epci == "243400017"
