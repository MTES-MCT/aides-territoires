import pytest

from bs4 import BeautifulSoup

from django.urls import reverse

from notifications.factories import NotificationFactory

pytestmark = pytest.mark.django_db


def test_authenticated_notification_notice_if_notifications_present(client, user):
    """Authenticated users are notified of unread notifications"""
    NotificationFactory(recipient=user, title="Unread notification")
    NotificationFactory(recipient=user, title="Another unread notification")

    read = NotificationFactory(recipient=user, title="Read notification")
    read.mark_as_read()
    read.save()

    client.force_login(user)
    login_url = reverse("login")

    res = client.get(login_url, follow=True)
    assert "Voir les 2 notifications non lues" in res.content.decode()
    assert "at-notification-icon" in res.content.decode()


def test_authenticated_notification_no_notice_if_no_notification(client, user):
    """Authenticated users do not have the bell icon if no unread notification"""

    read = NotificationFactory(recipient=user, title="Read notification")
    read.mark_as_read()
    read.save()

    client.force_login(user)
    login_url = reverse("login")

    res = client.get(login_url, follow=True)
    assert "at-notification-icon" not in res.content.decode()


def test_notification_list_displays_notifications(client, user):
    """Unread notifications are in bold, read notifications are not"""
    read = NotificationFactory(recipient=user, title="Read notification")
    unread = NotificationFactory(recipient=user, title="Unread notification")

    read.mark_as_read()
    read.save()

    client.force_login(user)
    url = reverse("notification_list_view")

    res = client.get(url)

    soup = BeautifulSoup(res.content.decode(), "html.parser")

    unread = soup.find(id=f"notification-{unread.pk}")
    read = soup.find(id=f"notification-{read.pk}")

    assert "strong" in str(unread)
    assert "strong" not in str(read)
