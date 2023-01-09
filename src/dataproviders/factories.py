import factory
from factory.django import DjangoModelFactory


from dataproviders.models import DataSource
from accounts.factories import UserFactory
from backers.factories import BackerFactory


class DataSourceFactory(DjangoModelFactory):
    """Factory for projects."""

    class Meta:
        model = DataSource

    name = factory.Faker("company")
    backer = factory.SubFactory(BackerFactory)
    aid_author = factory.SubFactory(UserFactory)
