"""Test the goal tracking python/js api."""

import pytest
from django.urls import reverse

from analytics.utils import track_goal


pytestmark = pytest.mark.django_db


def test_no_goal_is_tracked(client, settings):
    settings.COMPRESS_ENABLED = False
    settings.ANALYTICS_ENABLED = True

    home_url = reverse("home")
    res = client.get(home_url)
    content = res.content.decode()

    assert "_paq.push(['trackGoal'" not in content
    assert '&idgoal="' in content


def test_simple_goal_tracking(client, settings):
    settings.COMPRESS_ENABLED = False
    settings.ANALYTICS_ENABLED = True

    session = client.session
    track_goal(session, 666)
    # This is required because of the implementation of test client
    session.save()

    home_url = reverse("home")
    res = client.get(home_url)
    content = res.content.decode()

    assert "_paq.push(['trackGoal', 666])" in content
    assert '&idgoal=666"' in content
