import pytest

from bs4 import BeautifulSoup

from django.urls import reverse
from accounts.factories import UserFactory

from notifications.factories import NotificationFactory
from notifications.models import Notification

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


def test_authenticated_notification_notice_if_no_notification(client, user):
    """Authenticated users have a different bell icon if no unread notification"""

    read = NotificationFactory(recipient=user, title="Read notification")
    read.mark_as_read()
    read.save()

    client.force_login(user)
    login_url = reverse("login")

    res = client.get(login_url, follow=True)
    assert "Voir la page des notifications" in res.content.decode()
    assert "at-notification-icon-no-unread" in res.content.decode()


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


def test_notification_detail_view_marks_it_as_read(client, user):
    notification = NotificationFactory(recipient=user, title="New notification")

    client.force_login(user)
    url = reverse("notification_detail_view", kwargs={"pk": notification.id})
    res = client.get(url)

    assert res.status_code == 200
    notification.refresh_from_db()

    assert notification.date_read is not None


def test_notification_detail_can_only_show_own_notifications(client, user):
    """Trying to see someone else's notification will return a 404"""
    other_user = UserFactory(email="other.user@example.org")
    notification = NotificationFactory(
        recipient=other_user, title="Forbidden notification"
    )

    client.force_login(user)
    url = reverse("notification_detail_view", kwargs={"pk": notification.id})
    res = client.get(url)

    assert res.status_code == 404
    notification.refresh_from_db()

    assert notification.date_read is None


def test_notification_can_be_deleted(client, user):
    notification = NotificationFactory(recipient=user, title="New notification")

    client.force_login(user)
    url = reverse("notification_delete_view", kwargs={"pk": notification.id})
    res = client.post(url)

    assert res.status_code == 302

    assert Notification.objects.count() == 0


def test_other_users_notifications_cannot_be_deleted(client, user):
    """Trying to delete someone else's notification will return a 404"""
    other_user = UserFactory(email="other.user@example.org")
    notification = NotificationFactory(
        recipient=other_user, title="Forbidden notification"
    )

    client.force_login(user)
    url = reverse("notification_delete_view", kwargs={"pk": notification.id})
    res = client.post(url)

    assert res.status_code == 404
    assert Notification.objects.count() == 1


def test_notifications_can_all_be_marked_as_read(client, user):
    """All the users notifications can be marked as read, and this doesn't
    affect already read notificiations or another user's notifications"""

    read = NotificationFactory(recipient=user, title="Read notification")
    NotificationFactory(recipient=user, title="Unread notification")
    NotificationFactory(recipient=user, title="Another unread notification")

    read.mark_as_read()
    read.save()

    other_user = UserFactory(email="other.user@example.org")
    NotificationFactory(recipient=other_user, title="Unaffected notification")

    client.force_login(user)
    url = reverse("notification_mark_all_read_view")
    res = client.get(url)

    assert res.status_code == 302

    assert (
        Notification.objects.filter(recipient=user, date_read__isnull=True).count() == 0
    )
    assert Notification.objects.filter(date_read__isnull=True).count() == 1


def test_notifications_can_all_be_deleted(client, user):
    """All the users notifications can be deleted, and this doesn't
    another user's notifications"""

    read = NotificationFactory(recipient=user, title="Read notification")
    NotificationFactory(recipient=user, title="Unread notification")
    NotificationFactory(recipient=user, title="Another unread notification")

    read.mark_as_read()
    read.save()

    other_user = UserFactory(email="other.user@example.org")
    NotificationFactory(recipient=other_user, title="Unaffected notification")

    client.force_login(user)
    url = reverse("notification_delete_all_view")
    res = client.post(url)

    assert res.status_code == 302

    assert Notification.objects.filter(recipient=user).count() == 0
    assert Notification.objects.all().count() == 1


def test_notification_parameters_can_be_updated(client, user):

    client.force_login(user)

    assert user.notification_email_frequency == "daily"

    params_url = reverse(
        "notification_settings_view",
    )

    res = client.post(
        params_url,
        {"notification_email_frequency": "weekly"},
    )

    assert res.status_code == 302

    user.refresh_from_db()
    assert user.notification_email_frequency == "weekly"
