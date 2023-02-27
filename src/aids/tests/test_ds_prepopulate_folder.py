"""Test data prepared to send to Démarches-Simplifiées to prepopulate a folder."""

import pytest

from aids.factories import AidFactory
from aids.utils import prepopulate_ds_folder
from accounts.factories import UserFactory
from organizations.factories import OrganizationFactory
from accounts.models import User


pytestmark = pytest.mark.django_db


def test_data_json_is_populated_with_aid_ds_mapping_field_data(client):
    """Check the json-object constructed to send data to Démarches-Simplifiées"""

    ds_mapping_json = {
        "FieldsList": [
            {
                "ds_field_label": "Comment avez-vous connu Aides-territoires ?",
                "ds_field_id": "champ_Q2hhbXAtMjkzMzk3NQ==",
                "at_app": None,
                "at_model": None,
                "at_model_attr": None,
                "response_value": "Par Aides-territoires",
            },
            {
                "ds_field_label": "Nature du maître d'ouvrage",
                "ds_field_id": "champ_Q2hhbXAtMTk3NzQ0NQ==",
                "at_app": "organizations",
                "at_model": "Organization",
                "at_model_attr": "organization_type",
                "response_value": None,
                "choices_mapping": {
                    "commune": "Commune",
                    "epci": "EPCI",
                },
            },
            {
                "ds_field_label": "Nom du réprésentant légal",
                "ds_field_id": "champ_Q2hhbXAtMjkzNDM2MA==",
                "at_app": "accounts",
                "at_model": "User",
                "at_model_attr": "last_name",
                "response_value": None,
            },
            {
                "ds_field_label": "Prénom du réprésentant légal",
                "ds_field_id": "champ_Q2hhbXAtMjkzNDM2Mg==",
                "at_app": "accounts",
                "at_model": "User",
                "at_model_attr": "first_name",
                "response_value": None,
            },
            {
                "ds_field_label": "Fonction du réprésentant légal",
                "ds_field_id": "champ_Q2hhbXAtMjkzNDM2NA==",
                "at_app": "accounts",
                "at_model": "User",
                "at_model_attr": "beneficiary_function",
                "response_value": None,
            },
        ]
    }
    aid = AidFactory(ds_mapping=ds_mapping_json)
    organization = OrganizationFactory(organization_type=["epci"])
    user = UserFactory(
        first_name="Joseph",
        last_name="Rouletabille",
        email="joseph@rouletabille.org",
        beneficiary_function=User.FUNCTION_TYPE.mayor,
        beneficiary_organization=organization,
    )
    organization.beneficiaries.add(user)
    organization.save()

    data_well_formated = {
        "champ_Q2hhbXAtMjkzMzk3NQ==": "Par Aides-territoires",
        "champ_Q2hhbXAtMTk3NzQ0NQ==": "EPCI",
        "champ_Q2hhbXAtMjkzNDM2MA==": "Rouletabille",
        "champ_Q2hhbXAtMjkzNDM2Mg==": "Joseph",
        "champ_Q2hhbXAtMjkzNDM2NA==": "Maire",
    }

    print(data_well_formated)
    assert (
        prepopulate_ds_folder(aid.ds_mapping, user, organization) == data_well_formated
    )
