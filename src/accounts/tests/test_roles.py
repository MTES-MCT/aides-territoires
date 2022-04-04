import pytest

from rest_framework.authtoken.models import Token

from accounts.models import User
from accounts.factories import UserFactory
from search.factories import SearchPageFactory
from geofr.models import Perimeter
from geofr.factories import PerimeterFactory


pytestmark = pytest.mark.django_db


def test_user_role_contributor():
    """Users with 'is_contributor' as True are considered as contributors."""

    # user
    UserFactory(is_contributor=False, email="sample.notcontributor@example.org")
    # contributor
    UserFactory(is_contributor=True, email="sample.iscontributor@example.org")

    assert User.objects.count() == 2
    assert User.objects.contributors().count() == 1


def test_user_role_search_page_admin():
    """Users with linked Search Pages are considered as Search Page administrators."""

    # user
    UserFactory(is_contributor=False, email="sample.notcontributor2@example.org")
    # search page administrator
    search_page_administrator = UserFactory(
        is_contributor=False,
        email="sample.notcontributor3@example.org")
    SearchPageFactory(administrator=search_page_administrator)

    assert User.objects.count() == 2
    assert User.objects.search_page_admins().count() == 1


def test_user_role_animator():
    """Users with 'animator_perimeter' filled are considered as local animators."""

    # user
    UserFactory(
        is_contributor=False,
        email="sample.notcontributor@example.org")
    # local animator
    martinique = PerimeterFactory(name='Martinique', scale=Perimeter.SCALES.region)
    UserFactory(animator_perimeter=martinique)

    assert User.objects.count() == 2
    assert User.objects.animators().count() == 1


def test_user_role_api_token():
    """Users with a Token are considered as API users."""

    # user
    UserFactory(is_contributor=False)
    # api user
    api_user = UserFactory(is_contributor=False)
    # There are different ways to generate an API Token (most simple one: in the Admin UI)
    # https://django-rest-framework.readthedocs.io/en/3.4.7/api-guide/authentication.html?highlight=generate#generating-tokens  # noqa
    # call_command('drf_create_token', api_user.email)
    Token.objects.get_or_create(user=api_user)

    assert User.objects.count() == 2
    assert User.objects.with_api_token().count() == 1


def test_user_can_have_multiple_roles():
    """Roles are not exclusive. A user can have multiple roles."""

    multi_role_user = UserFactory(is_contributor=True)
    SearchPageFactory(administrator=multi_role_user)
    guadeloupe = PerimeterFactory(name='Guadeloupe', scale=Perimeter.SCALES.region)
    multi_role_user.animator_perimeter = guadeloupe
    multi_role_user.save()
    Token.objects.get_or_create(user=multi_role_user)

    assert User.objects.count() == 1
    assert User.objects.contributors().count() == 1
    assert User.objects.search_page_admins().count() == 1
    assert User.objects.animators().count() == 1
    assert User.objects.with_api_token().count() == 1
