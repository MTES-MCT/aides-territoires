"""Test methods aid related forms."""

import pytest

from aids.models import Aid
from aids.admin import AidAdmin
from django.contrib.admin.sites import AdminSite
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
