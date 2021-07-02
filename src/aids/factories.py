import factory
from factory import fuzzy
from factory.django import DjangoModelFactory

from aids.models import Aid
from accounts.factories import UserFactory


class FuzzyMultipleChoice(fuzzy.BaseFuzzyAttribute):
    """Generate a random sub-sample of a list of choices."""

    def __init__(self, choices, **kwargs):
        self.choices = None
        self.choices_generator = choices
        super(FuzzyMultipleChoice, self).__init__(**kwargs)

    def fuzz(self):
        if self.choices is None:
            self.choices = [choice[0] for choice in self.choices_generator]

        sample_size = factory.random.randgen.randint(1, len(self.choices))
        return factory.random.randgen.sample(self.choices, sample_size)


class AidFactory(DjangoModelFactory):
    """Factory for aids."""

    class Meta:
        model = Aid

    name = factory.Faker('company')
    author = factory.SubFactory(UserFactory)
    description = factory.Faker('text')
    eligibility = factory.Faker('text')
    mobilization_steps = FuzzyMultipleChoice(Aid.STEPS)
    origin_url = factory.Faker('url')
    targeted_audiences = FuzzyMultipleChoice(Aid.AUDIENCES)
    aid_types = FuzzyMultipleChoice(Aid.TYPES)
    destinations = FuzzyMultipleChoice(Aid.DESTINATIONS)
    contact = factory.Faker('name')
    recurrence = 'oneoff'
    status = 'published'

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
