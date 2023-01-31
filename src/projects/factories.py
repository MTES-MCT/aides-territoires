import factory
from factory.django import DjangoModelFactory
from zoneinfo import ZoneInfo

from django.utils.text import slugify
from organizations.factories import CommuneOrganizationFactory

from projects.models import Project, ValidatedProject


class ProjectFactory(DjangoModelFactory):
    """Factory for projects."""

    class Meta:
        model = Project

    name = factory.Faker("company", locale="fr_FR")
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    description = factory.Faker("text", locale="fr_FR")


class ValidatedProjectFactory(DjangoModelFactory):
    """Factory for validated projects."""

    class Meta:
        model = ValidatedProject

    project_name = factory.Faker("company", locale="fr_FR")
    aid_name = factory.Faker("company", locale="fr_FR")
    financer_name = factory.Faker("company", locale="fr_FR")
    date_obtained = factory.Faker("date_time", tzinfo=ZoneInfo("UTC"))
    description = ""
    budget = factory.Faker("pyint", min_value=10000, max_value=100000)
    organization = factory.SubFactory(CommuneOrganizationFactory)
