from datetime import timedelta

import factory
from factory.django import DjangoModelFactory
from django.utils import timezone

from alerts.models import Alert


def two_weeks_ago():
    return timezone.now() - timedelta(days=14)


class AlertFactory(DjangoModelFactory):
    class Meta:
        model = Alert

    email = factory.Faker("email")
    querystring = "text=ademe"
    alert_frequency = "weekly"
    validated = True
    date_validated = factory.LazyFunction(two_weeks_ago)
    latest_alert_date = factory.LazyFunction(two_weeks_ago)
