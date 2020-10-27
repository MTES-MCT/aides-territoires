import pytest
from django.urls import reverse

from alerts.models import Alert
from accounts.models import User
from aids.factories import AidFactory
from categories.factories import CategoryFactory
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
    """Test that manual filter add-up on top of initial filter."""

    AidFactory(name="Un repas sans fromage, c'est dommage")
    AidFactory(name="Du fromage sans vin, ce n'est pas sain")
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
    assert 'dommage' not in res.content.decode()
    assert 'malin' not in res.content.decode()
    assert 'sain' in res.content.decode()


def test_categories_filter_overriding(client, settings):
    categories = [
        CategoryFactory(name='Category 1'),
        CategoryFactory(name='Category 2'),
        CategoryFactory(name='Category 3'),
        CategoryFactory(name='Category 4'),
        CategoryFactory(name='Category 5'),
    ]

    # We create a minisite with all categories pre-filter
    page = MinisiteFactory(
        title='Gloubiboulga page',
        search_querystring='text=fromage')
    page.available_categories.set(categories)
    page_url = reverse('search_view')
    page_host = '{}.testserver'.format(page.slug)
    settings.ALLOWED_HOSTS = [page_host]

    # All categories appear in the form
    res = client.get(page_url, HTTP_HOST=page_host)
    assert res.status_code == 200
    content = res.content.decode()
    assert '<option value="category-1"' in content
    assert '<option value="category-2"' in content
    assert '<option value="category-3"' in content
    assert '<option value="category-4"' in content
    assert '<option value="category-5"' in content

    # We create a minisite with a category pre-filter
    page = MinisiteFactory(
        title='Gloubiboulga page 2',
        search_querystring='text=fromage')
    page.available_categories.set(categories[:2])
    page_url = reverse('search_view')
    page_host = '{}.testserver'.format(page.slug)
    settings.ALLOWED_HOSTS = [page_host]

    # Only the available categories appear in the form
    res = client.get(page_url, HTTP_HOST=page_host)
    assert res.status_code == 200
    content = res.content.decode()
    assert '<option value="category-1"' in content
    assert '<option value="category-2"' in content
    assert '<option value="category-3"' not in content
    assert '<option value="category-4"' not in content
    assert '<option value="category-5"' not in content


def test_audiences_filter_overriding(client, settings):

    # We create a minisite with no audiences pre-filter
    page = MinisiteFactory(
        title='Gloubiboulga page',
        search_querystring='text=fromage')
    page_url = reverse('search_view')
    page_host = '{}.testserver'.format(page.slug)
    settings.ALLOWED_HOSTS = [page_host]

    # All audiences appear in the form
    res = client.get(page_url, HTTP_HOST=page_host)
    assert res.status_code == 200
    content = res.content.decode()
    assert '<option value="commune">' not in content
    assert '<option value="epci">' not in content
    assert '<option value="association">' not in content
    assert '<option value="region">' not in content

    # We create a minisite with an audience pre-filter
    page = MinisiteFactory(
        title='Gloubiboulga page 2',
        search_querystring='text=fromage',
        available_audiences=['commune', 'epci'])
    page_url = reverse('search_view')
    page_host = '{}.testserver'.format(page.slug)
    settings.ALLOWED_HOSTS = [page_host]

    # Only the available audiences appear in the form
    res = client.get(page_url, HTTP_HOST=page_host)
    assert res.status_code == 200
    content = res.content.decode()
    assert '<option value="commune">' in content
    assert '<option value="epci">' in content
    assert '<option value="association">' not in content
    assert '<option value="region">' not in content


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
