import pytest

from organizations.factories import OrganizationFactory

pytestmark = pytest.mark.django_db


def test_organization_fill_extra_perimeters_on_save(perimeters):
    organization = OrganizationFactory()
    organization.perimeter = perimeters["montpellier"]
    organization.save()
    assert organization.perimeter_region == perimeters["occitanie"]
    assert organization.perimeter_department == perimeters["herault"]
