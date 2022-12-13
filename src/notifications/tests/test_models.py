import pytest
from notifications.constants import NOTIFICATION_TYPES_LIST

from notifications.factories import NotificationFactory

pytestmark = pytest.mark.django_db


def test_notification_can_be_marked_as_read():
    read = NotificationFactory(title="Read notification")
    read.mark_as_read()
    read.save()

    assert read.date_read is not None


def test_notification_title_can_be_shortened(user):
    notification_type = NOTIFICATION_TYPES_LIST[0]
    title_50 = "50 letters-long title 1234567890123456789012345678"
    title_51 = "51 letters-long title 12345678901234567890123456789"

    notif_50 = NotificationFactory(title=title_50)
    notif_51 = NotificationFactory(
        title=title_51, notification_type=notification_type[0], recipient=user
    )

    title_51_shortened = "51 letters-long title 123456789012345678901234567…"
    assert notif_50.truncate_title() == title_50
    assert notif_51.truncate_title() == title_51_shortened

    assert (
        str(notif_51)
        == f"{notification_type[1]} – {user.full_name} – {title_51_shortened}"
    )
