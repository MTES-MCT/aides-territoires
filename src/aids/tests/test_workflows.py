import pytest
from django.urls import reverse

from aids.models import Aid
from aids.factories import AidFactory


pytestmark = pytest.mark.django_db


def test_aid_creation_requires_logged_in_user(client):
    """Anonymous users cannot create new aids."""

    form_url = reverse('aid_create_view')
    res = client.get(form_url, follow=True)
    assert res.status_code == 200
    assert len(res.redirect_chain) == 1
    assert res.redirect_chain[0][0].startswith('/comptes/inscription/')


def test_aid_creation_requires_contributor(client, user):
    """Users without contributor cannot create new aids."""

    client.force_login(user)
    form_url = reverse('aid_create_view')
    res = client.get(form_url, follow=True)
    assert res.status_code == 200
    assert len(res.redirect_chain) == 1
    assert res.redirect_chain[0][0].startswith('/comptes/profil-contributeur/')


def test_aid_creation_view(client, contributor, aid_form_data):
    """Saving the form creates a new aid."""

    form_url = reverse('aid_create_view')
    client.force_login(contributor)
    res = client.get(form_url)
    assert res.status_code == 200

    aids = Aid.objects.filter(author=contributor)
    assert aids.count() == 0

    aid_form_data['name'] = 'Very unique title'
    aid_form_data['status'] = 'draft'
    res = client.post(form_url, data=aid_form_data)
    assert res.status_code == 302
    assert aids.count() == 1
    assert aids[0].name == 'Very unique title'
    assert aids[0].author == contributor
    assert aids[0].status == 'draft'


def test_invalid_aid_drafts_can_be_saved(client, contributor):
    """Invalid aids can be saved as drafts."""

    form_url = reverse('aid_create_view')
    client.force_login(contributor)
    res = client.get(form_url)
    assert res.status_code == 200

    aids = Aid.objects.filter(author=contributor)
    assert aids.count() == 0

    data = {
        'name': 'Very unique title',
        'status': 'draft'}
    res = client.post(form_url, data=data)
    assert res.status_code == 302
    assert aids.count() == 1
    assert aids[0].name == 'Very unique title'
    assert aids[0].author == contributor
    assert aids[0].status == 'draft'


def test_drafts_require_at_least_a_title(client, contributor):
    """Invalid aids can be saved as drafts but require a title."""

    form_url = reverse('aid_create_view')
    client.force_login(contributor)
    res = client.get(form_url)
    assert res.status_code == 200

    aids = Aid.objects.filter(author=contributor)
    assert aids.count() == 0

    data = {'status': 'draft'}
    res = client.post(form_url, data=data)
    assert res.status_code == 200
    assert aids.count() == 0


def test_reviewable_aid_creation(client, contributor, aid_form_data):
    """Valid aids can be created with a "reviewable" status."""

    form_url = reverse('aid_create_view')
    client.force_login(contributor)
    aids = Aid.objects.filter(author=contributor)
    assert aids.count() == 0

    aid_form_data['status'] = 'review'
    res = client.post(form_url, data=aid_form_data)
    assert res.status_code == 302
    assert aids.count() == 1
    assert aids[0].status == 'reviewable'


def test_invalid_aids_cannot_become_reviewable(client, contributor):
    """Invalid aids cannot be created with a "reviewable" status."""

    form_url = reverse('aid_create_view')
    client.force_login(contributor)
    aids = Aid.objects.filter(author=contributor)
    assert aids.count() == 0

    invalid_data = {
        'name': 'Almost empty aid',
        'status': 'reviewa'
    }
    res = client.post(form_url, data=invalid_data)
    assert res.status_code == 200
    assert aids.count() == 0


def test_anonymous_cannot_access_edition_form(client, contributor):
    aid = AidFactory(name='Title', author=contributor)
    form_url = reverse('aid_edit_view', args=[aid.slug])
    res = client.get(form_url)
    assert res.status_code == 302


def test_only_aid_owner_can_access_edition_form(client, contributor):
    """Editing someone's else aid is forbidden."""

    aid = AidFactory()
    form_url = reverse('aid_edit_view', args=[aid.slug])
    client.force_login(contributor)
    res = client.get(form_url)
    assert res.status_code == 404


