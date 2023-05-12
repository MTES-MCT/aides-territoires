"""Test aid views."""

from datetime import timedelta
import pytest
from django.urls import reverse
from django.utils import timezone

from aids.factories import AidFactory, AidProjectFactory
from projects.factories import ProjectFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def past_week():
    today = timezone.now().date()
    return today - timedelta(days=7)


@pytest.fixture
def amendment_form_data(aid_form_data):
    aid_form_data.update(
        {
            "amendment_author_name": "Éric Iki",
            "amendment_author_email": "eric.iki@example.com",
            "amendment_comment": "This is a comment",
        }
    )
    return aid_form_data


def test_draft_list_is_for_authenticated_users_only(client, contributor):
    """Anonymous users cannot access any draft list."""

    drafts_url = reverse("aid_draft_list_view")
    res = client.get(drafts_url)
    assert res.status_code == 302

    client.force_login(contributor)
    res = client.get(drafts_url)
    assert res.status_code == 200


def test_draft_list_only_display_authors_aids(client, contributor):
    """Don't display aids from other users."""

    AidFactory(name="Is this the real life?", author=contributor)
    AidFactory(name="Is this just fantasy?")

    client.force_login(contributor)
    drafts_url = reverse("aid_draft_list_view")
    res = client.get(drafts_url)

    content = res.content.decode("utf-8")
    assert "Is this the real life?" in content
    assert "Is this just fantasy?" not in content


def test_draft_list_does_not_show_deleted_aids(client, contributor):
    """Deleted aids must be excluded from all queries by default."""

    AidFactory(name="Is this the real life?", author=contributor, status="deleted")
    client.force_login(contributor)
    drafts_url = reverse("aid_draft_list_view")
    res = client.get(drafts_url)

    content = res.content.decode("utf-8")
    assert "Is this the real life?" not in content


def test_only_published_aids_are_displayed(client):
    aid = AidFactory(status="draft")
    url = aid.get_absolute_url()
    res = client.get(url)
    assert res.status_code == 404

    aid.status = "reviewable"
    aid.save()
    res = client.get(url)
    assert res.status_code == 404

    aid.status = "published"
    aid.save()
    res = client.get(url)
    assert res.status_code == 200


def test_admin_users_can_preview_unpublished_aids(client, superuser):
    client.force_login(superuser)
    aid = AidFactory(status="draft")
    url = aid.get_absolute_url()
    res = client.get(url)
    assert res.status_code == 200
    assert (
        "Cette aide n’est actuellement pas affichée sur le site."
        in res.content.decode()
    )


def test_contributors_can_preview_their_own_aids(client, user, contributor):
    client.force_login(contributor)
    aid = AidFactory(status="draft", author=user)
    url = aid.get_absolute_url()
    res = client.get(url)
    assert res.status_code == 404

    aid.author = contributor
    aid.save()
    res = client.get(url)
    assert res.status_code == 200
    assert (
        "Cette aide n’est actuellement pas affichée sur le site."
        in res.content.decode()
    )


def test_anonymous_cannot_see_unpublished_aids(client):
    aid = AidFactory(status="draft")
    url = aid.get_absolute_url()
    res = client.get(url)
    assert res.status_code == 404


def test_anonymous_can_see_published_aids(client):
    aid = AidFactory(status="published")
    url = aid.get_absolute_url()
    res = client.get(url)
    assert res.status_code == 200


def test_anonymous_can_see_expired_aids(client, past_week):
    aid = AidFactory(status="published", submission_deadline=past_week)
    url = aid.get_absolute_url()
    res = client.get(url)
    assert res.status_code == 200
    assert "Cette aide n’est plus disponible" in res.content.decode()


def test_superuser_has_a_edit_button(client, superuser):
    client.force_login(superuser)
    aid = AidFactory(status="published")
    url = aid.get_absolute_url()
    res = client.get(url)
    assert res.status_code == 200
    assert "admin-edit-page" in res.content.decode()


def test_others_have_no_edit_button(client, contributor):
    aid = AidFactory(status="published")
    url = aid.get_absolute_url()

    # anonymous
    res = client.get(url)
    assert res.status_code == 200
    assert "admin-edit-page" not in res.content.decode()

    # standard user
    client.force_login(contributor)
    res = client.get(url)
    assert res.status_code == 200
    assert "admin-edit-page" not in res.content.decode()


def test_anonymous_user_can_not_see_aid_stats(client):
    first_aid = AidFactory()
    url = reverse("aid_detail_stats_view", args=[first_aid.slug])
    res = client.get(url)
    assert res.status_code == 302


def test_only_aid_author_can_see_aid_stats(client, contributor):
    client.force_login(contributor)

    first_aid = AidFactory()
    url = reverse("aid_detail_stats_view", args=[first_aid.slug])
    res = client.get(url)
    assert res.status_code == 403

    second_aid = AidFactory(author=contributor)
    url = reverse("aid_detail_stats_view", args=[second_aid.slug])
    res = client.get(url)
    assert res.status_code == 200


def test_admin_user_can_also_see_aid_stats(client, superuser):
    client.force_login(superuser)
    aid = AidFactory()
    url = reverse("aid_detail_stats_view", args=[aid.slug])
    res = client.get(url)
    assert res.status_code == 200


@pytest.fixture
def last_month():
    today = timezone.now()
    return today - timedelta(days=30)


def test_aid_stats_displayed_are_linked_to_a_period(client, contributor, last_month):
    client.force_login(contributor)

    aid = AidFactory(author=contributor)
    first_project = ProjectFactory()
    second_project = ProjectFactory()

    today = timezone.now()
    today_formated = today.strftime("%Y-%m-%d")
    last_month_formated = last_month.strftime("%Y-%m-%d")
    print(today)
    print(last_month)
    print(today_formated)
    print(last_month_formated)

    AidProjectFactory(
        aid=aid, project=first_project, creator=contributor, date_created=today
    )
    AidProjectFactory(
        aid=aid, project=second_project, creator=contributor, date_created=last_month
    )

    url = reverse("aid_detail_stats_view", args=[aid.slug])
    res = client.get(url)
    assert res.status_code == 200
    assert "<strong>1</strong>" in res.content.decode()

    url = reverse("aid_detail_stats_view", args=[aid.slug])
    res = client.get(
        f"{url}?start_date={last_month_formated}&end_date={today_formated}"
    )
    assert res.status_code == 200
    assert "<strong>2</strong>" in res.content.decode()
