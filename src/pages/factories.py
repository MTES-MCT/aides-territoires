import factory
from factory.django import DjangoModelFactory

from pages.models import Page


class PageFactory(DjangoModelFactory):
    class Meta:
        model = Page

    title = factory.Faker("company")
    url = factory.Sequence(lambda n: "/page_{}/".format(n))
