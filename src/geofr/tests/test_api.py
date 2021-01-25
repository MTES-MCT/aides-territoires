import json
import pytest
from django.urls import reverse

from geofr.factories import Perimeter, PerimeterFactory


pytestmark = pytest.mark.django_db


@pytest.fixture
def api_url():
    return reverse('perimeters-list')


def test_api(client, api_url):
    PerimeterFactory(name='EPCI 1', scale=Perimeter.TYPES.epci)
    PerimeterFactory(name='Communes littorales', scale=Perimeter.TYPES.adhoc)

    res = client.get(api_url)
    assert res.status_code == 200
    content = json.loads(res.content.decode())
    assert content['count'] == 2 + 2  # already France & Outre-mer


# def test_api_with_q_filter(client, api_url):
#     PerimeterFactory(name='EPCI 1', scale=Perimeter.TYPES.epci)
#     PerimeterFactory(name='Communes littorales', scale=Perimeter.TYPES.adhoc)

#     res = client.get(f'{api_url}?q=epci')
#     assert res.status_code == 200
#     content = json.loads(res.content.decode())
#     assert content['count'] == 1


def test_api_with_is_visible_to_users_filters(client, api_url):
    PerimeterFactory(name='EPCI 1', scale=Perimeter.TYPES.epci)
    PerimeterFactory(name='Communes littorales', scale=Perimeter.TYPES.adhoc,
                     is_visible_to_users=False)

    # Only return Perimeters with is_visible_to_users=True
    res = client.get(f'{api_url}?is_visible_to_users=true')
    assert res.status_code == 200
    content = json.loads(res.content.decode())
    assert content['count'] == 1 + 2  # already France & Outre-mer

    # Return all Perimeters
    res = client.get(f'{api_url}?is_visible_to_users=false')
    assert res.status_code == 200
    content = json.loads(res.content.decode())
    assert content['count'] == 2 + 2  # already France & Outre-mer
