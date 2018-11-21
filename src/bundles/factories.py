import factory
from factory.django import DjangoModelFactory

from accounts.factories import UserFactory
from bundles.models import Bundle


class BundleFactory(DjangoModelFactory):
    """Factory for Bundles."""

    class Meta:
        model = Bundle

    owner = factory.SubFactory(UserFactory)
    name = factory.Faker('company')

    @factory.post_generation
    def aids(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for aid in extracted:
                self.aids.add(aid)
