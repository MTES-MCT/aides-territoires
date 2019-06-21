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


def test_anonymous_user_cannot_see_the_bundle_form(client, aid):
    """Aid bundles requires a logged in account."""
    aid_url = aid.get_absolute_url()
    res = client.get(aid_url)
    content = res.content.decode()

    assert 'Vous devez être identifé·e pour utiliser ' \
           'les listes d\'aides' in content


def test_anonymous_user_cannot_bundle_aids(client, aid):
    aid_url = aid.get_absolute_url()
    res = client.post(aid_url)
    assert res.status_code == 405  # method not allowed


def test_bundle_modal_shows_selected_bundles(
        live_server, browser, client, aid):
    """Authenticated users cannot login again, duh!"""

    user = aid.author
    [
        BundleFactory(name='Bundle_1', owner=user, aids=[aid]),
        BundleFactory(name='Bundle_2', owner=user, aids=[aid]),
        BundleFactory(name='Bundle_3', owner=user, aids=[])
    ]

    # Browser login
    client.force_login(user)
    cookie = client.cookies['sessionid']
    aid_url = live_server + aid.get_absolute_url()
    browser.get(aid_url)
    browser.add_cookie({'name': 'sessionid', 'value': cookie.value,
                        'secure': False, 'path': '/'})
    browser.refresh()

    modal = browser.find_element_by_id('bundle-modal')
    content = modal.get_attribute('innerHTML')
    assert 'Vous devez être identifé·e pour utiliser ' \
           'les listes d\'aides' not in content
    assert '<form id="bundle-form"' in content

    input0 = browser.find_element_by_id('id_bundles_0')
    assert input0.is_selected()

    input1 = browser.find_element_by_id('id_bundles_1')
    assert input1.is_selected()

    input2 = browser.find_element_by_id('id_bundles_2')
    assert not input2.is_selected()


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


def test_bundle_form_allows_for_bundle_creation(client, aid):
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
