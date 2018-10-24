"""Test methods aid related forms."""

import pytest
from django.contrib.admin.sites import AdminSite

from aids.models import Aid
from aids.admin import AidAdmin
from aids.forms import AidSearchForm, AidEditForm
from aids.factories import AidFactory


pytestmark = pytest.mark.django_db


@pytest.fixture
def aid_admin_form_class():
    """Generates a valid form class.

    Since `AidFormAdmin` is an admin form, is is declared without the usual
    `model` and `fields` configuration parameters. That's why it has to be
    instanciated that way.
    """

    site = AdminSite()
    admin = AidAdmin(Aid, site)
    form_class = admin.get_form(None)
    return form_class


@pytest.fixture
def aids(user, backer):
    """Generates a few aids and return the corresponding queryset."""

    AidFactory(
        author=user,
        backers=[backer],
        submission_deadline='2018-01-01',
        mobilization_steps=['preop'],
        aid_types=['grant', 'loan'])
    AidFactory(
        author=user,
        backers=[backer],
        submission_deadline='2018-01-01',
        mobilization_steps=['preop'],
        aid_types=['grant', 'loan'])
    AidFactory(
        author=user,
        backers=[backer],
        submission_deadline='2018-01-01',
        mobilization_steps=['preop'],
        aid_types=['grant', 'loan'])
    AidFactory(
        author=user,
        backers=[backer],
        submission_deadline='2018-01-01',
        mobilization_steps=['preop'],
        aid_types=['grant', 'loan'])
    AidFactory(
        author=user,
        backers=[backer],
        submission_deadline='2018-05-01',
        mobilization_steps=['preop'],
        aid_types=['grant', 'loan'])
    AidFactory(
        author=user,
        backers=[backer],
        submission_deadline='2018-05-01',
        mobilization_steps=['preop', 'op'],
        aid_types=['grant', 'loan'])
    AidFactory(
        author=user,
        backers=[backer],
        submission_deadline='2018-05-01',
        mobilization_steps=['preop', 'op'],
        aid_types=['grant', 'loan'])
    AidFactory(
        author=user,
        backers=[backer],
        submission_deadline='2018-05-01',
        mobilization_steps=['preop', 'op'],
        aid_types=['grant', 'loan'])
    AidFactory(
        author=user,
        backers=[backer],
        submission_deadline='2018-09-01',
        mobilization_steps=['preop', 'op', 'postop'],
        aid_types=['loan'])
    AidFactory(
        author=user,
        backers=[backer],
        submission_deadline='2018-09-01',
        mobilization_steps=['op', 'postop'],
        aid_types=['loan'])
    AidFactory(
        author=user,
        backers=[backer],
        submission_deadline='2018-09-01',
        mobilization_steps=['op', 'postop'],
        aid_types=[])
    AidFactory(
        author=user,
        backers=[backer],
        submission_deadline='2018-09-01',
        mobilization_steps=['postop'],
        aid_types=['networking', 'return_fund'])

    qs = Aid.objects.all().order_by('id')
    return qs


def test_admin_form_default(aid_admin_form_class, aid_form_data):
    """Test the form with default values."""

    form = aid_admin_form_class(aid_form_data)
    assert form.is_valid()


def test_seach_form_filter_mobilization_step(aids):
    form = AidSearchForm({'mobilization_step': ['preop']})
    qs = form.filter_queryset(aids)
    assert qs.count() == 9
    for aid in qs:
        assert 'preop' in aid.mobilization_steps

    form = AidSearchForm({'mobilization_step': ['op']})
    qs = form.filter_queryset(aids)
    assert qs.count() == 6
    for aid in qs:
        assert 'op' in aid.mobilization_steps

    form = AidSearchForm({'mobilization_step': ['postop']})
    qs = form.filter_queryset(aids)
    assert qs.count() == 4
    for aid in qs:
        assert 'postop' in aid.mobilization_steps

    form = AidSearchForm({'mobilization_step': ['preop', 'postop']})
    qs = form.filter_queryset(aids)
    assert qs.count() == 12
    for aid in qs:
        assert any((
            'preop' in aid.mobilization_steps,
            'postop' in aid.mobilization_steps))


def test_search_form_filter_by_types(aids):
    form = AidSearchForm({'aid_types': ['grant']})
    qs = form.filter_queryset(aids)
    assert qs.count() == 8
    for aid in qs:
        assert 'grant' in aid.aid_types

    form = AidSearchForm({'aid_types': ['grant', 'networking']})
    qs = form.filter_queryset(aids)
    for aid in qs:
        print(aid.aid_types)
    assert qs.count() == 9
    for aid in qs:
        assert 'grant' in aid.aid_types or 'networking' in aid.aid_types


def test_search_form_filter_by_deadline(aids):
    form = AidSearchForm({'apply_before': '2018-12-01'})
    qs = form.filter_queryset(aids)
    assert qs.count() == 12

    form = AidSearchForm({'apply_before': '2018-08-01'})
    qs = form.filter_queryset(aids)
    assert qs.count() == 8

    form = AidSearchForm({'apply_before': '2018-04-01'})
    qs = form.filter_queryset(aids)
    assert qs.count() == 4

    form = AidSearchForm({'apply_before': '2018-01-01'})
    qs = form.filter_queryset(aids)
    assert qs.count() == 0

    form = AidSearchForm({'apply_before': '2017-12-31'})
    qs = form.filter_queryset(aids)
    assert qs.count() == 0
