import pytest
from django.urls import reverse

from aids.factories import AidFactory

pytestmark = pytest.mark.django_db


def test_sitemap(client):
    AidFactory(name="First aid")
    AidFactory(name="Draft aid", status="draft")

    url = reverse("sitemap_xml")
    res = client.get(url)

    assert "first-aid" in res.content.decode()
    assert "draft-aid" not in res.content.decode()
    assert res.status_code == 200
