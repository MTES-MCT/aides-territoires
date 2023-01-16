from django.db import models
from django.utils import timezone


class Notification(models.Model):
    """A notification that a user receives upon the completion of certain actions"""

    recipient = models.ForeignKey(
        "accounts.User",
        verbose_name="destinataire",
        on_delete=models.CASCADE,
    )
    title = models.CharField("titre", max_length=100)
    message = models.CharField("message", max_length=500)
    date_created = models.DateTimeField("date de création", default=timezone.now)
    date_read = models.DateTimeField("date de consultation", null=True, blank=True)
    date_email = models.DateTimeField(
        "date d’envoi de la notification par courriel", null=True, blank=True
    )

    def mark_as_read(self):
        self.date_read = timezone.now()
        self.save()

    def truncate_title(self):
        if len(self.title) <= 50:
            return self.title
        else:
            return self.title[:49] + "…"

    def __str__(self):
        user = self.recipient.full_name
        return f"{user} – {self.truncate_title()}"

    class Meta:
        verbose_name = "notification"
        ordering = ["date_created"]
