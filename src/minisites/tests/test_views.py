import pytest
from django.urls import reverse

from alerts.models import Alert
from accounts.models import User
from aids.factories import AidFactory
from minisites.factories import MinisiteFactory

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.urls('minisites.urls')
]


def test_minisite_display(client, settings):
    """Is the seach page slug correctly found from the host?"""

    page = MinisiteFactory(title='Gloubiboulga page')
    page_url = reverse('home')
    page_host = '{}.testserver'.format(page.slug)
    settings.ALLOWED_HOSTS = [page_host]

    res = client.get(page_url, HTTP_HOST=page_host)
    assert res.status_code == 200
    assert 'Gloubiboulga page' in res.content.decode()


def test_minisite_results(client, settings):
    """Test that the saved search query is applied."""

    AidFactory(name="Un repas sans fromage, c'est dommage")
    AidFactory(name="Une soirée sans vin, ce n'est pas malin")

    page = MinisiteFactory(
        title='Gloubiboulga page',
        search_querystring='text=fromage')
    page_url = reverse('home')
    page_host = '{}.testserver'.format(page.slug)
    settings.ALLOWED_HOSTS = [page_host]

    res = client.get(page_url, HTTP_HOST=page_host)
    assert res.status_code == 200
    assert 'fromage' in res.content.decode()
    assert 'malin' not in res.content.decode()


def test_minisite_results_overriding(client, settings):
    """Test that manual filters override saved ones."""

    AidFactory(name="Un repas sans fromage, c'est dommage")
    AidFactory(name="Une soirée sans vin, ce n'est pas malin")

    page = MinisiteFactory(
        title='Gloubiboulga page',
        search_querystring='text=fromage')
    page_url = reverse('home')
    full_url = '{}?text=vin'.format(page_url)
    page_host = '{}.testserver'.format(page.slug)
    settings.ALLOWED_HOSTS = [page_host]

    res = client.get(full_url, HTTP_HOST=page_host)
    assert res.status_code == 200
    assert 'fromage' not in res.content.decode()
    assert 'malin' in res.content.decode()


def test_alert_creation(client, settings, mailoutbox):
    """Anonymous can create alerts. They receive a validation email."""

    alerts = Alert.objects.all()
    assert alerts.count() == 0

    users = User.objects.all()
    assert users.count() == 0

    page = MinisiteFactory(
        title='Gloubiboulga page',
        search_querystring='text=fromage')
    page_host = '{}.testserver'.format(page.slug)
    settings.ALLOWED_HOSTS = [page_host]

    url = reverse('alert_create_view')
    res = client.post(url, data={
        'title': 'My new search',
        'email': 'alert-user@example.com',
        'alert_frequency': 'daily',
        'querystring': 'text=Ademe&call_for_projects_only=on',
    }, HTTP_HOST=page_host)
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
