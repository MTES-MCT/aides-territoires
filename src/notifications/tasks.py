from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone

from accounts.models import User
from core.celery import app
from emails.utils import send_email
from notifications.models import Notification


def send_single_unread_notification_email(user_email: str) -> None:
    """Send an email stating the number of unread notifications."""
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        # In case we could not find any valid user with the given email
        # we don't raise any exception, because we can't give any hints
        # about whether or not any particular email has an account
        # on our site.
        return

    body_template = "emails/unread_notifications.txt"
    subject = "Vous avez des notifications non lues"

    unread_notifications = Notification.objects.filter(
        recipient=user,
        date_read__isnull=True,
        date_email__isnull=True,
    )
    if not unread_notifications.count():
        return

    email_body = render_to_string(
        body_template,
        {
            "unread_notifications_count": unread_notifications.count(),
            "user_name": user.full_name,
        },
    )
    send_email(
        subject=subject,
        body=email_body,
        recipient_list=[user.email],
        from_email=settings.DEFAULT_FROM_EMAIL,
        tags=["connexion", settings.ENV_NAME],
        fail_silently=False,
    )

    unread_notifications.update(date_email=timezone.now())


@app.task
def send_all_unread_notification_emails(frequency: str = "daily") -> None:
    """
    Send notification reminders to all suitable users
    """
    recipients = set(
        Notification.objects.filter(
            recipient__notification_email_frequency=frequency,
            date_read__isnull=True,
            date_email__isnull=True,
        ).values_list("recipient__email", flat=True)
    )

    for recipient in recipients:
        send_single_unread_notification_email(recipient)
