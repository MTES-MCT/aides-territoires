import json
import pytest
from django.urls import reverse

from aids.factories import AidFactory


pytestmark = pytest.mark.django_db

@pytest.fixture
def api_url():
    return reverse('aids-list')


def test_api_default_version(client, api_url):
    AidFactory(name='First aid')
    AidFactory(name='Second aid')

    res = client.get(api_url)
    assert res.status_code == 200
    content = json.loads(res.content.decode())
    assert content['count'] == 2


def test_api_version_1_0(client, api_url):
    AidFactory(name='First aid')
    AidFactory(name='Second aid')

    res = client.get(f'{api_url}?version=1.0')
    assert res.status_code == 200
    content = json.loads(res.content.decode())
    assert content['count'] == 2


def test_api_invalid_version(client, api_url):
    AidFactory(name='First aid')
    AidFactory(name='Second aid')

    res = client.get('f{api_url}?version=42')
    assert res.status_code == 404
