import json

import pytest
from django.urls import reverse

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
    organization = OrganizationFactory()
    organization.perimeter = perimeters["montpellier"]
    organization.organization_type = ["commune"]
    organization.save()
    response = client.get(reverse("carto_stats"))
    assert response.status_code == 200
    assert response.context["regions_org_max"] == 1
    assert json.loads(response.context["regions_org_count"]) == {
        "Occitanie": 1,
        "Normandie": 0,
        "Nouvelle-Aquitaine": 0,
        "Corse": 0,
        "Bourgogne": 0,
    }
    assert response.context["departments_org_max"] == 1
    assert response.context["departments_codes"] == [
        "12",
        "19",
        "2A",
        "2B",
        "21",
        "28",
        "34",
    ]
    assert json.loads(response.context["departments_org_count"]) == {
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
    assert "date_created" in communes_with_org["34172-Montpellier"]
    assert "organization_name" in communes_with_org["34172-Montpellier"]
    assert "projects_count" in communes_with_org["34172-Montpellier"]
    assert "user_email" in communes_with_org["34172-Montpellier"]
    assert "age" in communes_with_org["34172-Montpellier"]
