import pytest
from django.urls import reverse

from aids.factories import AidFactory
from aids.models import Aid

pytestmark = pytest.mark.django_db


def test_copy_generic_aid_as_local(client, contributor):

    aid = AidFactory(name='First title', status='published', is_generic=True)
    aids = Aid.objects.all().order_by('id')
    count_before = aids.count()

    client.force_login(contributor)
    url = reverse('aid_generic_to_local_view', args=[aid.slug])
    res = client.post(url)
    assert res.status_code == 302
    aids = Aid.objects.all().order_by('id')
    count_after = aids.count()
    assert count_after == count_before + 1

    assert aids[1].name == 'First title'
    assert aids[1].author == contributor
    assert aids[1].status == 'draft'
    assert aids[1].slug != aids[0].slug
