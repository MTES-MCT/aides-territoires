import factory
from faker import Faker
from factory.django import DjangoModelFactory

from tags.models import Tag


fake = Faker()


class TagFactory(DjangoModelFactory):
    """Factory for Tags."""

    class Meta:
        model = Tag

    @factory.sequence
    def name(n):
        return '{}{}'.format(fake.word(), n)
