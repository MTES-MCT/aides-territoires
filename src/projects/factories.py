import factory
from factory.django import DjangoModelFactory

from django.utils.text import slugify

from projects.models import Project


class ProjectFactory(DjangoModelFactory):
    """Factory for projects."""

    class Meta:
        model = Project

    name = factory.Faker("company")
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    description = factory.Faker("text")
