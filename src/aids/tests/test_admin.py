import pytest
from datetime import timedelta

from django.contrib.admin.sites import AdminSite
from django.utils import timezone

from aids.factories import AidFactory
from aids.admin import AidAdmin
from aids.models import Aid


pytestmark = pytest.mark.django_db


@pytest.fixture
def admin():
    return AidAdmin(model=Aid, admin_site=AdminSite())


def test_set_review_status_does_not_set_published_date(admin):

    aid = AidFactory(status='draft')
    assert aid.date_published is None

    aid.status = 'reviewable'
    admin.save_model(obj=aid, request=None, form=None, change=None)
    aid.refresh_from_db()

    assert aid.status == 'reviewable'
    assert aid.date_published is None


def test_set_published_status_does_set_published_date(admin):
    """When aids are published, we store the publication date."""

    aid = AidFactory(status='draft')
    assert aid.date_published is None

    aid.status = 'published'
    admin.save_model(obj=aid, request=None, form=None, change=None)
    aid.refresh_from_db()

    assert aid.status == 'published'
    assert aid.date_published is not None


def test_unpublish_aid_does_not_remove_published_date(admin):
    """when aid are unpublished, we keep the first publication date."""

    aid = AidFactory(status='published', date_published=timezone.now())

    aid.status = 'draft'
    admin.save_model(obj=aid, request=None, form=None, change=None)
    aid.refresh_from_db()

    assert aid.status == 'draft'
    assert aid.date_published is not None


def test_republish_aid_does_not_override_first_publication_date(admin):
    """when aid are republished, we keep the first publication date."""

    last_month = timezone.now() - timedelta(days=30)

    aid = AidFactory(status='draft', date_published=last_month)
    aid.status = 'published'
    admin.save_model(obj=aid, request=None, form=None, change=None)
    aid.refresh_from_db()

    assert aid.status == 'published'
    assert aid.date_published == last_month
