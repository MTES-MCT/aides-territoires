import pytest

from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_anonymous_user_has_default_search_link_in_header(client):
    res = client.get(reverse("home"))
    assert (
        """<a class="fr-btn at-btn--primary fr-icon-search-line" href="/aides/">
                                    Trouver des aides
                                </a>"""
        in res.content.decode()
    )


def test_logged_in_user_has_custom_search_link_in_header(client, contributor):
    client.force_login(contributor)
    res = client.get(reverse("home"))
    assert "?targeted_audiences=commune&amp;perimeter=1" in res.content.decode()
