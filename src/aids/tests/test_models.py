import pytest
from datetime import timedelta

from django.utils import timezone

from aids.factories import AidFactory


pytestmark = pytest.mark.django_db


def test_set_review_status_does_not_set_published_date():

    aid = AidFactory(status="draft")
    assert aid.date_published is None

    aid.status = "reviewable"
    aid.save()
    aid.refresh_from_db()

    assert aid.status == "reviewable"
    assert aid.date_published is None


def test_set_published_status_does_set_published_date():
    """When aids are published, we store the publication date."""

    aid = AidFactory(status="draft")
    assert aid.date_published is None

    aid.status = "published"
    aid.save()
    aid.refresh_from_db()

    assert aid.status == "published"
    assert aid.date_published is not None


def test_unpublish_aid_does_not_remove_published_date():
    """when aids are unpublished, we keep the first publication date."""

    aid = AidFactory(status="published", date_published=timezone.now())

    aid.status = "draft"
    aid.save()
    aid.refresh_from_db()

    assert aid.status == "draft"
    assert aid.date_published is not None


def test_republish_aid_does_not_override_first_publication_date():
    """when aids are republished, we keep the first publication date."""

    last_month = timezone.now() - timedelta(days=30)

    aid = AidFactory(status="draft", date_published=last_month)
    aid.status = "published"
    aid.save()
    aid.refresh_from_db()

    assert aid.status == "published"
    assert aid.date_published == last_month
