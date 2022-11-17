import factory
from factory.django import DjangoModelFactory
from django.utils.text import slugify

from categories.models import Theme, Category


class ThemeFactory(DjangoModelFactory):
    """Factory for themes."""

    class Meta:
        model = Theme

    name = factory.Faker("name")
    slug = factory.LazyAttribute(lambda o: slugify(o.name))


class CategoryFactory(DjangoModelFactory):
    """Factory for categories."""

    class Meta:
        model = Category

    name = factory.Faker("name")
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    theme = factory.SubFactory(ThemeFactory)
