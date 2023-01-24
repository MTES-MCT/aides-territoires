from django.core.management.base import BaseCommand

from notifications.tasks import send_all_unread_notification_emails


class Command(BaseCommand):
    """
    Manually execute the send_all_unread_notification_emails periodic task
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "-f",
            "--frequency",
            type=str,
            choices=["daily", "weekly"],
            help="Define the frequencies",
        )

    def handle(self, *args, **kwargs):
        frequency = kwargs["frequency"]

        if frequency:
            send_all_unread_notification_emails(frequency)
        else:
            send_all_unread_notification_emails()
