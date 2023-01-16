import pytest

from notifications.models import Notification


pytestmark = pytest.mark.django_db


def test_user_send_notification_creates_a_notification(user):
    user.send_notification(
        title="Sent notification",
        message="Sample content",
    )

    user.refresh_from_db()

    notifications = Notification.objects.filter(recipient=user)

    assert notifications.count() == 1
    assert notifications.first().title == "Sent notification"
