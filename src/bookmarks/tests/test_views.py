import pytest
from django.urls import reverse


pytestmark = pytest.mark.django_db


def test_bookmark_list_is_for_logged_in_users_only(client):
    url = reverse('bookmark_list_view')
    res = client.get(url)
    assert res.status_code == 302


def test_bookmark_create_is_for_logged_in_users_only(client):
    url = reverse('bookmark_create_view')
    res = client.post(url, data={}, follow=True)
    assert res.redirect_chain[0][0].startswith('/comptes/connexion/')