def test_aid_edition_view(client, contributor, aid_form_data):
    """Test the aid edition form and view."""

    aid = AidFactory(name='First title', author=contributor)
    form_url = reverse('aid_edit_view', args=[aid.slug])
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


def test_draft_aids_can_stay_invalid(client, contributor, aid_form_data):
    """Draft aids don't need to be valid to be saved."""

    aid = AidFactory(name='Ttile', author=contributor, status='draft')
    form_url = reverse('aid_edit_view', args=[aid.slug])
    client.force_login(contributor)
    res = client.get(form_url)
    assert res.status_code == 200

    aids = Aid.objects.filter(author=contributor)
    assert aids.count() == 1
    assert aids[0].status == 'draft'

    aid_form_data['description'] = ''
    res = client.post(form_url, data=aid_form_data)
    assert res.status_code == 302
    assert aids.count() == 1
    assert aids[0].description == ''


def test_reviewable_aids_cannot_become_invalid(client, contributor,
                                               aid_form_data):
    """Reviewable aids must stay valid."""

    aid = AidFactory(name='Title', author=contributor, status='reviewable')
    form_url = reverse('aid_edit_view', args=[aid.slug])
    client.force_login(contributor)
    res = client.get(form_url)
    assert res.status_code == 200

    aids = Aid.objects.filter(author=contributor)
    assert aids.count() == 1
    assert aids[0].status == 'reviewable'

    aid_form_data['description'] = ''
    res = client.post(form_url, data=aid_form_data)
    assert res.status_code == 200
    assert aids.count() == 1
    assert aids[0].description != ''


def test_published_aids_cannot_become_invalid(client, contributor,
                                              aid_form_data):
    """Published aids must stay valid."""

    aid = AidFactory(name='Title', author=contributor)
    form_url = reverse('aid_edit_view', args=[aid.slug])
    client.force_login(contributor)
    res = client.get(form_url)
    assert res.status_code == 200

    aids = Aid.objects.filter(author=contributor)
    assert aids.count() == 1
    assert aids[0].status == 'published'

    aid_form_data['description'] = ''
    res = client.post(form_url, data=aid_form_data)
    assert res.status_code == 200
    assert aids.count() == 1
    assert aids[0].description != ''


def test_aid_edition_save_as_new(client, contributor, aid_form_data):
    """Test the "save as new" button."""

    aid = AidFactory(name='First title', status='published',
                     author=contributor)
    aids = Aid.objects.filter(author=contributor).order_by('id')
    assert aids.count() == 1

    client.force_login(contributor)
    form_url = reverse('aid_edit_view', args=[aid.slug])
    aid_form_data['name'] = 'Second title'
    aid_form_data['_save_as_new'] = '_save_as_new'
    res = client.post(form_url, data=aid_form_data)
    assert res.status_code == 302
    assert aids.count() == 2

    assert aids[0].name == 'First title'
    assert '[Copie' in aids[1].name
    assert 'Second title' in aids[1].name

    assert aids[0].status == 'published'
    assert aids[1].status == 'draft'

    assert aids[0].author == aids[1].author == contributor
    assert aids[0].slug != aids[1].slug


def test_save_invalid_aid_as_new(client, contributor, aid_form_data):
    """Invalid drafts can be created by the "save as new" button."""

    aid = AidFactory(name='First title', status='published',
                     author=contributor)
    aids = Aid.objects.filter(author=contributor).order_by('id')
    assert aids.count() == 1

    client.force_login(contributor)
    form_url = reverse('aid_edit_view', args=[aid.slug])
    aid_form_data['name'] = 'Second title'
    aid_form_data['description'] = ''
    aid_form_data['_save_as_new'] = '_save_as_new'
    res = client.post(form_url, data=aid_form_data)
    assert res.status_code == 302
    assert aids.count() == 2

    assert aids[0].name == 'First title'
    assert '[Copie' in aids[1].name
    assert 'Second title' in aids[1].name

    assert aids[0].status == 'published'
    assert aids[1].status == 'draft'

    assert aids[0].author == aids[1].author == contributor
    assert aids[0].slug != aids[1].slug

    assert aids[1].description == ''


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
    assert 'En revue' not in res.content.decode('utf-8')

    contributor.is_superuser = True
    contributor.save()
    res = client.get(url)
    assert res.status_code == 200
    assert 'En revue' in res.content.decode('utf-8')
