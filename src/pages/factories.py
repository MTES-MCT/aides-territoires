import factory
from factory.django import DjangoModelFactory

from pages.models import Page, FaqCategory, FaqQuestionAnswer


class PageFactory(DjangoModelFactory):
    class Meta:
        model = Page

    title = factory.Faker("company")
    url = factory.Sequence(lambda n: "/page_{}/".format(n))


class FaqCategoryFactory(DjangoModelFactory):
    """Factory for FaqCategory."""

    class Meta:
        model = FaqCategory

    name = factory.Faker("company")


class FaqQuestionAnswerFactory(DjangoModelFactory):
    """Factory for FaqQuestionAnswer."""

    class Meta:
        model = FaqQuestionAnswer

    question = factory.Faker("text")
    answer = factory.Faker("text")
