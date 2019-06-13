import pytest
from datetime import timedelta

from django.utils import timezone

from aids.factories import AidFactory
from bookmarks.factories import BookmarkFactory

pytestmark = pytest.mark.django_db


@pytest.fixture()
def last_month():
    return timezone.now() - timedelta(days=30)


@pytest.fixture()
def last_week():
    return timezone.now() - timedelta(days=7)


def test_get_aids_with_no_aids(last_month):
    """No aids exist, so no aids can be found."""

    bookmark = BookmarkFactory(querystring='text=test')
    aids = bookmark.get_aids(published_after=last_month)
    assert len(aids) == 0


def test_get_aids_with_no_old_aids(last_month):
    """Matching aids are older than the requested threshold."""

    bookmark = BookmarkFactory(querystring='text=test')
    AidFactory.create_batch(
        5,
        name='Test',
        date_created=last_month - timedelta(days=10))
    aids = bookmark.get_aids(published_after=last_month)
    assert len(aids) == 0


def test_get_aids_with_no_matching_aids(last_month, last_week):
    """Existing aids do not match."""

    bookmark = BookmarkFactory(querystring='text=Gloubiboulga')
    AidFactory.create_batch(
        5,
        name='Test',
        date_created=last_week)
    aids = bookmark.get_aids(published_after=last_month)
    assert len(aids) == 0


def test_get_aids_with_matching_aids(last_month, last_week):
    """Matching aids are found."""

    bookmark = BookmarkFactory(querystring='text=test')
    AidFactory.create_batch(
        5,
        name='Test',
        date_created=last_week)
    aids = bookmark.get_aids(published_after=last_month)
    assert len(aids) == 5


def test_get_aids_with_unpublished_aids(last_month, last_week):
    """Matching aids are not published."""

    bookmark = BookmarkFactory(querystring='text=test')
    AidFactory.create_batch(
        5,
        name='Test',
        date_created=last_week,
        status='draft')
    aids = bookmark.get_aids(published_after=last_month)
    assert len(aids) == 0
