import factory
from factory.django import DjangoModelFactory
from organizations.models import Organization
from core.services.factory_utils import FuzzyMultipleChoice


class OrganizationFactory(DjangoModelFactory):
    """Factory for organizations."""

    class Meta:
        model = Organization

    name = factory.Faker("first_name")
    organization_type = FuzzyMultipleChoice(Organization.ORGANIZATION_TYPE_CHOICES)


class CommuneOrganizationFactory(DjangoModelFactory):
    """Factory for communes."""

    class Meta:
        model = Organization

    name = factory.Faker("first_name")
    organization_type = ["commune"]
    zip_code = 34080
    city_name = "Montpellier"
