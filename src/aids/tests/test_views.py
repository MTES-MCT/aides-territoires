"""Test aid views."""

import pytest
from django.urls import reverse

from aids.factories import AidFactory
from aids.models import Aid

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


def test_draft_list_does_not_show_deleted_aids(client, user):
    """Deleted aids must be excluded from all queries by default."""

    AidFactory(name='Is this the real life?', author=user,
               status='deleted')
    client.force_login(user)
    drafts_url = reverse('aid_draft_list_view')
    res = client.get(drafts_url)

    content = res.content.decode('utf-8')
    assert 'Is this the real life?' not in content


def test_aid_creation_view(client, user, aid_form_data):
    """Saving the form creates a new aid."""

    # Anonymous, no access
    form_url = reverse('aid_create_view')
    res = client.get(form_url)
    assert res.status_code == 302

    # Logged user, access granted
    client.force_login(user)
    res = client.get(form_url)
    assert res.status_code == 200

    aids = Aid.objects.filter(author=user)
    assert aids.count() == 0

    aid_form_data['name'] = 'Very unique title'
    res = client.post(form_url, data=aid_form_data)
    assert res.status_code == 302
    assert aids.count() == 1
    assert aids[0].name == 'Very unique title'
    assert aids[0].author == user


def test_aid_edition_view(client, user, aid_form_data):
    """Test the aid edition form and view."""

    aid = AidFactory(name='First title', author=user)
    # Anonymous, no access
    form_url = reverse('aid_edit_view', args=[aid.slug])
    res = client.get(form_url)
    assert res.status_code == 302

    # Logged user, access granted
    client.force_login(user)
    res = client.get(form_url)
    assert res.status_code == 200

    aids = Aid.objects.filter(author=user)
    assert aids.count() == 1

    aid_form_data['name'] = 'New title'
    res = client.post(form_url, data=aid_form_data)
    assert res.status_code == 302
    assert aids.count() == 1
    assert aids[0].name == 'New title'
    assert aids[0].author == user


def test_edition_of_other_users_aid(client, user):
    """Editing someone's else aid is forbidden."""

    aid = AidFactory()
    form_url = reverse('aid_edit_view', args=[aid.slug])
    client.force_login(user)
    res = client.get(form_url)
    assert res.status_code == 404


def test_edition_of_aid_status(client, user):
    """Test that the publication workflow works as expected."""

    aid = AidFactory(status='draft', author=user)
    client.force_login(user)

    update_status_url = reverse('aid_status_update_view', args=[aid.slug])
    res = client.get(update_status_url)
    assert res.status_code == 405  # Method not allowed, only post

    res = client.post(update_status_url, {'current_status': 'draft'})
    aid.refresh_from_db()
    assert res.status_code == 302
    assert aid.status == 'reviewable'

    res = client.post(update_status_url, {'current_status': 'reviewable'})
    aid.refresh_from_db()
    assert res.status_code == 302
    assert aid.status == 'draft'

    aid.status = 'published'
    aid.save()

    res = client.post(update_status_url, {'current_status': 'published'})
    aid.refresh_from_db()
    assert res.status_code == 302
    assert aid.status == 'draft'
