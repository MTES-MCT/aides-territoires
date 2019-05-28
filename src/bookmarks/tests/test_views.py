import pytest
from django.urls import reverse

from bookmarks.models import Bookmark


pytestmark = pytest.mark.django_db


def test_bookmark_list_is_for_logged_in_users_only(client):
    url = reverse('bookmark_list_view')
    res = client.get(url)
    assert res.status_code == 302


def test_bookmark_create_is_for_logged_in_users_only(client):
    url = reverse('bookmark_create_view')
    res = client.post(url, data={}, follow=True)
    assert res.redirect_chain[0][0].startswith('/comptes/connexion/')


def test_bookmark_create_view(user, client):
    bookmarks = Bookmark.objects.all()
    assert bookmarks.count() == 0

    url = reverse('bookmark_create_view')
    client.force_login(user)
    res = client.post(url, data={
        'text': 'Ademe',
        'call_for_projects_only': 'on',
    })
    assert res.status_code == 302
    assert bookmarks.count() == 1

    bookmark = bookmarks[0]
    assert bookmark.owner == user
    assert bookmark.querystring == 'text=Ademe&call_for_projects_only=on'
