import factory
from factory.django import DjangoModelFactory

from tags.models import Tag


class TagFactory(DjangoModelFactory):
    """Factory for Tags."""

    class Meta:
        model = Tag

    name = factory.Faker('name')
