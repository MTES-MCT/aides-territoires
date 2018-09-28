from datetime import timedelta
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

from aids.models import Aid


class Command(BaseCommand):
    """Send an email alert upon new aid creations."""

    def handle(self, *args, **options):
        yesterday = timezone.now() - timedelta(days=1)
        new_aids = Aid.objects \
            .published() \
            .filter(date_created__gte=yesterday) \
            .order_by('author') \
            .select_related('author')

        if new_aids.count() == 0:
            self.stdout.write('We could not find any new aids.')
            return

        email_body = render_to_string('emails/new_aids_alert_body.txt', {
            'new_aids': new_aids
        })
        email_subject = 'Nouvelles aides au {:%d/%m/%Y}'.format(yesterday)
        email_from = settings.DEFAULT_FROM_EMAIL
        email_to = [settings.CONTACT_EMAIL]

        send_mail(
            email_subject,
            email_body,
            email_from,
            email_to,
            fail_silently=False)
