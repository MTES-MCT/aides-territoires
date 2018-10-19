"""Test aid views."""

import pytest
from django.urls import reverse

from aids.factories import AidFactory

pytestmark = pytest.mark.django_db


def test_draft_list_is_for_authenticated_users_only(client, user):
    """Anonymous users cannot access any draft list."""

    drafts_url = reverse('aid_draft_list_view')
    res = client.get(drafts_url)
    assert res.status_code == 302

    client.force_login(user)
    res = client.get(drafts_url)
    assert res.status_code == 200


def test_draft_list_only_display_authors_aids(client, user):
    """Don't display aids from other users."""

    AidFactory(name='Is this the real life?', author=user)
    AidFactory(name='Is this just fantasy?')

    client.force_login(user)
    drafts_url = reverse('aid_draft_list_view')
    res = client.get(drafts_url)

    content = res.content.decode('utf-8')
    assert 'Is this the real life?' in content
    assert 'Is this just fantasy?' not in content
