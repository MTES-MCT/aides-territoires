import factory
from factory.django import DjangoModelFactory

from backers.models import Backer


class BackerFactory(DjangoModelFactory):
    """Factory for backer objects."""

    class Meta:
        model = Backer

    name = factory.Faker('company')
