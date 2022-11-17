import factory
from factory.django import DjangoModelFactory

from django.utils.text import slugify

from programs.models import Program


class ProgramFactory(DjangoModelFactory):
    """Factory for programs."""

    class Meta:
        model = Program

    name = factory.Faker("name")
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
