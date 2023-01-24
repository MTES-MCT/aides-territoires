import factory
from factory.django import DjangoModelFactory
from accounts.models import User


class UserFactory(DjangoModelFactory):
    """Factory for users."""

    class Meta:
        model = User
        django_get_or_create = ("email",)

    first_name = factory.Faker("first_name", locale="fr_FR")
    last_name = factory.Faker("last_name", locale="fr_FR")
    email = factory.Faker("email", locale="fr_FR")
    password = factory.PostGenerationMethodCall("set_password", "DefaultPassword!")
    is_contributor = True
    is_beneficiary = True
    beneficiary_function = "other"
    beneficiary_role = "Compte de test"


class ContributorFactory(UserFactory):
    contributor_organization = factory.Faker("company", locale="fr_FR")
    contributor_role = factory.Faker("job", locale="fr_FR")
    contributor_contact_phone = factory.Faker("phone_number", locale="fr_FR")
    email = "contributor@example.org"
    first_name = "Sample"
    last_name = "Contributor"
