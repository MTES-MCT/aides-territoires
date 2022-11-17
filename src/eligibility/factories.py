import factory
from factory.django import DjangoModelFactory

from eligibility.models import EligibilityTest, EligibilityQuestion


class EligibilityTestFactory(DjangoModelFactory):
    """Factory for eligibility test objects."""

    class Meta:
        model = EligibilityTest

    name = factory.Faker("name")


class EligibilityQuestionFactory(DjangoModelFactory):
    """Factory for eligibility question objects."""

    class Meta:
        model = EligibilityQuestion

    text = factory.Faker("text")
    answer_choice_a = factory.Faker("text")
    answer_choice_b = factory.Faker("text")
    answer_correct = "a"
