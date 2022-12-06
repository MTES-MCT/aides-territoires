from django.db import models
from django.utils import timezone


class Notification(models.Model):
    """A notification that a user receives upon the completion of certain actions"""

    recipient = models.ForeignKey(
        "accounts.User",
        verbose_name="destinataire",
        on_delete=models.CASCADE,
    )
    message = models.CharField("message", max_length=256)
    date_created = models.DateTimeField("date de création", default=timezone.now)
    date_read = models.DateTimeField("date de consultation", null=True, blank=True)

    def __str__(self):
        return f"({self.id}) à:{self.recipient.full_name} – {self.message}"

    def mark_as_read(self):
        self.date_read = timezone.now()
        self.save()

    class Meta:
        verbose_name = "notification"
        ordering = ["-date_created"]
