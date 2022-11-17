from datetime import timedelta

import factory
from factory.django import DjangoModelFactory
from django.utils import timezone

from accounts.factories import UserFactory
from bookmarks.models import Bookmark


def two_weeks_ago():
    return timezone.now() - timedelta(days=14)


class BookmarkFactory(DjangoModelFactory):
    class Meta:
        model = Bookmark

    owner = factory.SubFactory(UserFactory)
    querystring = "text=ademe"
    send_email_alert = True
    alert_frequency = "weekly"
    latest_alert_date = factory.LazyFunction(two_weeks_ago)
