from django.db import models
from django.utils import timezone

from notifications.constants import NOTIFICATION_TYPES_LIST


class Notification(models.Model):
    """A notification that a user receives upon the completion of certain actions"""

    recipient = models.ForeignKey(
        "accounts.User",
        verbose_name="destinataire",
        on_delete=models.CASCADE,
    )
    notification_type = models.CharField(
        "type de notification",
        max_length=32,
        choices=NOTIFICATION_TYPES_LIST,
        default="internal_user",
        help_text="Utilisé pour la gestion des préférences de réception des notifications",
    )
    title = models.CharField("titre", max_length=100)
    message = models.CharField("message", max_length=500)
    date_created = models.DateTimeField("date de création", default=timezone.now)
    date_read = models.DateTimeField("date de consultation", null=True, blank=True)

    def mark_as_read(self):
        self.date_read = timezone.now()
        self.save()

    def truncate_title(self):
        if len(self.title) <= 50:
            return self.title
        else:
            return self.title[:49] + "…"

    def __str__(self):
        notification_type = self.get_notification_type_display()
        user = self.recipient.full_name
        return f"{notification_type} – {user} – {self.truncate_title()}"

    class Meta:
        verbose_name = "notification"
        ordering = ["date_created"]
