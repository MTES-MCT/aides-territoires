"""Test methods aid related forms."""

import pytest
from django.contrib.admin.sites import AdminSite

from aids.models import Aid
from aids.admin import AidAdmin
from aids.forms import AidSearchForm
from aids.factories import AidFactory
from accounts.factories import UserFactory
from backers.factories import BackerFactory


pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    """Generates a valid and active user."""

    user = UserFactory()
    return user


@pytest.fixture
def backer():
    """Generates a valid Backer."""

    backer = BackerFactory()
    return backer


@pytest.fixture
def aid_form_class():
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
def aid_form_data(user, backer):
    """Returns valid data to create an Aid object."""

    return {
        'name': 'Test aid',
        'author': user.id,
        'backer': backer.id,
        'description': 'My aid description',
        'eligibility': 'Aid eligibility info',
        'application_perimeter': 'france',
        'mobilization_steps': ['preop'],
        'targeted_audiances': ['department'],
        'aid_types': ['grant', 'loan'],
        'destinations': ['operation'],
        'thematics': ['local_development'],
        'publication_status': 'open',
        'status': 'published',
    }


@pytest.fixture
def aids(user, backer):
    """Generates a few aids and return the corresponding queryset."""

    AidFactory(author=user, backer=backer, application_perimeter='europe')
    AidFactory(author=user, backer=backer, application_perimeter='france')
    AidFactory(author=user, backer=backer, application_perimeter='mainland')
    AidFactory(author=user, backer=backer, application_perimeter='overseas')
    AidFactory(author=user, backer=backer, application_perimeter='region',
               application_region='01')  # Guadeloupe
    AidFactory(author=user, backer=backer, application_perimeter='region',
               application_region='02')  # Martinique
    AidFactory(author=user, backer=backer, application_perimeter='region',
               application_region='28')  # Normandie
    AidFactory(author=user, backer=backer, application_perimeter='region',
               application_region='76')  # Occitanie
    AidFactory(author=user, backer=backer, application_perimeter='department',
               application_department='972')  # Martinique
    AidFactory(author=user, backer=backer, application_perimeter='department',
               application_department='973')  # Guyane
    AidFactory(author=user, backer=backer, application_perimeter='department',
               application_department='27')  # Eure
    AidFactory(author=user, backer=backer, application_perimeter='department',
               application_department='34')  # Hérault

    qs = Aid.objects.all().order_by('id')
    return qs


def test_form_default(aid_form_class, aid_form_data):
    """Test the form with default values."""

    form = aid_form_class(aid_form_data)
    assert form.is_valid()


def test_form_application_department(aid_form_class, aid_form_data):
    """Test that the department is a mandatory field."""

    # Department perimeter selected, but no department selected
    aid_form_data['application_perimeter'] = 'department'
    form = aid_form_class(aid_form_data)
    assert not form.is_valid()
    assert 'application_department' in form.errors

    aid_form_data['application_department'] = '34'
    form = aid_form_class(aid_form_data)
    assert form.is_valid()

    # Department selected but perimeter is not set to department
    aid_form_data['application_perimeter'] = 'france'
    form = aid_form_class(aid_form_data)
    assert not form.is_valid()
    assert 'application_department' in form.errors

    aid_form_data['application_department'] = ''
    form = aid_form_class(aid_form_data)
    assert form.is_valid()


def test_form_application_region(aid_form_class, aid_form_data):
    """Test that the region is a mandatory field."""

    # Region perimeter selected, but no region selected
    aid_form_data['application_perimeter'] = 'region'
    form = aid_form_class(aid_form_data)
    assert not form.is_valid()
    assert 'application_region' in form.errors

    aid_form_data['application_region'] = '76'
    form = aid_form_class(aid_form_data)
    assert form.is_valid()

    # Region selected, but perimeter is not set to region
    aid_form_data['application_perimeter'] = 'france'
    form = aid_form_class(aid_form_data)
    assert not form.is_valid()
    assert 'application_region' in form.errors

    aid_form_data['application_region'] = ''
    form = aid_form_class(aid_form_data)
    assert form.is_valid()


def test_form_filter_with_no_zipcode(aids):
    form = AidSearchForm({'zipcode': ''})
    qs = form.filter_queryset(aids)
    assert qs.count() == 12


def test_form_with_invalid_zipcode(aids):
    form = AidSearchForm({'zipcode': 'blah'})
    assert not form.is_valid()
    assert 'zipcode' in form.errors

    qs = form.filter_queryset(aids)
    assert qs.count() == 12


def test_form_filter_mainland_zipcode(aids):
    form = AidSearchForm({'zipcode': '34110'})  # Vic la Gardiole
    qs = form.filter_queryset(aids)
    assert qs.count() == 5
    assert qs[0].application_perimeter == 'europe'
    assert qs[1].application_perimeter == 'france'
    assert qs[2].application_perimeter == 'mainland'
    assert qs[3].application_perimeter == 'region'
    assert qs[3].application_region == '76'
    assert qs[4].application_perimeter == 'department'
    assert qs[4].application_region == '34'

    form = AidSearchForm({'zipcode': '27370'})  # St Cyr la Campagne
    qs = form.filter_queryset(aids)
    assert qs.count() == 5
    assert qs[0].application_perimeter == 'europe'
    assert qs[1].application_perimeter == 'france'
    assert qs[2].application_perimeter == 'mainland'
    assert qs[3].application_perimeter == 'region'
    assert qs[3].application_region == '28'
    assert qs[4].application_perimeter == 'department'
    assert qs[4].application_region == '27'

    form = AidSearchForm({'zipcode': '46800'})
    qs = form.filter_queryset(aids)
    assert qs.count() == 3
    assert qs[0].application_perimeter == 'europe'
    assert qs[1].application_perimeter == 'france'
    assert qs[2].application_perimeter == 'mainland'


def test_form_filter_overseas_zipcode(aids):
    form = AidSearchForm({'zipcode': '97200'})  # Fort de France
    qs = form.filter_queryset(aids)
    assert qs.count() == 5
    assert qs[0].application_perimeter == 'europe'
    assert qs[1].application_perimeter == 'france'
    assert qs[2].application_perimeter == 'overseas'
    assert qs[3].application_perimeter == 'region'
    assert qs[3].application_region == '02'
    assert qs[4].application_perimeter == 'department'
    assert qs[4].application_region == '972'

    form = AidSearchForm({'zipcode': '97300'})  # Cayenne
    qs = form.filter_queryset(aids)
    assert qs.count() == 5
    assert qs[0].application_perimeter == 'europe'
    assert qs[1].application_perimeter == 'france'
    assert qs[2].application_perimeter == 'overseas'
    assert qs[3].application_perimeter == 'region'
    assert qs[3].application_region == '03'
    assert qs[4].application_perimeter == 'department'
    assert qs[4].application_region == '973'

    form = AidSearchForm({'zipcode': '97400'})  # St-Denis
    qs = form.filter_queryset(aids)
    assert qs.count() == 3
    assert qs[0].application_perimeter == 'europe'
    assert qs[1].application_perimeter == 'france'
    assert qs[2].application_perimeter == 'overseas'
