import factory
from factory.django import DjangoModelFactory

from accounts.models import User


class UserFactory(DjangoModelFactory):
    """Factory for users."""

    class Meta:
        model = User

    full_name = factory.Faker('name')
    email = factory.Faker('email')
    password = 'pass'


class ContributorFactory(UserFactory):
    organization = factory.Faker('company')
    role = factory.Faker('job')
    contact_phone = factory.Faker('phone_number')
