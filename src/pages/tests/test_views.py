import pytest

from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_open_redirects_are_forbidden(client):
    base_url = reverse("page_view", args=["https://beta.gouv.fr"])
    res = client.get(base_url)

    assert res.status_code == 403
