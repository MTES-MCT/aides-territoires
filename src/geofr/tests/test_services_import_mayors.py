import pytest
from geofr.models import Perimeter, PerimeterData
from geofr.services.import_mayors import import_row

pytestmark = pytest.mark.django_db


def test_import_row(client, perimeters):

    sample_commune = {
        "Code du département": "34",
        "Libellé du département": "Hérault",
        "Code de la collectivité à statut particulier": "",
        "Libellé de la collectivité à statut particulier": "",
        "Code de la commune": "34172",
        "Libellé de la commune": "Montpellier",
        "Nom de l'élu": "DELAFOSSE",
        "Prénom de l'élu": "Michaël",
        "Code sexe": "M",
        "Date de naissance": "13/04/1977",
        "Code de la catégorie socio-professionnelle": "34",
        "Libellé de la catégorie socio-professionnelle": "Professeur, profession scientifique",
        "Date de début du mandat": "28/06/2020",
        "Date de début de la fonction": "09/07/2020",
    }
    montpellier = Perimeter.objects.get(name="Montpellier")

    # Import adds a PerimeterData entry
    result = import_row(sample_commune)

    assert result is True

    mayor_first_name = PerimeterData.objects.get(
        perimeter=montpellier, prop="mayor_first_name"
    )
    mayor_last_name = PerimeterData.objects.get(
        perimeter=montpellier, prop="mayor_last_name"
    )

    assert PerimeterData.objects.count() == 2
    assert mayor_first_name.value == "Michaël"
    assert mayor_last_name.value == "DELAFOSSE"

    # Importing a second time updates the already existing Perimeterdata entry
    sample_commune["Nom de l'élu"] = "Nouveau Nom"
    result = import_row(sample_commune)

    assert result is False

    mayor_first_name.refresh_from_db()
    mayor_last_name.refresh_from_db()

    assert mayor_first_name.value == "Michaël"
    assert mayor_last_name.value == "Nouveau Nom"

    assert PerimeterData.objects.count() == 2
