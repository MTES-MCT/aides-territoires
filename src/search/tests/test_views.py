import pytest
from django.urls import reverse

from aids.factories import AidFactory
from search.factories import SearchPageFactory

pytestmark = pytest.mark.django_db


def test_search_page_display(client):
    """Is the seach page slug correctly found from the url?."""

    page = SearchPageFactory(title='Gloubiboulga page')
    page_url = reverse('search_page', args=[page.slug])

    res = client.get(page_url)
    assert res.status_code == 200
    assert 'Gloubiboulga page' in res.content.decode()


def test_search_page_results(client):
    """Test that the saved search query is applied."""

    AidFactory(name="Un repas sans fromage, c'est dommage")
    AidFactory(name="Une soirée sans vin, ce n'est pas malin")

    page = SearchPageFactory(
        title='Gloubiboulga page',
        search_querystring='text=fromage')
    page_url = reverse('search_page', args=[page.slug])
    res = client.get(page_url)

    assert res.status_code == 200
    assert 'fromage' in res.content.decode()
    assert 'malin' not in res.content.decode()


def test_search_page_with_excluded_aids_results(client):
    """Test that the excluded_aids are filtered out."""

    AidFactory(name="Un repas sans fromage, c'est dommage")
    AidFactory(name="Une soirée sans vin, ce n'est pas malin")
    aid_to_exclude = AidFactory(name="Du fromage sans vin, ce n'est pas sain")

    page = SearchPageFactory(
        title='Gloubiboulga page',
        search_querystring='text=fromage')
    page.excluded_aids.set([aid_to_exclude])
    page_url = reverse('search_page', args=[page.slug])
    res = client.get(page_url)

    assert res.status_code == 200
    assert 'fromage' in res.content.decode()
    assert 'malin' not in res.content.decode()
    assert 'sain' not in res.content.decode()


def test_search_query_overriding(client):
    """Test that manual filter add-up on top of initial filter."""

    AidFactory(name="Un repas sans fromage, c'est dommage")
    AidFactory(name="Du fromage sans vin, ce n'est pas sain")
    AidFactory(name="Une soirée sans vin, ce n'est pas malin")

    page = SearchPageFactory(
        title='Gloubiboulga page',
        search_querystring='text=fromage')
    page_url = reverse('search_page', args=[page.slug])
    full_url = '{}?text=vin'.format(page_url)
    res = client.get(full_url)

    assert res.status_code == 200
    assert 'dommage' not in res.content.decode()
    assert 'malin' not in res.content.decode()
    assert 'sain' in res.content.decode()
