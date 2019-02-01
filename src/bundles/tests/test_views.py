"""Test bundle related views."""

import pytest

from bundles.factories import BundleFactory
from aids.factories import AidFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def aid(user):
    """Return a valid aid."""

    aid = AidFactory(author=user)
    return aid


def test_anonymous_user_cannot_see_the_bookmark_form(client, aid):
    """Aid bundles requires a logged in account."""
    aid_url = aid.get_absolute_url()
    res = client.get(aid_url)
    content = res.content.decode()

    assert 'Vous devez être identifé·e pour utiliser ' \
           'les listes d\'aides' in content


def test_anonymous_user_cannot_bookmark_aids(client, aid):
    aid_url = aid.get_absolute_url()
    res = client.post(aid_url)
    assert res.status_code == 405  # method not allowed


def test_bundle_modal_shows_selected_bundles(client, aid):
    """Authenticated users cannot login again, duh!"""

    user = aid.author
    bundles = [
        BundleFactory(name='Bundle_1', owner=user, aids=[aid]),
        BundleFactory(name='Bundle_2', owner=user, aids=[aid]),
        BundleFactory(name='Bundle_3', owner=user, aids=[])
    ]

    client.force_login(user)
    aid_url = aid.get_absolute_url()
    res = client.get(aid_url)
    content = res.content.decode()
    assert 'Vous devez être identifé·e pour utiliser ' \
           'les listes d\'aides' not in content

    assert '<form id="bookmark-form"' in content
    assert '<input type="checkbox" name="bundles" value="{}" ' \
           'id="id_bundles_0" checked>'.format(bundles[0].id) in content
    assert '<label for="id_bundles_0">Bundle_1</label>' in content
    assert '<input type="checkbox" name="bundles" value="{}" ' \
           'id="id_bundles_1" checked>'.format(bundles[1].id) in content
    assert '<label for="id_bundles_1">Bundle_2</label>' in content
    assert '<input type="checkbox" name="bundles" value="{}" ' \
           'id="id_bundles_2">'.format(bundles[2].id) in content
    assert '<label for="id_bundles_2">Bundle_3</label>' in content


def test_bundle_selection_is_effective(client, aid):
    user = aid.author
    bundles = [
        BundleFactory(name='Bundle_1', owner=user, aids=[aid]),
        BundleFactory(name='Bundle_2', owner=user, aids=[aid]),
        BundleFactory(name='Bundle_3', owner=user, aids=[])
    ]

    client.force_login(user)
    aid_url = aid.get_absolute_url()
    client.post(aid_url, {'bundles': [bundles[2].id]})

    aid_bundles = aid.bundles.all()
    assert aid_bundles.count() == 1
    assert aid_bundles[0].id == bundles[2].id


def test_bookmark_form_allows_for_bundle_creation(client, aid):
    user = aid.author
    bundles = [
        BundleFactory(name='Bundle_1', owner=user, aids=[aid]),
        BundleFactory(name='Bundle_2', owner=user, aids=[aid]),
        BundleFactory(name='Bundle_3', owner=user, aids=[])
    ]

    client.force_login(user)
    aid_url = aid.get_absolute_url()
    client.post(aid_url, {
        'bundles': [bundles[2].id], 'new_bundle': 'Bundle_4'})
    aid_bundles = list(aid.bundles.all())
    assert len(aid_bundles) == 2
    assert aid_bundles[0].id == bundles[2].id
    assert aid_bundles[1].name == 'Bundle_4'
