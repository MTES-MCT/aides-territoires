from django.utils import timezone
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.conf import settings

from aids.models import Aid


class Command(BaseCommand):
    """Send an email alert when aids are waiting for review."""

    def handle(self, *args, **options):
        reviewable_aids = (
            Aid.objects.under_review().order_by("author").select_related("author")
        )

        nb_aids = reviewable_aids.count()
        if nb_aids == 0:
            self.stdout.write("We could not find any reviewable aids.")
            return

        site = Site.objects.get_current()
        email_body = render_to_string(
            "emails/reviewable_aids_alert_body.txt",
            {"reviewable_aids": reviewable_aids, "domain": site.domain},
        )
        today = timezone.now()
        email_subject = "{} aides en revue au {:%d/%m/%Y}".format(nb_aids, today)
        email_from = settings.DEFAULT_FROM_EMAIL
        email_to = [settings.CONTACT_EMAIL]

        send_mail(email_subject, email_body, email_from, email_to, fail_silently=False)
