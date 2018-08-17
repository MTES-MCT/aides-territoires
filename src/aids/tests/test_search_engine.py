"""Test methods for the search engine view."""

import pytest
from django.urls import reverse

from aids.factories import AidFactory


pytestmark = pytest.mark.django_db


def test_seach_engine_view(client):
    """Test that the url is publicly accessible."""

    url = reverse('search_view')
    res = client.get(url)
    assert res.status_code == 200


def test_only_published_aids_are_listed(client):
    """Test that aids with a status different than `published` are not shown."""

    AidFactory.create_batch(3)
    url = reverse('search_view')
    res = client.get(url)
    assert res.status_code == 200
    assert len(res.context['aids']) == 3

    # Let's create some non published aids, to check that the list
    # of objects passed to the context does not change
    AidFactory.create_batch(5, status='draft')
    AidFactory.create_batch(7, status='reviewable')
    res = client.get(url)
    assert res.status_code == 200
    assert len(res.context['aids']) == 3

    # Let's add some more published aids, to check that the limit does not
    # come from pagination parameters
    AidFactory.create_batch(11)
    url = reverse('search_view')
    res = client.get(url)
    assert res.status_code == 200
    assert len(res.context['aids']) == 14
