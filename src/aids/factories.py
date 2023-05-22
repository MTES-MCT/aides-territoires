import factory
from factory.django import DjangoModelFactory

from aids.models import Aid, SuggestedAidProject, AidProject
from core.services.factory_utils import FuzzyMultipleChoice
from accounts.factories import UserFactory
from projects.factories import ProjectFactory


class AidFactory(DjangoModelFactory):
    """Factory for aids."""

    class Meta:
        model = Aid

    name = factory.Faker("company", locale="fr_FR")
    author = factory.SubFactory(UserFactory)
    description = factory.Faker("text", locale="fr_FR")
    eligibility = factory.Faker("text", locale="fr_FR")
    mobilization_steps = FuzzyMultipleChoice(Aid.STEPS)
    origin_url = factory.Faker("url")
    targeted_audiences = FuzzyMultipleChoice(Aid.AUDIENCES)
    aid_types = FuzzyMultipleChoice(Aid.TYPES)
    destinations = FuzzyMultipleChoice(Aid.DESTINATIONS)
    contact = factory.Faker("name", locale="fr_FR")
    recurrence = "oneoff"
    status = "published"

    @factory.post_generation
    def financers(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for financer in extracted:
                self.financers.add(financer)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        obj = super()._create(model_class, *args, **kwargs)
        obj.set_search_vector_unaccented(financers=[])
        obj.save()
        return obj


class AidProjectFactory(DjangoModelFactory):
    """Factory for aidproject."""

    class Meta:
        model = AidProject

    aid = factory.SubFactory(AidFactory)
    project = factory.SubFactory(ProjectFactory)
    creator = factory.SubFactory(UserFactory)


class SuggestedAidProjectFactory(DjangoModelFactory):
    """Factory for suggestedaidproject."""

    class Meta:
        model = SuggestedAidProject

    aid = factory.SubFactory(AidFactory)
    project = factory.SubFactory(ProjectFactory)
    creator = factory.SubFactory(UserFactory)
