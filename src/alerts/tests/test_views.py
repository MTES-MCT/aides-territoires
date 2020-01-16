import time
import pytest
from django.urls import reverse

from accounts.models import User
from alerts.models import Alert
from alerts.factories import AlertFactory


pytestmark = pytest.mark.django_db


def test_alert_list_is_for_logged_in_users_only(client):
    url = reverse('alert_list_view')
    res = client.get(url)
    assert res.status_code == 302


def test_alert_form_displayed_to_users(user, client):
    client.force_login(user)
    url = reverse('search_view')
    res = client.get(url)
    content = res.content.decode()
    assert 'class="user-modal modal"' in content
    assert 'class="anonymous-modal modal"' not in content


def test_alert_form_displayed_to_anonymous(client):
    url = reverse('search_view')
    res = client.get(url)
    content = res.content.decode()
    assert 'class="user-modal modal"' not in content
    assert 'class="anonymous-modal modal"' in content


def test_logged_user_can_create_a_alert(user, client, mailoutbox):
    """Logged users can create new alerts."""

    alerts = Alert.objects.all()
    assert alerts.count() == 0

    url = reverse('alert_create_view')
    client.force_login(user)
    res = client.post(url, data={
        'title': 'My new search',
        'send_email_alert': True,
        'alert_frequency': 'daily',
        'querystring': 'text=Ademe&call_for_projects_only=on',
    })
    assert res.status_code == 302
    assert alerts.count() == 1

    alert = alerts[0]
    assert alert.owner == user
    assert alert.title == 'My new search'
    assert 'text=Ademe' in alert.querystring
    assert 'call_for_projects_only=on' in alert.querystring
    assert len(mailoutbox) == 0


def test_anonymous_can_create_a_alert(client, mailoutbox):
    """Anonymous can create alerts. They receive a validation email."""

    alerts = Alert.objects.all()
    assert alerts.count() == 0

    users = User.objects.all()
    assert users.count() == 0

    url = reverse('alert_create_view')
    res = client.post(url, data={
        'title': 'My new search',
        'email': 'alert-user@example.com',
        'alert_frequency': 'daily',
        'querystring': 'text=Ademe&call_for_projects_only=on',
    })
    assert res.status_code == 302
    assert alerts.count() == 1
    assert users.count() == 1

    user = users[0]
    alert = alerts[0]
    assert alert.owner == user
    assert alert.title == 'My new search'
    assert 'text=Ademe' in alert.querystring
    assert 'call_for_projects_only=on' in alert.querystring

    assert len(mailoutbox) == 1
    mail_body = mailoutbox[0].body
    assert 'Cliquez sur ce lien pour valider votre abonnement au système d\'alertes' in mail_body  # noqa


def test_anonymous_can_create_several_alerts(client, mailoutbox):
    """Anonymous can create several alerts.

    As long as they don't validate their email, we don't require for them
    to log in. Otherwise, it would prevent them to create several alerts
    at once.
    """
    alerts = Alert.objects.order_by('id')
    assert alerts.count() == 0

    users = User.objects.all()
    assert users.count() == 0

    url = reverse('alert_create_view')
    res = client.post(url, data={
        'title': 'My new search',
        'email': 'alert-user@example.com',
        'alert_frequency': 'daily',
        'querystring': 'text=Ademe&call_for_projects_only=on',
    })
    assert res.status_code == 302
    assert alerts.count() == 1
    assert users.count() == 1

    res = client.post(url, data={
        'title': 'My new search 2',
        'email': 'alert-user@example.com',
        'alert_frequency': 'daily',
        'querystring': 'text=Ademe&call_for_projects_only=off',
    })
    assert res.status_code == 302
    assert alerts.count() == 2
    assert users.count() == 1

    user = users[0]
    assert user.last_login is None

    alert = alerts[1]
    assert alert.owner == user
    assert alert.title == 'My new search 2'

    # We only send one validation email for the first alert
    assert len(mailoutbox) == 1
    mail_body = mailoutbox[0].body
    assert 'Cliquez sur ce lien pour valider votre abonnement au système d\'alertes' in mail_body  # noqa


def test_unlogged_user_cannot_create_new_alert(user, client, mailoutbox):
    alerts = Alert.objects.all()
    assert alerts.count() == 0

    users = User.objects.all()
    assert users.count() == 1

    url = reverse('alert_create_view')
    res = client.post(url, data={
        'title': 'My new search',
        'email': user.email,
        'querystring': 'text=Ademe&call_for_projects_only=on',
    })
    assert res.status_code == 302
    assert alerts.count() == 0
    assert users.count() == 1
    assert len(mailoutbox) == 0


def test_delete_alert(user, client):
    AlertFactory.create_batch(5, owner=user)
    alerts = Alert.objects.all()
    assert alerts.count() == 5

    alert_id = alerts[0].id

    url = reverse('alert_delete_view', args=[alert_id])
    client.force_login(user)
    res = client.post(url, data={'pk': alert_id})
    assert res.status_code == 302
    assert alerts.count() == 4

    pks = alerts.values_list('id', flat=True)
    assert alert_id not in pks


def test_user_cannot_delete_someone_else_alert(user, client):
    AlertFactory.create_batch(5)
    alerts = Alert.objects.all()
    assert alerts.count() == 5

    alert_id = alerts[0].id

    url = reverse('alert_delete_view', args=[alert_id])
    client.force_login(user)
    res = client.post(url, data={'pk': alert_id})
    assert res.status_code == 404
    assert alerts.count() == 5


def test_update_alert_alert_settings(user, client):
    alert = AlertFactory(owner=user, send_email_alert=False)
    url = reverse('alert_update_view', args=[alert.pk])
    client.force_login(user)

    client.post(url, data={
        'send_email_alert': True,
        'alert_frequency': 'daily',
    })
    alert.refresh_from_db()
    assert alert.send_email_alert

    client.post(url, data={
        'send_email_alert': False,
        'alert_frequency': 'daily',
    })
    alert.refresh_from_db()
    assert not alert.send_email_alert


def test_user_cannot_update_someone_else_alert(user, client):
    alert = AlertFactory(send_email_alert=False)
    url = reverse('alert_update_view', args=[alert.pk])
    client.force_login(user)

    client.post(url, data={
        'send_email_alert': True,
        'alert_frequency': 'daily',
    })
    alert.refresh_from_db()
    assert not alert.send_email_alert


def test_update_alert_dynamic_ui(user, client, live_server, browser):
    alert = AlertFactory(owner=user, send_email_alert=False)

    # Browser login
    client.force_login(user)
    url = reverse('alert_list_view')
    browser.get(live_server + url)
    cookie = client.cookies['sessionid']
    browser.add_cookie({
        'name': 'sessionid',
        'value': cookie.value,
        'secure': False,
        'path': '/'})
    browser.refresh()

    alerts_div = browser.find_elements_by_css_selector('div.alert')
    assert len(alerts_div) == 1

    checkbox_label = browser.find_element_by_css_selector(
        'label[for=id_send_email_alert_{}]'.format(alert.id))
    checkbox_label.click()
    time.sleep(0.2)

    alert.refresh_from_db()
    assert alert.send_email_alert
