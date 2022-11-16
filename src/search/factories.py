import factory
from factory.django import DjangoModelFactory
from django.utils.text import slugify

from search.models import SearchPage


class SearchPageFactory(DjangoModelFactory):
    class Meta:
        model = SearchPage

    title = factory.Faker("company")
    slug = factory.LazyAttribute(lambda o: slugify(o.title))
    content = factory.Faker("text")
    more_content = factory.Faker("text")
    search_querystring = "text=test"
