import json

import pytest
from django.urls import reverse

from geofr.models import Perimeter
from geofr.factories import PerimeterFactory
from organizations.factories import OrganizationFactory

pytestmark = pytest.mark.django_db


def test_regular_users_cannot_access_cartographie(client, contributor):
    client.force_login(contributor)
    response = client.get(reverse("carto_stats"))
    assert response.status_code == 302
    assert response.url == "/?next=/stats/stats-cartographie/"


def test_admin_users_can_access_cartographie(client, superuser, perimeters):
    client.force_login(superuser)
    response = client.get(reverse("carto_stats"))
    assert response.status_code == 200
    assert "Statistiques sur carte" in response.content.decode()


def test_organizations_displayed_by_cartographie(client, superuser, perimeters):
    client.force_login(superuser)
    valfaunes = PerimeterFactory(
        scale=Perimeter.SCALES.epci,
        contained_in=[
            perimeters["europe"],
            perimeters["france"],
            perimeters["occitanie"],
            perimeters["herault"],
        ],
        is_overseas=False,
        name="Valflaunès",
        code="34322",
        regions=["76"],
        departments=["34"],
        basin="FR000006",
    )
    montpellier = perimeters["montpellier"]
    montpellier.contained_in.add(valfaunes)

    organization_commune = OrganizationFactory()
    organization_commune.perimeter = montpellier
    organization_commune.organization_type = ["commune"]
    organization_commune.save()

    organization_epci = OrganizationFactory()
    organization_epci.perimeter = valfaunes
    organization_epci.organization_type = ["epci"]
    organization_epci.save()
    response = client.get(reverse("carto_stats"))
    assert response.status_code == 200
    assert response.context["regions_org_communes_max"] == 1
    assert json.loads(response.context["regions_org_communes_count"]) == {
        "Occitanie": 1,
        "Normandie": 0,
        "Nouvelle-Aquitaine": 0,
        "Corse": 0,
        "Bourgogne": 0,
    }
    assert json.loads(response.context["regions_org_epcis_count"]) == {
        "Occitanie": 1,
        "Normandie": 0,
        "Nouvelle-Aquitaine": 0,
        "Corse": 0,
        "Bourgogne": 0,
    }
    assert response.context["departments_org_communes_max"] == 1
    assert response.context["departments_codes"] == [
        "12",
        "19",
        "2A",
        "2B",
        "21",
        "28",
        "34",
    ]
    assert json.loads(response.context["departments_org_communes_count"]) == {
        "Hérault": 1,
        "Aveyron": 0,
        "Eure": 0,
        "Corrèze": 0,
        "Corse-du-Sud": 0,
        "Haute-Corse": 0,
        "Côte-d’Or": 0,
    }
    assert json.loads(response.context["departments_org_epcis_count"]) == {
        "Hérault": 1,
        "Aveyron": 0,
        "Eure": 0,
        "Corrèze": 0,
        "Corse-du-Sud": 0,
        "Haute-Corse": 0,
        "Côte-d’Or": 0,
    }

    communes_with_org = json.loads(response.context["communes_with_org"])
    assert "34172-Montpellier" in communes_with_org
    communes_montpellier = communes_with_org["34172-Montpellier"]
    assert len(communes_montpellier) == 1
    assert "date_created" in communes_montpellier[0]
    assert "organization_name" in communes_montpellier[0]
    assert "projects_count" in communes_montpellier[0]
    assert "user_email" in communes_montpellier[0]
    assert "age" in communes_montpellier[0]

    epcis_with_org = json.loads(response.context["epcis_with_org"])
    assert "34172-Montpellier" in epcis_with_org
    communes_montpellier = epcis_with_org["34172-Montpellier"]
    assert len(communes_montpellier) == 1
    assert "date_created" in communes_montpellier[0]
    assert communes_montpellier[0]["organization_name"] == organization_epci.name
    assert "projects_count" in communes_montpellier[0]
    assert "user_email" in communes_montpellier[0]
    assert communes_montpellier[0]["age"] == 4
