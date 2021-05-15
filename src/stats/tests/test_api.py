import pytest

from django.urls import reverse

from stats.models import AidContactClickEvent, AidMatchProjectEvent
from aids.factories import AidFactory
from projects.factories import ProjectFactory


pytestmark = pytest.mark.django_db


@pytest.fixture
def contact_api_url():
    return reverse('aid-contact-click-events-list')

@pytest.fixture
def project_api_url():
    return reverse('aid-match-project-events-list')


def test_aid_contact_click_events_api(client, contact_api_url):
    aid = AidFactory()
    assert AidContactClickEvent.objects.count() == 0

    # querystring should be passed
    data = {
        'aid': aid.id,
        # 'querystring': ''
    }
    client.post(contact_api_url, data=data)
    assert AidContactClickEvent.objects.count() == 0

    # querystring can be empty
    data = {
        'aid': aid.id,
        'querystring': ''
    }
    client.post(contact_api_url, data=data)
    assert AidContactClickEvent.objects.count() == 1

    # querystring will be cleaned
    data = {
        'aid': aid.id,
        'querystring': 'perimeter=&aid_type=financial'
    }
    client.post(contact_api_url, data=data)
    assert AidContactClickEvent.objects.count() == 2
    event = AidContactClickEvent.objects.last()
    assert event.querystring == 'aid_type=financial'


def test_aid_match_project_event_api(client, project_api_url):
    aid = AidFactory()
    project = ProjectFactory()
    assert AidMatchProjectEvent.objects.count() == 0

    # querystring should be passed
    data = {
        'aid': aid.id,
        'project': project.id,
        # 'querystring': ''
    }
    client.post(project_api_url, data=data)
    assert AidMatchProjectEvent.objects.count() == 0

    # is_matching will default to False if not passed
    data = {
        'aid': aid.id,
        'project': project.id,
        'querystring': '?text=coucou'
    }
    client.post(project_api_url, data=data)
    assert AidMatchProjectEvent.objects.count() == 1
    event = AidMatchProjectEvent.objects.last()
    assert event.is_matching == False

    # querystring can be empty
    data = {
        'aid': aid.id,
        'project': project.id,
        'is_matching': True,
        'querystring': ''
    }
    client.post(project_api_url, data=data)
    assert AidMatchProjectEvent.objects.count() == 2
    event = AidMatchProjectEvent.objects.last()
    assert event.is_matching == True

    # querystring will be cleaned
    data = {
        'aid': aid.id,
        'project': project.id,
        'is_matching': 'true',
        'querystring': 'perimeter=&aid_type=financial'
    }
    client.post(project_api_url, data=data)
    assert AidMatchProjectEvent.objects.count() == 3
    event = AidMatchProjectEvent.objects.last()
    assert event.querystring == 'aid_type=financial'
