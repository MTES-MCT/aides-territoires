import factory
from factory.django import DjangoModelFactory

from accounts.factories import UserFactory

from notifications.models import Notification


class NotificationFactory(DjangoModelFactory):
    """Factory for notification."""

    class Meta:
        model = Notification

    recipient = factory.SubFactory(UserFactory)
    notification_type = "other"
    title = factory.Faker("text", locale="fr_FR")
    message = factory.Faker("text", locale="fr_FR")
