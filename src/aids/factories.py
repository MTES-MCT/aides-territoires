import factory
from factory import fuzzy
from factory.django import DjangoModelFactory

from aids.models import Aid
from accounts.factories import UserFactory
from backers.factories import BackerFactory


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
    backer = factory.SubFactory(BackerFactory)
    description = factory.Faker('text')
    eligibility = factory.Faker('text')
    diffusion_perimeter = Aid.PERIMETERS.france
    application_perimeter = fuzzy.FuzzyChoice(dict(Aid.PERIMETERS).keys())
    mobilization_steps = FuzzyMultipleChoice(Aid.STEPS)
    url = factory.Faker('url')
    targeted_audiances = FuzzyMultipleChoice(Aid.AUDIANCES)
    is_funding = factory.Faker('boolean')
    aid_types = FuzzyMultipleChoice(Aid.TYPES)
    destinations = FuzzyMultipleChoice(Aid.DESTINATIONS)
    thematics = FuzzyMultipleChoice(Aid.THEMATICS)
    contact_email = factory.Faker('email')
    contact_phone = factory.Faker('phone_number')
    publication_status = Aid.AID_STATUSES.open
    open_to_third_party = True
    status = Aid.STATUSES.published
