import pytest
from django.urls import reverse

from backers.factories import BackerFactory


pytestmark = pytest.mark.django_db


def test_backer_details_page_loads(client, contributor):
    backer = BackerFactory(name="Some Backer", slug="some-backer")
    url = reverse("backer_detail_view", args=[backer.pk, backer.slug])
    response = client.get(url)
    assert response.status_code == 200
    assert "Some Backer" in str(response.content)
