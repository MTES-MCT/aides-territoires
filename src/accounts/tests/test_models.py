import pytest
from backers.factories import BackerFactory

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


def test_user_toggle_excluded_backer(user):
    backer_1 = BackerFactory(name="Backer 1")
    backer_2 = BackerFactory(name="Backer 2")
    backer_3 = BackerFactory(name="Backer 3")

    user.toggle_excluded_backer(backer=backer_1, is_excluded=True)
    user.toggle_excluded_backer(backer=backer_2, is_excluded=True)

    user.refresh_from_db()

    assert user.excluded_backers.count() == 2

    user.toggle_excluded_backer(backer=backer_2, is_excluded=False)
    user.toggle_excluded_backer(backer=backer_3, is_excluded=False)

    user.refresh_from_db()

    assert user.excluded_backers.count() == 1
