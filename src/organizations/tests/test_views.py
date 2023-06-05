import pytest

from django.urls import reverse

from organizations.models import Organization

pytestmark = pytest.mark.django_db


def test_organization_update_view_updates_the_org(client, contributor):

    user_org = contributor.beneficiary_organization

    client.force_login(contributor)

    params_url = reverse("organization_update_view", args=[user_org.id])

    res = client.post(
        params_url,
        {
            "organization_type": "epci",
            "intercommunality_type": "SM",
            "perimeter": user_org.id,
            "name": "Syndicat mixte du Pays des Champis",
            "address": "1 place de l’Hôtel de Ville",
            "city_name": "Champignac-en-Cambrousse",
            "zip_code": "12345",
            "siren_code": "200000669",
            "siret_code": "20000066900016",
            "ape_code": "8413Z",
        },
    )

    assert res.status_code == 302

    contributor.beneficiary_organization.refresh_from_db()

    updated_user_org = Organization.objects.get(id=user_org.id)

    assert updated_user_org.name == "Syndicat mixte du Pays des Champis"
    assert updated_user_org.intercommunality_type == "SM"
