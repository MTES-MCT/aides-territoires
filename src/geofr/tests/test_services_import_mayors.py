import pytest
from geofr.models import Perimeter, PerimeterData
from geofr.services.import_mayors import insert_email_row, insert_mayor_row

pytestmark = pytest.mark.django_db


def test_insert_mayor_row(client, perimeters):

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
    result = insert_mayor_row(sample_commune)

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
    insert_mayor_row(sample_commune)

    mayor_first_name.refresh_from_db()
    mayor_last_name.refresh_from_db()

    assert mayor_first_name.value == "Michaël"
    assert mayor_last_name.value == "Nouveau Nom"

    assert PerimeterData.objects.count() == 2


def test_insert_email_row(client, perimeters):
    sample_commune = {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [3.896091, 43.5994487]},
        "properties": {
            "id": "mairie-34172-01",
            "codeInsee": "34172",
            "pivotLocal": "mairie",
            "nom": "Mairie - Montpellier",
            "adresses": [
                {
                    "type": "géopostale",
                    "lignes": ["1 place Georges-Frèche"],
                    "codePostal": "34267",
                    "commune": "Montpellier Cedex 2",
                    "coordonnees": [3.896091, 43.5994487],
                }
            ],
            "horaires": [
                {
                    "du": "lundi",
                    "au": "vendredi",
                    "heures": [{"de": "08:30:00", "a": "17:30:00"}],
                }
            ],
            "email": "mairie@ville-montpellier.fr",
            "telephone": "04 67 34 70 00",
            "url": "https://www.montpellier.fr",
            "zonage": {"communes": ["34172 Montpellier"]},
        },
    }

    montpellier = Perimeter.objects.get(name="Montpellier")

    # Import adds a PerimeterData entry
    result = insert_email_row(sample_commune)

    assert result is True

    mairie_email = PerimeterData.objects.get(
        perimeter=montpellier, prop="mairie_email"
    ).value

    assert mairie_email == "mairie@ville-montpellier.fr"
