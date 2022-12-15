import pytest

from notifications.models import Notification


pytestmark = pytest.mark.django_db


def test_user_check_notification_allowed(user):
    """The method should only return true if notifications are allowed
    for the specific parameter requested"""

    user.notification_aid_team = "none"
    user.notification_aid_user = "internal_only"
    user.notification_internal_team = "internal_email"
    user.save()

    assert user.check_notification_allowed("aid_team") is False
    assert user.check_notification_allowed("aid_user") is True
    assert user.check_notification_allowed("internal_team") is True


def test_user_send_notification_creates_a_notification_if_type_allowed(user):
    user.notification_aid_team = "none"
    user.notification_aid_user = "internal_only"
    user.save()

    user.send_notification(
        notification_type="aid_team",
        title="Unsent notification",
        message="Sample content",
    )
    user.send_notification(
        notification_type="aid_user",
        title="Sent notification",
        message="Sample content",
    )

    user.refresh_from_db()

    notifications = Notification.objects.filter(recipient=user)

    assert notifications.count() == 1
    assert notifications.first().title == "Sent notification"
