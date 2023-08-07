import pytest
from accounts.factories import UserFactory
from accounts.templatetags.accounts import choices_display, sib_email_id
from organizations.factories import OrganizationFactory

pytestmark = pytest.mark.django_db


def test_choices_display(contributor):
    assert choices_display(contributor, "beneficiary_function") == "Autre"


def test_sib_email_id():
    empty_account = UserFactory()

    assert sib_email_id({"user": empty_account}) == ""

    commune_organization = OrganizationFactory(organization_type=["commune"])
    commune_account = UserFactory(
        email="commune@example.org", beneficiary_organization=commune_organization
    )

    assert sib_email_id({"user": commune_account}) == "commune@example.org"

    individual_organization = OrganizationFactory(organization_type=["individual"])
    individual_account = UserFactory(
        email="individual@example.org", beneficiary_organization=individual_organization
    )

    assert sib_email_id({"user": individual_account}) == ""
