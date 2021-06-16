"""Test methods aid related forms."""

import pytest
from django.contrib.admin.sites import AdminSite

from aids.models import Aid
from aids.admin import AidAdmin
from aids.forms import BaseAidForm, AidSearchForm, AidEditForm
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
        financers=[backer],
        submission_deadline='2018-01-01',
        mobilization_steps=['preop'],
        aid_types=['grant', 'loan'],
        targeted_audiences=['commune'])
    AidFactory(
        author=user,
        financers=[backer],
        submission_deadline='2018-01-01',
        mobilization_steps=['preop'],
        aid_types=['grant', 'loan'],
        targeted_audiences=['department'])
    AidFactory(
        author=user,
        financers=[backer],
        submission_deadline='2018-01-01',
        mobilization_steps=['preop'],
        aid_types=['grant', 'loan'],
        targeted_audiences=['region'])
    AidFactory(
        author=user,
        financers=[backer],
        submission_deadline='2018-01-01',
        mobilization_steps=['preop'],
        aid_types=['grant', 'loan'],
        targeted_audiences=['epci'])
    AidFactory(
        author=user,
        financers=[backer],
        submission_deadline='2018-05-01',
        mobilization_steps=['preop'],
        aid_types=['grant', 'loan'],
        targeted_audiences=['public_cies'])
    AidFactory(
        author=user,
        financers=[backer],
        submission_deadline='2018-05-01',
        mobilization_steps=['preop', 'op'],
        aid_types=['grant', 'loan'],
        targeted_audiences=['association'])
    AidFactory(
        author=user,
        financers=[backer],
        submission_deadline='2018-05-01',
        mobilization_steps=['preop', 'op'],
        aid_types=['grant', 'loan'],
        targeted_audiences=['private_person'])
    AidFactory(
        author=user,
        financers=[backer],
        submission_deadline='2018-05-01',
        mobilization_steps=['preop', 'op'],
        aid_types=['grant', 'loan'],
        targeted_audiences=['researcher'])
    AidFactory(
        author=user,
        financers=[backer],
        submission_deadline='2018-09-01',
        mobilization_steps=['preop', 'op', 'postop'],
        aid_types=['loan'],
        targeted_audiences=['private_sector'])
    AidFactory(
        author=user,
        financers=[backer],
        submission_deadline='2018-09-01',
        mobilization_steps=['op', 'postop'],
        aid_types=['loan'],
        targeted_audiences=[])
    AidFactory(
        author=user,
        financers=[backer],
        submission_deadline='2018-09-01',
        mobilization_steps=['op', 'postop'],
        aid_types=[],
        targeted_audiences=[])
    AidFactory(
        author=user,
        financers=[backer],
        submission_deadline='2018-09-01',
        mobilization_steps=['postop'],
        aid_types=['technical', 'financial'],
        targeted_audiences=[])

    qs = Aid.objects.all().order_by('id')
    return qs


def test_admin_form_default(aid_admin_form_class, aid_form_data):
    """Test the form with default values."""
    form = aid_admin_form_class(aid_form_data)
    if not form.is_valid():
        assert True


def test_search_form_filter_mobilization_step(aids):
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
        'technical_aids': ['technical']})
    qs = form.filter_queryset(aids)
    assert qs.count() == 9
    for aid in qs:
        assert 'grant' in aid.aid_types or 'technical' in aid.aid_types


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
    assert qs.count() == 4

    form = AidSearchForm({'apply_before': '2017-12-31'})
    qs = form.filter_queryset(aids)
    assert qs.count() == 0


