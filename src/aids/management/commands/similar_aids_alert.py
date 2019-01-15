from datetime import timedelta
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.conf import settings

from accounts.models import User
from aids.models import Aid


class Command(BaseCommand):
    """Send email alerts to users when alerts are published.

    Detect when new aids are relevant to some user's interests, and notify
    them accordingly.
    """

    def handle(self, *args, **options):
        self.last_week = timezone.now() - timedelta(days=7)
        self.site = Site.objects.get_current()

        users = self.get_users()
        for user in users:
            relevent_new_aids = self.get_relevent_new_aids(user)
            if len(relevent_new_aids) > 0:
                self.send_alert(user, relevent_new_aids)

    def get_users(self):
        """Return users that wants to receive such alerts."""
        users = User.objects.filter(similar_aids_alert=True)
        return users

    def get_relevent_new_aids(self, user):
        """Find recent aids relevent to this user's interests."""
        tags = user.watched_tags
        aids = Aid.objects \
            .published() \
            .open() \
            .filter(date_created__gt=self.last_week) \
            .filter(tags__overlap=tags)
        return aids

    def send_alert(self, user, aids):
        email_body = render_to_string('emails/similar_aids_alert_body.txt', {
            'user': user,
            'aids': aids,
            'domain': self.site.domain,
        })
        email_subject = 'Ces aides peuvent vous intéresser'
        email_from = settings.DEFAULT_FROM_EMAIL
        email_to = [user.email]

        send_mail(
            email_subject,
            email_body,
            email_from,
            email_to,
            fail_silently=False)
