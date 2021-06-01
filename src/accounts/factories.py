import factory
from factory.django import DjangoModelFactory

from accounts.models import User


class UserFactory(DjangoModelFactory):
    """Factory for users."""

    class Meta:
        model = User

    first_name = factory.Faker('name')
    last_name = factory.Faker('name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'pass')
    is_contributor = True


class ContributorFactory(UserFactory):
    organization = factory.Faker('company')
    role = factory.Faker('job')
    contact_phone = factory.Faker('phone_number')