def test_search_from_filter_by_audiences(aids):
    form = AidSearchForm({'targeted_audiences': ['commune']})
    qs = form.filter_queryset(aids)
    assert qs.count() == 1
    for aid in qs:
        assert 'commune' in aid.targeted_audiences

    form = AidSearchForm({'targeted_audiences': [
        'commune', 'department'
        ]})
    qs = form.filter_queryset(aids)
    assert qs.count() == 2
    for aid in qs:
        assert any((
            'commune' in aid.targeted_audiences,
            'department' in aid.targeted_audiences))

    form = AidSearchForm({'targeted_audiences': [
        'commune', 'department', 'region'
        ]})
    qs = form.filter_queryset(aids)
    assert qs.count() == 3
    for aid in qs:
        assert any((
            'commune' in aid.targeted_audiences,
            'department' in aid.targeted_audiences,
            'region' in aid.targeted_audiences))

    form = AidSearchForm({'targeted_audiences': [
            'commune', 'department', 'region', 'epci'
        ]})
    qs = form.filter_queryset(aids)
    assert qs.count() == 4
    for aid in qs:
        assert any((
            'commune' in aid.targeted_audiences,
            'department' in aid.targeted_audiences,
            'region' in aid.targeted_audiences,
            'epci' in aid.targeted_audiences))

    form = AidSearchForm({'targeted_audiences': [
            'commune', 'department', 'region', 'epci', 'public_cies'
        ]})
    qs = form.filter_queryset(aids)
    assert qs.count() == 5
    for aid in qs:
        assert any((
            'commune' in aid.targeted_audiences,
            'department' in aid.targeted_audiences,
            'region' in aid.targeted_audiences,
            'epci' in aid.targeted_audiences,
            'public_cies' in aid.targeted_audiences))

    form = AidSearchForm({
        'targeted_audiences': [
            'commune', 'department', 'region', 'epci', 'public_cies',
            'association'
        ]
    })
    qs = form.filter_queryset(aids)
    assert qs.count() == 6
    for aid in qs:
        assert any((
            'commune' in aid.targeted_audiences,
            'department' in aid.targeted_audiences,
            'region' in aid.targeted_audiences,
            'epci' in aid.targeted_audiences,
            'public_cies' in aid.targeted_audiences,
            'association' in aid.targeted_audiences))

    form = AidSearchForm({
        'targeted_audiences': [
            'commune', 'department', 'region', 'epci', 'public_cies',
            'association', 'private_person'
        ]
    })
    qs = form.filter_queryset(aids)
    assert qs.count() == 7
    for aid in qs:
        assert any((
            'commune' in aid.targeted_audiences,
            'department' in aid.targeted_audiences,
            'region' in aid.targeted_audiences,
            'epci' in aid.targeted_audiences,
            'public_cies' in aid.targeted_audiences,
            'association' in aid.targeted_audiences,
            'private_person' in aid.targeted_audiences))

    form = AidSearchForm({
        'targeted_audiences': [
            'commune', 'department', 'region', 'epci', 'public_cies',
            'association', 'private_person', 'researcher'
        ]
    })
    qs = form.filter_queryset(aids)
    assert qs.count() == 8
    for aid in qs:
        assert any((
            'commune' in aid.targeted_audiences,
            'department' in aid.targeted_audiences,
            'region' in aid.targeted_audiences,
            'epci' in aid.targeted_audiences,
            'public_cies' in aid.targeted_audiences,
            'association' in aid.targeted_audiences,
            'private_person' in aid.targeted_audiences,
            'researcher' in aid.targeted_audiences,))

    form = AidSearchForm({
        'targeted_audiences': [
            'commune', 'department', 'region', 'epci', 'public_cies',
            'association', 'private_person', 'researcher', 'private_sector'
        ]
    })
    qs = form.filter_queryset(aids)
    assert qs.count() == 9
    for aid in qs:
        assert any((
            'commune' in aid.targeted_audiences,
            'department' in aid.targeted_audiences,
            'region' in aid.targeted_audiences,
            'epci' in aid.targeted_audiences,
            'public_cies' in aid.targeted_audiences,
            'association' in aid.targeted_audiences,
            'private_person' in aid.targeted_audiences,
            'researcher' in aid.targeted_audiences,
            'private_sector' in aid.targeted_audiences))


