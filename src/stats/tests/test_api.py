import json
import pytest

from django.urls import reverse

from stats.models import AidContactClickEvent
from aids.factories import AidFactory


pytestmark = pytest.mark.django_db


@pytest.fixture
def api_url():
    return reverse('aid-contact-click-events-list')


def test_aid_contact_click_events_api(client, api_url):
    aid = AidFactory()
    assert AidContactClickEvent.objects.count() == 0

    # querystring should be passed
    data = {
        'aid': aid.id,
        # 'querystring': ''
    }
    res = client.post(api_url, data=data)
    assert AidContactClickEvent.objects.count() == 0

    # querystring can be empty
    data = {
        'aid': aid.id,
        'querystring': ''
    }
    res = client.post(api_url, data=data)
    assert AidContactClickEvent.objects.count() == 1

    # querystring will be cleaned
    data = {
        'aid': aid.id,
        'querystring': 'perimeter=&aid_type=financial'
    }
    res = client.post(api_url, data=data)
    assert AidContactClickEvent.objects.count() == 2
    event = AidContactClickEvent.objects.last()
    assert event.querystring == 'aid_type=financial'
