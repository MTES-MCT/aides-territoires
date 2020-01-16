import time
import pytest
from django.urls import reverse

from accounts.models import User
from alerts.models import Bookmark
from alerts.factories import BookmarkFactory


pytestmark = pytest.mark.django_db


def test_bookmark_list_is_for_logged_in_users_only(client):
    url = reverse('bookmark_list_view')
    res = client.get(url)
    assert res.status_code == 302


def test_bookmark_form_displayed_to_users(user, client):
    client.force_login(user)
    url = reverse('search_view')
    res = client.get(url)
    content = res.content.decode()
    assert 'class="user-modal modal"' in content
    assert 'class="anonymous-modal modal"' not in content


def test_bookmark_form_displayed_to_anonymous(client):
    url = reverse('search_view')
    res = client.get(url)
    content = res.content.decode()
    assert 'class="user-modal modal"' not in content
    assert 'class="anonymous-modal modal"' in content


def test_logged_user_can_create_a_bookmark(user, client, mailoutbox):
    """Logged users can create new bookmarks."""

    bookmarks = Bookmark.objects.all()
    assert bookmarks.count() == 0

    url = reverse('bookmark_create_view')
    client.force_login(user)
    res = client.post(url, data={
        'title': 'My new search',
        'send_email_alert': True,
        'alert_frequency': 'daily',
        'querystring': 'text=Ademe&call_for_projects_only=on',
    })
    assert res.status_code == 302
    assert bookmarks.count() == 1

    bookmark = bookmarks[0]
    assert bookmark.owner == user
    assert bookmark.title == 'My new search'
    assert 'text=Ademe' in bookmark.querystring
    assert 'call_for_projects_only=on' in bookmark.querystring
    assert len(mailoutbox) == 0


def test_anonymous_can_create_a_bookmark(client, mailoutbox):
    """Anonymous can create bookmarks. They receive a validation email."""

    bookmarks = Bookmark.objects.all()
    assert bookmarks.count() == 0

    users = User.objects.all()
    assert users.count() == 0

    url = reverse('bookmark_create_view')
    res = client.post(url, data={
        'title': 'My new search',
        'email': 'bookmark-user@example.com',
        'alert_frequency': 'daily',
        'querystring': 'text=Ademe&call_for_projects_only=on',
    })
    assert res.status_code == 302
    assert bookmarks.count() == 1
    assert users.count() == 1

    user = users[0]
    bookmark = bookmarks[0]
    assert bookmark.owner == user
    assert bookmark.title == 'My new search'
    assert 'text=Ademe' in bookmark.querystring
    assert 'call_for_projects_only=on' in bookmark.querystring

    assert len(mailoutbox) == 1
    mail_body = mailoutbox[0].body
    assert 'Cliquez sur ce lien pour valider votre abonnement au système d\'alertes' in mail_body  # noqa


def test_anonymous_can_create_several_bookmarks(client, mailoutbox):
    """Anonymous can create several bookmarks.

    As long as they don't validate their email, we don't require for them
    to log in. Otherwise, it would prevent them to create several bookmarks
    at once.
    """
    bookmarks = Bookmark.objects.order_by('id')
    assert bookmarks.count() == 0

    users = User.objects.all()
    assert users.count() == 0

    url = reverse('bookmark_create_view')
    res = client.post(url, data={
        'title': 'My new search',
        'email': 'bookmark-user@example.com',
        'alert_frequency': 'daily',
        'querystring': 'text=Ademe&call_for_projects_only=on',
    })
    assert res.status_code == 302
    assert bookmarks.count() == 1
    assert users.count() == 1

    res = client.post(url, data={
        'title': 'My new search 2',
        'email': 'bookmark-user@example.com',
        'alert_frequency': 'daily',
        'querystring': 'text=Ademe&call_for_projects_only=off',
    })
    assert res.status_code == 302
    assert bookmarks.count() == 2
    assert users.count() == 1

    user = users[0]
    assert user.last_login is None

    bookmark = bookmarks[1]
    assert bookmark.owner == user
    assert bookmark.title == 'My new search 2'

    # We only send one validation email for the first bookmark
    assert len(mailoutbox) == 1
    mail_body = mailoutbox[0].body
    assert 'Cliquez sur ce lien pour valider votre abonnement au système d\'alertes' in mail_body  # noqa


def test_unlogged_user_cannot_create_new_bookmark(user, client, mailoutbox):
    bookmarks = Bookmark.objects.all()
    assert bookmarks.count() == 0

    users = User.objects.all()
    assert users.count() == 1

    url = reverse('bookmark_create_view')
    res = client.post(url, data={
        'title': 'My new search',
        'email': user.email,
        'querystring': 'text=Ademe&call_for_projects_only=on',
    })
    assert res.status_code == 302
    assert bookmarks.count() == 0
    assert users.count() == 1
    assert len(mailoutbox) == 0


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


def test_update_bookmark_alert_settings(user, client):
    bookmark = BookmarkFactory(owner=user, send_email_alert=False)
    url = reverse('bookmark_update_view', args=[bookmark.pk])
    client.force_login(user)

    client.post(url, data={
        'send_email_alert': True,
        'alert_frequency': 'daily',
    })
    bookmark.refresh_from_db()
    assert bookmark.send_email_alert

    client.post(url, data={
        'send_email_alert': False,
        'alert_frequency': 'daily',
    })
    bookmark.refresh_from_db()
    assert not bookmark.send_email_alert


def test_user_cannot_update_someone_else_bookmark(user, client):
    bookmark = BookmarkFactory(send_email_alert=False)
    url = reverse('bookmark_update_view', args=[bookmark.pk])
    client.force_login(user)

    client.post(url, data={
        'send_email_alert': True,
        'alert_frequency': 'daily',
    })
    bookmark.refresh_from_db()
    assert not bookmark.send_email_alert


def test_update_bookmark_dynamic_ui(user, client, live_server, browser):
    bookmark = BookmarkFactory(owner=user, send_email_alert=False)

    # Browser login
    client.force_login(user)
    url = reverse('bookmark_list_view')
    browser.get(live_server + url)
    cookie = client.cookies['sessionid']
    browser.add_cookie({
        'name': 'sessionid',
        'value': cookie.value,
        'secure': False,
        'path': '/'})
    browser.refresh()

    bookmarks_div = browser.find_elements_by_css_selector('div.bookmark')
    assert len(bookmarks_div) == 1

    checkbox_label = browser.find_element_by_css_selector(
        'label[for=id_send_email_alert_{}]'.format(bookmark.id))
    checkbox_label.click()
    time.sleep(0.2)

    bookmark.refresh_from_db()
    assert bookmark.send_email_alert
