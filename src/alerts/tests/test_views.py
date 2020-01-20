import pytest
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from alerts.models import Alert
from alerts.factories import AlertFactory


pytestmark = pytest.mark.django_db


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
    assert users.count() == 0

    alert = alerts[0]
    assert alert.email == 'alert-user@example.com'
    assert alert.title == 'My new search'
    assert 'text=Ademe' in alert.querystring
    assert 'call_for_projects_only=on' in alert.querystring
    assert not alert.validated
    assert alert.date_validated is None

    assert len(mailoutbox) == 1
    mail_body = mailoutbox[0].body
    assert 'Cliquez sur ce lien pour confirmer la création de votre alerte Aides-territoires' in mail_body  # noqa


def test_anonymous_can_create_several_alerts(client, mailoutbox):
    """Anonymous can create several alerts.

    As long as they don't validate their email, we don't require for them
    to log in. Otherwise, it would prevent them to create several alerts
    at once.
    """
    alerts = Alert.objects.order_by('date_created')
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
    assert users.count() == 0

    res = client.post(url, data={
        'title': 'My new search 2',
        'email': 'alert-user@example.com',
        'alert_frequency': 'daily',
        'querystring': 'text=Ademe&call_for_projects_only=off',
    })
    assert res.status_code == 302
    assert alerts.count() == 2
    assert users.count() == 0

    alert = alerts[1]
    assert alert.email == 'alert-user@example.com'
    assert alert.title == 'My new search 2'

    # We send validation email for every alert
    assert len(mailoutbox) == 2
    mail_body = mailoutbox[0].body
    assert 'Cliquez sur ce lien pour confirmer la création de votre alerte Aides-territoires' in mail_body  # noqa


def test_unvalidated_alerts_creation_quotas(client):
    """There is a maximum amount of unvalidated alerts one can create."""

    AlertFactory.create_batch(
        10,
        validated=False,
        email='alert-user@example.com')

    alerts = Alert.objects.all()
    assert alerts.count() == 10

    url = reverse('alert_create_view')
    res = client.post(url, data={
        'title': 'My new search',
        'email': 'alert-user@example.com',
        'alert_frequency': 'daily',
        'querystring': 'text=Ademe&call_for_projects_only=on',
    })
    assert res.status_code == 302
    assert alerts.count() == 10


def test_alert_creation_quotas(client):
    """There is a maximum amount of alerts one can create."""

    AlertFactory.create_batch(
        100,
        email='alert-user@example.com')

    alerts = Alert.objects.all()
    assert alerts.count() == 100

    url = reverse('alert_create_view')
    res = client.post(url, data={
        'title': 'My new search',
        'email': 'alert-user@example.com',
        'alert_frequency': 'daily',
        'querystring': 'text=Ademe&call_for_projects_only=on',
    })
    assert res.status_code == 302
    assert alerts.count() == 100


def test_alert_validation_url(client):
    alert = AlertFactory(validated=False, date_validated=None)
    assert not alert.validated
    assert alert.date_validated is None

    validation_url = reverse('alert_validate_view', args=[alert.token])
    res = client.get(validation_url)
    assert res.status_code == 200

    alert.refresh_from_db()
    assert not alert.validated

    res = client.post(validation_url)
    alert.refresh_from_db()
    assert res.status_code == 302
    assert alert.validated
    assert alert.date_validated.date() == timezone.now().date()


def test_delete_alert(client):
    alerts = Alert.objects.all()

    alert = AlertFactory()
    url = reverse('alert_delete_view', args=[alert.token])
    res = client.get(url)
    assert res.status_code == 200
    assert alerts.count() == 1

    res = client.post(url)
    assert res.status_code == 302
    assert alerts.count() == 0
