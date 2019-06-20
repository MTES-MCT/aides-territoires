"""Test methods aid related forms."""

import pytest
from django.contrib.admin.sites import AdminSite

from aids.models import Aid
from aids.admin import AidAdmin
from aids.forms import AidSearchForm
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
        aid_types=['grant', 'loan'],
        targeted_audiances=['commune'])
    AidFactory(
        author=user,
        backers=[backer],
        submission_deadline='2018-01-01',
        mobilization_steps=['preop'],
        aid_types=['grant', 'loan'],
        targeted_audiances=['department'])
    AidFactory(
        author=user,
        backers=[backer],
        submission_deadline='2018-01-01',
        mobilization_steps=['preop'],
        aid_types=['grant', 'loan'],
        targeted_audiances=['region'])
    AidFactory(
        author=user,
        backers=[backer],
        submission_deadline='2018-01-01',
        mobilization_steps=['preop'],
        aid_types=['grant', 'loan'],
        targeted_audiances=['epci'])
    AidFactory(
        author=user,
        backers=[backer],
        submission_deadline='2018-05-01',
        mobilization_steps=['preop'],
        aid_types=['grant', 'loan'],
        targeted_audiances=['lessor'])
    AidFactory(
        author=user,
        backers=[backer],
        submission_deadline='2018-05-01',
        mobilization_steps=['preop', 'op'],
        aid_types=['grant', 'loan'],
        targeted_audiances=['association'])
    AidFactory(
        author=user,
        backers=[backer],
        submission_deadline='2018-05-01',
        mobilization_steps=['preop', 'op'],
        aid_types=['grant', 'loan'],
        targeted_audiances=['private_person'])
    AidFactory(
        author=user,
        backers=[backer],
        submission_deadline='2018-05-01',
        mobilization_steps=['preop', 'op'],
        aid_types=['grant', 'loan'],
        targeted_audiances=['researcher'])
    AidFactory(
        author=user,
        backers=[backer],
        submission_deadline='2018-09-01',
        mobilization_steps=['preop', 'op', 'postop'],
        aid_types=['loan'],
        targeted_audiances=['private_sector'])
    AidFactory(
        author=user,
        backers=[backer],
        submission_deadline='2018-09-01',
        mobilization_steps=['op', 'postop'],
        aid_types=['loan'],
        targeted_audiances=[])
    AidFactory(
        author=user,
        backers=[backer],
        submission_deadline='2018-09-01',
        mobilization_steps=['op', 'postop'],
        aid_types=[],
        targeted_audiances=[])
    AidFactory(
        author=user,
        backers=[backer],
        submission_deadline='2018-09-01',
        mobilization_steps=['postop'],
        aid_types=['networking', 'return_fund'],
        targeted_audiances=[])

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
    form = AidSearchForm({'financial_aids': ['grant']})
    qs = form.filter_queryset(aids)
    assert qs.count() == 8
    for aid in qs:
        assert 'grant' in aid.aid_types

    form = AidSearchForm({
        'financial_aids': ['grant'],
        'technical_aids': ['networking']})
    qs = form.filter_queryset(aids)
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


def test_search_from_filter_by_audiances(aids):
    form = AidSearchForm({'targeted_audiances': ['commune']})
    qs = form.filter_queryset(aids)
    assert qs.count() == 1
    for aid in qs:
        assert 'commune' in aid.targeted_audiances

    form = AidSearchForm({'targeted_audiances': [
        'commune', 'department'
        ]})
    qs = form.filter_queryset(aids)
    assert qs.count() == 2
    for aid in qs:
        assert any((
            'commune' in aid.targeted_audiances,
            'department' in aid.targeted_audiances))

    form = AidSearchForm({'targeted_audiances': [
        'commune', 'department', 'region'
        ]})
    qs = form.filter_queryset(aids)
    assert qs.count() == 3
    for aid in qs:
        assert any((
            'commune' in aid.targeted_audiances,
            'department' in aid.targeted_audiances,
            'region' in aid.targeted_audiances))

    form = AidSearchForm({'targeted_audiances': [
            'commune', 'department', 'region', 'epci'
        ]})
    qs = form.filter_queryset(aids)
    assert qs.count() == 4
    for aid in qs:
        assert any((
            'commune' in aid.targeted_audiances,
            'department' in aid.targeted_audiances,
            'region' in aid.targeted_audiances,
            'epci' in aid.targeted_audiances))

    form = AidSearchForm({'targeted_audiances': [
            'commune', 'department', 'region', 'epci', 'lessor'
        ]})
    qs = form.filter_queryset(aids)
    assert qs.count() == 5
    for aid in qs:
        assert any((
            'commune' in aid.targeted_audiances,
            'department' in aid.targeted_audiances,
            'region' in aid.targeted_audiances,
            'epci' in aid.targeted_audiances,
            'lessor' in aid.targeted_audiances))

    form = AidSearchForm({'targeted_audiances': [
            'commune', 'department', 'region', 'epci', 'lessor', 'association'
        ]})
    qs = form.filter_queryset(aids)
    assert qs.count() == 6
    for aid in qs:
        assert any((
            'commune' in aid.targeted_audiances,
            'department' in aid.targeted_audiances,
            'region' in aid.targeted_audiances,
            'epci' in aid.targeted_audiances,
            'lessor' in aid.targeted_audiances,
            'association' in aid.targeted_audiances))

    form = AidSearchForm({'targeted_audiances': [
            'commune', 'department', 'region', 'epci', 'lessor', 'association',
            'private_person'
        ]})
    qs = form.filter_queryset(aids)
    assert qs.count() == 7
    for aid in qs:
        assert any((
            'commune' in aid.targeted_audiances,
            'department' in aid.targeted_audiances,
            'region' in aid.targeted_audiances,
            'epci' in aid.targeted_audiances,
            'lessor' in aid.targeted_audiances,
            'association' in aid.targeted_audiances,
            'private_person' in aid.targeted_audiances))

    form = AidSearchForm({'targeted_audiances': [
            'commune', 'department', 'region', 'epci', 'lessor', 'association',
            'private_person', 'researcher'
            ]})
    qs = form.filter_queryset(aids)
    assert qs.count() == 8
    for aid in qs:
        assert any((
            'commune' in aid.targeted_audiances,
            'department' in aid.targeted_audiances,
            'region' in aid.targeted_audiances,
            'epci' in aid.targeted_audiances,
            'lessor' in aid.targeted_audiances,
            'association' in aid.targeted_audiances,
            'private_person' in aid.targeted_audiances,
            'researcher' in aid.targeted_audiances,))

    form = AidSearchForm({'targeted_audiances': [
        'commune', 'department', 'region', 'epci', 'lessor', 'association',
        'private_person', 'researcher', 'private_sector'
        ]})
    qs = form.filter_queryset(aids)
    assert qs.count() == 9
    for aid in qs:
        assert any((
            'commune' in aid.targeted_audiances,
            'department' in aid.targeted_audiances,
            'region' in aid.targeted_audiances,
            'epci' in aid.targeted_audiances,
            'lessor' in aid.targeted_audiances,
            'association' in aid.targeted_audiances,
            'private_person' in aid.targeted_audiances,
            'researcher' in aid.targeted_audiances,
            'private_sector' in aid.targeted_audiances))
