import pytest
from django.urls import reverse

from geofr.factories import PerimeterFactory
from bookmarks.models import Bookmark
from bookmarks.factories import BookmarkFactory


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


def test_bookmark_title(user, client):
    url = reverse('bookmark_create_view')
    client.force_login(user)
    client.post(url, data={
        'text': 'Ademe',
    })
    bookmarks = Bookmark.objects.order_by('id')
    bookmark = bookmarks.last()
    assert bookmark.title == '« Ademe »'

    client.post(url, data={
        'text': 'Test',
        'perimeter': PerimeterFactory(name='Testville').pk,
    })
    bookmark = bookmarks.last()
    assert bookmark.title == '« Test », Testville'

    client.post(url, data={
        'perimeter': PerimeterFactory(name='Testville2').pk,
    })
    bookmark = bookmarks.last()
    assert bookmark.title == 'Testville2'

    client.post(url, data={})
    bookmarks = Bookmark.objects.all()
    bookmark = bookmarks.last()
    assert bookmark.title == 'Misc'


def test_delete_bookmark(user, client):
    BookmarkFactory.create_batch(5, owner=user)
    bookmarks = Bookmark.objects.all()
    assert bookmarks.count() == 5

    bookmark_id = bookmarks[0].id

    url = reverse('bookmark_delete_view', args=[bookmark_id])
    client.force_login(user)
    res = client.post(url, data={'pk': bookmark_id})
    assert res.status_code == 302
    assert bookmarks.count() == 4

    pks = bookmarks.values_list('id', flat=True)
    assert bookmark_id not in pks


def test_user_cannot_delete_someone_else_bookmark(user, client):
    BookmarkFactory.create_batch(5)
    bookmarks = Bookmark.objects.all()
    assert bookmarks.count() == 5

    bookmark_id = bookmarks[0].id

    url = reverse('bookmark_delete_view', args=[bookmark_id])
    client.force_login(user)
    res = client.post(url, data={'pk': bookmark_id})
    assert res.status_code == 404
    assert bookmarks.count() == 5
