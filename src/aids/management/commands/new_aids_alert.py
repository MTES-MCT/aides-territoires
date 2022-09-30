from datetime import timedelta
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.conf import settings
from django.core.mail import send_mail

from aids.models import Aid


class Command(BaseCommand):
    """Send an email alert upon new aid creations."""

    def handle(self, *args, **options):
        now = timezone.now()
        yesterday = now - timedelta(days=1)
        new_aids = (
            Aid.objects.filter(date_created__gte=yesterday)
            .order_by("author")
            .select_related("author")
        )

        nb_aids = new_aids.count()
        if nb_aids == 0:
            self.stdout.write("We could not find any new aids.")
            return

        site = Site.objects.get_current()
        email_body = render_to_string(
            "emails/new_aids_alert_body.txt",
            {
                "new_aids": new_aids,
                "domain": site.domain,
            },
        )
        email_subject = "{} nouvelles aides au {:%d/%m/%Y}".format(nb_aids, now)
        email_from = settings.DEFAULT_FROM_EMAIL
        email_to = [settings.CONTACT_EMAIL]

        send_mail(email_subject, email_body, email_from, email_to, fail_silently=False)
