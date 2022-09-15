import pytest
from datetime import timedelta

from django.utils import timezone

from aids.factories import AidFactory
from alerts.factories import AlertFactory

pytestmark = pytest.mark.django_db


@pytest.fixture()
def last_month():
    return timezone.now() - timedelta(days=30)


@pytest.fixture()
def last_week():
    return timezone.now() - timedelta(days=7)


@pytest.fixture
def yesterday():
    return timezone.now() - timedelta(days=1)


def test_get_new_aids_with_no_aids(last_month):
    """No aids exist, so no aids can be found."""

    alert = AlertFactory(querystring="text=test")
    aids = alert.get_new_aids()
    assert len(aids) == 0


def test_get_new_aids_with_no_old_aids(last_month):
    """Matching aids are older than the requested threshold."""

    alert = AlertFactory(querystring="text=test")
    AidFactory.create_batch(5, name="Test", date_published=last_month)
    aids = alert.get_new_aids()
    assert len(aids) == 0


def test_get_new_aids_with_no_matching_aids(yesterday):
    """Existing aids do not match."""

    alert = AlertFactory(querystring="text=Gloubiboulga")
    AidFactory.create_batch(5, name="Test", date_published=yesterday)
    aids = alert.get_new_aids()
    assert len(aids) == 0


def test_get_new_aids_with_matching_aids(yesterday):
    """Matching aids are found."""

    alert = AlertFactory(querystring="text=test")
    AidFactory.create_batch(5, name="Test", date_published=yesterday)
    aids = alert.get_new_aids()
    assert len(aids) == 5


def test_get_new_aids_with_unpublished_aids(yesterday):
    """Matching aids are not published."""

    alert = AlertFactory(querystring="text=test")
    AidFactory.create_batch(5, name="Test", date_published=yesterday, status="draft")
    aids = alert.get_new_aids()
    assert len(aids) == 0


def test_get_absolute_url():
    alert = AlertFactory(querystring="text=test")
    alert_absolute_url = alert.get_absolute_url()
    assert alert_absolute_url.startswith("/aides/")


def test_get_absolute_url_in_minisite():
    alert = AlertFactory(querystring="text=test")
    alert_absolute_url = alert.get_absolute_url(in_minisite=True)
    assert not alert_absolute_url.startswith("/aides/")
