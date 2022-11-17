import factory
from factory.django import DjangoModelFactory

from backers.models import Backer


class BackerFactory(DjangoModelFactory):
    """Factory for backer objects."""

    class Meta:
        model = Backer

    name = factory.Faker("company")

    @factory.post_generation
    def financed_aids(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for aid in extracted:
                self.financed_aids.add(aid)