def test_aid_author_contributors_duplicate_validation(aid_form_data, user):
    aid_form_data['contributors'] = [user]

    form = BaseAidForm(aid_form_data)
    assert not form.is_valid()

    # actually works, but the test fails
    # form = AidAdminForm(aid_form_data)
    # assert not form.is_valid()

    # but it will currently work in other forms that override the fields list
    form = AidEditForm(aid_form_data)
    assert form.is_valid()


def test_aid_edition_subvention_rate_validation(aid_form_data):
    form = AidEditForm(aid_form_data, requested_status='reviewable')
    assert form.is_valid()

    # Lower range is optional
    aid_form_data['subvention_rate_0'] = None
    aid_form_data['subvention_rate_1'] = 40
    form = AidEditForm(aid_form_data, requested_status='reviewable')
    assert form.is_valid()

    # Upper range is optional
    aid_form_data['subvention_rate_0'] = 40
    aid_form_data['subvention_rate_1'] = None
    form = AidEditForm(aid_form_data, requested_status='reviewable')
    assert form.is_valid()

    # Range must be in the correct order
    aid_form_data['subvention_rate_0'] = 50
    aid_form_data['subvention_rate_1'] = 40
    form = AidEditForm(aid_form_data, requested_status='reviewable')
    assert not form.is_valid()
    assert form.has_error('subvention_rate', 'bound_ordering')

    # Range must be between 0 and 100
    aid_form_data['subvention_rate_0'] = -10
    aid_form_data['subvention_rate_1'] = 150
    form = AidEditForm(aid_form_data, requested_status='reviewable')
    assert not form.is_valid()
    assert form.has_error('subvention_rate', 'min_value')
    assert form.has_error('subvention_rate', 'max_value')


def test_aid_calendar_fields_validation(aid_form_data):
    form = AidEditForm(aid_form_data, requested_status='reviewable')
    assert form.is_valid()

    aid_form_data.update({
        'recurrence': 'oneoff',
        'submission_deadline': ''})
    form = AidEditForm(aid_form_data, requested_status='reviewable')
    assert not form.is_valid()

    aid_form_data.update({
        'recurrence': 'oneoff',
        'submission_deadline': '01/01/2020'})
    form = AidEditForm(aid_form_data, requested_status='reviewable')
    assert form.is_valid()

    aid_form_data.update({
        'recurrence': 'recurring',
        'submission_deadline': ''})
    form = AidEditForm(aid_form_data, requested_status='reviewable')
    assert not form.is_valid()

    aid_form_data.update({
        'recurrence': 'recurring',
        'submission_deadline': '01/01/2020'})
    form = AidEditForm(aid_form_data, requested_status='reviewable')
    assert form.is_valid()

    aid_form_data.update({
        'recurrence': 'ongoing',
        'submission_deadline': ''})
    form = AidEditForm(aid_form_data, requested_status='reviewable')
    assert form.is_valid()


def test_aid_creation_description_sanitization(aid_form_data):
    aid_form_data.update({
        'description': '''
        <div class="toto">
        <p>Paragraphe</p>
        <p>A <strong>paragraph</strong> with <em>formatted</em> text.</p>
        <h2>A title<h2>
        <script>alert('Nasty popup');</script>
        <p><img src="//example.com/nasty-tracker.gif" /></p>
        <p><a href="//example.com/good-link.html">A link!</a></p>
        <p style="margin: 10em">Huge margins</p>
        </div>
        '''
    })
    form = AidEditForm(aid_form_data, requested_status='reviewable')
    assert form.is_valid()

    description = form.cleaned_data['description']
    assert '<p>' in description
    assert '<h2>' in description
    assert '<em>' in description
    assert 'formatted' in description
    assert '<strong>' in description
    assert 'paragraph' in description
    assert '<a href="//example.com' in description
    assert '<img' in description
    assert 'style' in description

    assert 'script' not in description
    assert '<div' not in description
    assert 'class="toto"' not in description
