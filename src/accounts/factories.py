import factory
from factory.django import DjangoModelFactory
from accounts.models import User


class UserFactory(DjangoModelFactory):
    """Factory for users."""

    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'DefaultPassword!')
    is_contributor = True
    is_beneficiary = True
    beneficiary_function = "other"
    beneficiary_role = "Compte de test"


class ContributorFactory(UserFactory):
    contributor_organization = factory.Faker('company')
    contributor_role = factory.Faker('job')
    contributor_contact_phone = factory.Faker('phone_number')
