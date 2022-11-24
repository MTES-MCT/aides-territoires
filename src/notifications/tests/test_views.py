"""Test user login views."""

import pytest

from django.urls import reverse

from notifications.models import Notification

pytestmark = pytest.mark.django_db


def test_notification_notice(client, user):
    """Authenticated users are notified of unread notifications"""
    Notification.objects.create(recipient=user, message="Sample notification")
    Notification.objects.create(recipient=user, message="Another sample notification")

    client.force_login(user)
    login_url = reverse("login")

    res = client.get(login_url, follow=True)
    assert "Voir les 2 notifications non lues" in res.content.decode()
