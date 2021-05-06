"""Test aid views."""

from datetime import timedelta
import pytest
from django.urls import reverse
from django.utils import timezone

from aids.factories import AidFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def past_week():
    today = timezone.now().date()
    return today - timedelta(days=7)


@pytest.fixture
def amendment_form_data(aid_form_data):
    aid_form_data.update({
        'amendment_author_name': 'Éric Iki',
        'amendment_author_email': 'eric.iki@example.com',
        'amendment_comment': 'This is a comment',
    })
    return aid_form_data


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
    assert res.redirect_chain[0][0].startswith('/comptes/inscription/')


def test_aid_creation_requires_contributor(client, user):
    """Anonymous users cannot create new aids."""

    client.force_login(user)
    form_url = reverse('aid_create_view')
    res = client.get(form_url, follow=True)
    assert res.status_code == 200
    assert len(res.redirect_chain) == 1
    assert res.redirect_chain[0][0].startswith('/comptes/profil-contributeur/')


def test_aid_creation_view(client, contributor, amendment_form_data):
    """Saving the form creates a new aid."""

    form_url = reverse('aid_create_view')

    # Logged user, access granted
    client.force_login(contributor)
    res = client.get(form_url)
    assert res.status_code == 200

    aids = Aid.objects.filter(author=contributor)
    assert aids.count() == 0

    amendment_form_data['name'] = 'Very unique title'
    res = client.post(form_url, data=amendment_form_data)
    assert res.status_code == 302
    assert aids.count() == 1
    assert aids[0].name == 'Very unique title'
    assert aids[0].author == contributor
    assert aids[0].status == 'draft'


def test_aid_creation_status_as_draft(client, contributor,
                                      amendment_form_data):

    form_url = reverse('aid_create_view')
    client.force_login(contributor)
    aids = Aid.objects.filter(author=contributor)
    amendment_form_data['status'] = 'draft'
    res = client.post(form_url, data=amendment_form_data)
    assert res.status_code == 302
    assert aids.count() == 1
    assert aids[0].status == 'draft'


def test_aid_creation_status_as_review(client, contributor,
                                       amendment_form_data):

    form_url = reverse('aid_create_view')
    client.force_login(contributor)
    aids = Aid.objects.filter(author=contributor)
    amendment_form_data['status'] = 'review'
    res = client.post(form_url, data=amendment_form_data)
    assert res.status_code == 302
    assert aids.count() == 1
    assert aids[0].status == 'reviewable'


def test_aid_edition_view(client, contributor, amendment_form_data):
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

    amendment_form_data['name'] = 'New title'
    res = client.post(form_url, data=amendment_form_data)
    assert res.status_code == 302
    assert aids.count() == 1
    assert aids[0].name == 'New title'
    assert aids[0].author == contributor


def test_aid_edition_save_as_new(client, contributor, amendment_form_data):
    """Test the "save as new" button."""

    aid = AidFactory(name='First title', status='published',
                     author=contributor)
    aids = Aid.objects.filter(author=contributor).order_by('id')
    assert aids.count() == 1

    client.force_login(contributor)
    form_url = reverse('aid_edit_view', args=[aid.slug])
    amendment_form_data['name'] = 'Second title'
    amendment_form_data['_save_as_new'] = '_save_as_new'
    res = client.post(form_url, data=amendment_form_data)
    assert res.status_code == 302
    assert aids.count() == 2

    assert aids[0].name == 'First title'
    assert '[Copie' in aids[1].name
    assert 'Second title' in aids[1].name

    assert aids[0].status == 'published'
    assert aids[1].status == 'draft'

    assert aids[0].author == aids[1].author == contributor
    assert aids[0].slug != aids[1].slug


def test_copy_generic_aid_as_local(client, contributor):

    aid = AidFactory(name='First title', status='published', is_generic=True)
    aids = Aid.objects.all().order_by('id')
    count_before = aids.count()

    client.force_login(contributor)
    url = reverse('aid_generic_to_local_view', args=[aid.slug])
    res = client.post(url)
    assert res.status_code == 302
    aids = Aid.objects.all().order_by('id')
    count_after = aids.count()
    assert count_after == count_before + 1

    assert aids[1].name == 'First title'
    assert aids[1].author == contributor
    assert aids[1].status == 'draft'
    assert aids[1].slug != aids[0].slug
    assert aids[1].generic_aid.id == aids[0].id


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
    assert 'En revue' not in res.content.decode('utf-8')

    contributor.is_superuser = True
    contributor.save()
    res = client.get(url)
    assert res.status_code == 200
    assert 'En revue' in res.content.decode('utf-8')


def test_only_published_aids_are_displayed(client):
    aid = AidFactory(status='draft')
    url = aid.get_absolute_url()
    res = client.get(url)
    assert res.status_code == 404

    aid.status = 'reviewable'
    aid.save()
    res = client.get(url)
    assert res.status_code == 404

    aid.status = 'published'
    aid.save()
    res = client.get(url)
    assert res.status_code == 200


def test_admin_users_can_preview_unpublished_aids(client, superuser):
    client.force_login(superuser)
    aid = AidFactory(status='draft')
    url = aid.get_absolute_url()
    res = client.get(url)
    assert res.status_code == 200
    assert 'Cette aide <strong>n\'est actuellement pas affichée sur le site</strong>.' in res.content.decode()  # noqa


def test_contributons_can_preview_their_own_aids(client, user, contributor):
    client.force_login(contributor)
    aid = AidFactory(status='draft', author=user)
    url = aid.get_absolute_url()
    res = client.get(url)
    assert res.status_code == 404

    aid.author = contributor
    aid.save()
    res = client.get(url)
    assert res.status_code == 200
    assert 'Cette aide <strong>n\'est actuellement pas affichée sur le site</strong>.' in res.content.decode()  # noqa


def test_anonymous_cannot_see_unpublished_aids(client):
    aid = AidFactory(status='draft')
    url = aid.get_absolute_url()
    res = client.get(url)
    assert res.status_code == 404


def test_anonymous_can_see_published_aids(client):
    aid = AidFactory(status='published')
    url = aid.get_absolute_url()
    res = client.get(url)
    assert res.status_code == 200


def test_anonymous_can_see_expired_aids(client, past_week):
    aid = AidFactory(status='published', submission_deadline=past_week)
    url = aid.get_absolute_url()
    res = client.get(url)
    assert res.status_code == 200
    assert 'Cette aide n\'est <strong>plus disponible</strong>' in res.content.decode() # noqa
