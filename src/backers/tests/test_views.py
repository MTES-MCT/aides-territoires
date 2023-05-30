import pytest
from django.urls import reverse

from backers.factories import BackerFactory
from geofr.models import Perimeter


pytestmark = pytest.mark.django_db


def test_backer_details_page_loads(client, contributor):
    backer = BackerFactory(name="Some Backer", slug="some-backer")
    url = reverse("backer_detail_view", args=[backer.pk, backer.slug])
    response = client.get(url)
    assert response.status_code == 200
    assert "Some Backer" in str(response.content)


def test_backer_exclusion_list_page_loads(client, contributor):
    """Already excluded backers should be properly marked"""
    BackerFactory(name="Allowed_backer", perimeter=Perimeter.objects.first())
    backer_excluded = BackerFactory(
        name="Excluded_backer", perimeter=Perimeter.objects.first()
    )

    contributor.excluded_backers.add(backer_excluded)
    contributor.save()
    client.force_login(contributor)
    url = reverse("backers_exclusion_list")
    response = client.get(url)
    assert "1 porteur masqué." in response.content.decode()


def test_toggle_backer_exclude_view(client, contributor):
    backer_to_exclude = BackerFactory(
        name="Backer to exclude", perimeter=Perimeter.objects.first()
    )

    client.force_login(contributor)
    url = reverse(
        "toggle_backer_exclude_view",
        args=[backer_to_exclude.pk],
    )
    response = client.post(url, data={"excluded": 1})

    assert '"status": "success"' in response.content.decode()
    assert '"nb_excluded": 1' in response.content.decode()
