import pytest
from datetime import timedelta

from django.utils import timezone

from aids.factories import Aid, AidFactory


pytestmark = pytest.mark.django_db


@pytest.fixture
def next_month():
    today = timezone.now().date()
    return today + timedelta(days=30)


@pytest.fixture
def next_week():
    today = timezone.now().date()
    return today + timedelta(days=7)


@pytest.fixture
def last_month():
    today = timezone.now().date()
    return today - timedelta(days=30)


def test_open_filter(last_month, next_month):
    """Test the `open` queryset filter."""

    # Those aids must be considered `open`
    AidFactory(submission_deadline=timezone.now().date())
    AidFactory(submission_deadline=next_month)
    AidFactory(submission_deadline=None)
    AidFactory(submission_deadline=last_month, recurrence="ongoing")
    assert Aid.objects.open().count() == 4

    # Those aids must not be considered `open`
    AidFactory(submission_deadline=last_month, recurrence="oneoff")
    AidFactory(submission_deadline=last_month, recurrence="recurring")
    assert Aid.objects.open().count() == 4


def test_expired_filter(last_month, next_month):
    """Test the `expired` queryset filter."""

    # Those aids must not be considered `expired`
    AidFactory(submission_deadline=last_month, recurrence="oneoff")
    AidFactory(submission_deadline=last_month, recurrence="recurring")
    assert Aid.objects.expired().count() == 2

    # Those aids must not be considered `expired`
    AidFactory(submission_deadline=timezone.now().date())
    AidFactory(submission_deadline=next_month)
    AidFactory(submission_deadline=None)
    AidFactory(submission_deadline=last_month, recurrence="ongoing")
    assert Aid.objects.expired().count() == 2


def test_soon_expiring_filter(last_month, next_week, next_month, settings):
    settings.APPROACHING_DEADLINE_DELTA = 15

    AidFactory(submission_deadline=next_week, recurrence="oneoff")
    AidFactory(submission_deadline=next_week, recurrence="oneoff")
    AidFactory(submission_deadline=next_week, recurrence="ongoing")
    AidFactory(submission_deadline=next_week, recurrence="ongoing")
    AidFactory(submission_deadline=last_month, recurrence="oneoff")
    AidFactory(submission_deadline=last_month, recurrence="oneoff")

    assert Aid.objects.soon_expiring().count() == 2


def test_hidden_filter(last_month, next_month):
    """Test the `hidden` filter.

    Aids only appear when they have the `published` status and are not
    expired.
    """

    # Displayed aids
    AidFactory(
        status="published",
        submission_deadline=timezone.now().date(),
        recurrence="oneoff",
    )
    AidFactory(status="published", submission_deadline=next_month, recurrence="oneoff")
    AidFactory(status="published", submission_deadline=None, recurrence="oneoff")
    AidFactory(status="published", submission_deadline=next_month, recurrence="ongoing")
    assert Aid.objects.hidden().count() == 0

    # Hidden aids
    AidFactory(status="draft")
    AidFactory(status="reviewable")
    AidFactory(status="published", submission_deadline=last_month)
    assert Aid.objects.hidden().count() == 3


def test_live_filter(last_month, next_month):
    """Test the `live` filter.

    Aids only appear when they have the `published` status and are not
    expired.
    """

    # Displayed aids
    AidFactory(
        status="published",
        submission_deadline=timezone.now().date(),
        recurrence="oneoff",
    )
    AidFactory(status="published", submission_deadline=next_month, recurrence="oneoff")
    AidFactory(status="published", submission_deadline=None, recurrence="oneoff")
    AidFactory(status="published", submission_deadline=next_month, recurrence="ongoing")
    assert Aid.objects.live().count() == 4

    # Hidden aids
    AidFactory(status="draft")
    AidFactory(status="reviewable")
    AidFactory(status="published", submission_deadline=last_month)
    assert Aid.objects.live().count() == 4
