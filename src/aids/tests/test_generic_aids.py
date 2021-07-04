from datetime import timedelta
import pytest

from django.urls import reverse
from django.utils import timezone

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


def test_local_aid_date_is_copied_to_generic_aid(client, contributor):
    today = timezone.now().date()
    tomorrow = today + timedelta(days=1)
    next_week = today + timedelta(weeks=1)
    generic = AidFactory(status='published', is_generic=True, submission_deadline=today)
    local_1 = AidFactory(status='draft', generic_aid=generic, submission_deadline=tomorrow)
    local_2 = AidFactory(status='draft', generic_aid=generic, submission_deadline=next_week)
    assert generic.submission_deadline == today
    local_1.status = 'published'
    local_1.save()
    local_2.status = 'published'
    local_2.save()
    generic = Aid.objects.get(pk=generic.pk)
    assert generic.submission_deadline == next_week
