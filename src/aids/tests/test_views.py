"""Test aid views."""

import pytest
from django.urls import reverse

from aids.factories import AidFactory
from aids.models import Aid

pytestmark = pytest.mark.django_db


def test_draft_list_is_for_authenticated_users_only(client, contributor):
    """Anonymous users cannot access any draft list."""

    drafts_url = reverse('aid_draft_list_view')
    res = client.get(drafts_url)
    assert res.status_code == 302

    client.force_login(contributor)
    res = client.get(drafts_url)
    assert res.status_code == 200


def test_draft_list_only_display_authors_aids(client, contributor):
    """Don't display aids from other users."""

    AidFactory(name='Is this the real life?', author=contributor)
    AidFactory(name='Is this just fantasy?')

    client.force_login(contributor)
    drafts_url = reverse('aid_draft_list_view')
    res = client.get(drafts_url)

    content = res.content.decode('utf-8')
    assert 'Is this the real life?' in content
    assert 'Is this just fantasy?' not in content


def test_draft_list_does_not_show_deleted_aids(client, contributor):
    """Deleted aids must be excluded from all queries by default."""

    AidFactory(name='Is this the real life?', author=contributor,
               status='deleted')
    client.force_login(contributor)
    drafts_url = reverse('aid_draft_list_view')
    res = client.get(drafts_url)

    content = res.content.decode('utf-8')
    assert 'Is this the real life?' not in content


def test_aid_creation_requires_logged_in_user(client):
    """Anonymous users cannot create new aids."""

    form_url = reverse('aid_create_view')
    res = client.get(form_url, follow=True)
    assert res.status_code == 200
    assert len(res.redirect_chain) == 1
    assert res.redirect_chain[0][0].startswith('/comptes/demande-connexion/')


def test_aid_creation_requires_contributor(client, user):
    """Anonymous users cannot create new aids."""

    client.force_login(user)
    form_url = reverse('aid_create_view')
    res = client.get(form_url, follow=True)
    assert res.status_code == 200
    assert len(res.redirect_chain) == 1
    assert res.redirect_chain[0][0].startswith('/comptes/profil-contributeur/')


def test_aid_creation_view(client, contributor, aid_form_data):
    """Saving the form creates a new aid."""

    form_url = reverse('aid_create_view')

    # Logged user, access granted
    client.force_login(contributor)
    res = client.get(form_url)
    assert res.status_code == 200

    aids = Aid.objects.filter(author=contributor)
    assert aids.count() == 0

    aid_form_data['name'] = 'Very unique title'
    res = client.post(form_url, data=aid_form_data)
    assert res.status_code == 302
    assert aids.count() == 1
    assert aids[0].name == 'Very unique title'
    assert aids[0].author == contributor


def test_aid_edition_view(client, contributor, aid_form_data):
    """Test the aid edition form and view."""

    aid = AidFactory(name='First title', author=contributor)
    # Anonymous, no access
    form_url = reverse('aid_edit_view', args=[aid.slug])
    res = client.get(form_url)
    assert res.status_code == 302

    # Logged contributor, access granted
    client.force_login(contributor)
    res = client.get(form_url)
    assert res.status_code == 200

    aids = Aid.objects.filter(author=contributor)
    assert aids.count() == 1

    aid_form_data['name'] = 'New title'
    res = client.post(form_url, data=aid_form_data)
    assert res.status_code == 302
    assert aids.count() == 1
    assert aids[0].name == 'New title'
    assert aids[0].author == contributor


def test_edition_of_other_users_aid(client, contributor):
    """Editing someone's else aid is forbidden."""

    aid = AidFactory()
    form_url = reverse('aid_edit_view', args=[aid.slug])
    client.force_login(contributor)
    res = client.get(form_url)
    assert res.status_code == 404


def test_edition_of_aid_status(client, contributor):
    """Test that the publication workflow works as expected."""

    aid = AidFactory(status='draft', author=contributor)
    client.force_login(contributor)

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


def test_aid_deletion(client, contributor):
    """Test aid deletion."""

    aid = AidFactory(status='published', author=contributor)
    client.force_login(contributor)
    delete_url = reverse('aid_delete_view', args=[aid.slug])
    res = client.post(delete_url, {'confirm': True})
    assert res.status_code == 302

    aid.refresh_from_db()
    assert aid.status == 'deleted'


def test_deletion_requires_confirmation(client, contributor):
    """Without confirmation, aid does not get deleted."""

    aid = AidFactory(status='published', author=contributor)
    client.force_login(contributor)
    delete_url = reverse('aid_delete_view', args=[aid.slug])
    res = client.post(delete_url)
    assert res.status_code == 302

    aid.refresh_from_db()
    assert aid.status == 'published'


def test_only_aid_author_can_delete_it(client, contributor):
    """One cannot delete other users' aids."""

    aid = AidFactory(status='published')
    client.force_login(contributor)
    delete_url = reverse('aid_delete_view', args=[aid.slug])
    res = client.post(delete_url, {'confirm': True})
    assert res.status_code == 404

    aid.refresh_from_db()
    assert aid.status == 'published'


def test_aids_under_review_menu_is_for_admin_only(client, contributor):
    AidFactory(status='reviewable')
    client.force_login(contributor)
    url = reverse('home')
    res = client.get(url)
    assert res.status_code == 200
    assert 'Aides en revue' not in res.content.decode('utf-8')

    contributor.is_superuser = True
    contributor.save()
    res = client.get(url)
    assert res.status_code == 200
    assert 'Aides en revue' in res.content.decode('utf-8')
