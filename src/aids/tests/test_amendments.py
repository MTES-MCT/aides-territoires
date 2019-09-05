import pytest
from django.urls import reverse

from aids.factories import AidFactory
from aids.models import Aid

pytestmark = pytest.mark.django_db


def test_anonymous_can_amend_aids(client):
    aid = AidFactory()
    amend_url = reverse('aid_amend_view', args=[aid.slug])
    res = client.get(amend_url)
    assert res.status_code == 200

    text = 'You have the possibility to <strong>suggest amendments</strong>'
    content = res.content.decode()
    assert text in content


def test_aid_amendments_are_saved(client, aid_form_data):
    # At the beginning of the test, no amendments exist
    amendments = Aid.amendments.all()
    assert amendments.count() == 0

    aid = AidFactory(
        name='This is my aid name',
        description='This is a mistake')
    amend_url = reverse('aid_amend_view', args=[aid.slug])
    aid_form_data.update({
        'name': 'This is a better name',
        'description': 'This is a correction'
    })
    res = client.post(amend_url, data=aid_form_data)
    assert res.status_code == 302
    assert amendments.count() == 1

    # The amendment was successfully created
    amendment = amendments[0]
    assert amendment.name == 'This is a better name'
    assert amendment.description == 'This is a correction'
    assert amendment.author is None
    assert amendment.amended_aid == aid

    # The amended aid was NOT modified
    aid.refresh_from_db()
    assert aid.name == 'This is my aid name'
    assert aid.description == 'This is a mistake'
