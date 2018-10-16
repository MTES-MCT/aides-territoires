"""Test methods for search results sharing."""

import pytest
from django.urls import reverse
from django.utils.translation import activate


from aids.factories import AidFactory

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def set_default_language():
    activate('fr')


def test_share_button_is_hidden_for_anonymous_users(client):

    AidFactory.create_batch(3)
    url = reverse('search_view')
    res = client.get(url)

    assert res.status_code == 200
    content = res.content.decode('utf-8')
    assert 'envoyer ces résultats par e-mail' not in content


def test_share_button_is_displayed_for_logged_users(client, user):

    AidFactory.create_batch(3)
    client.force_login(user)
    assert user.is_authenticated

    url = reverse('search_view')
    res = client.get(url)

    assert res.status_code == 200
    content = res.content.decode('utf-8')
    assert 'envoyer ces résultats par e-mail' in content
