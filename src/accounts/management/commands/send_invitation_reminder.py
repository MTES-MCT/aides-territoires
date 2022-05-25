"""This is the "send invitation reminder email" feature."""

from datetime import timedelta
import logging

from sentry_sdk import capture_exception

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from core.utils import get_base_url
from accounts.models import User
from stats.utils import log_event
from emails.utils import send_email


logger = logging.getLogger(__name__)
User = get_user_model()


class Command(BaseCommand):
    """Send an email as invitation reminder."""

    def handle(self, *args, **options):

        invited_users = self.get_invited_users()
        reminded = []
        for invited_user in invited_users:
            self.send_invitation(invited_user)
            logger.info('Sending invitation reminder email to {}'.format(invited_user.email))
            reminded.append(invited_user.pk)

        updated = User.objects \
            .filter(pk__in=reminded) \
            .update(invitation_date=timezone.now())
        self.stdout.write('{} invitations reminder sent'.format(updated))
        log_event('invitation reminder', 'sent', source='send_invitations', value=updated)
        return

    def get_invited_users(self):
        """
        Get invitated users with pending invitation that could request a new email.
        Only return invitations with an invitation date old enough to send
        a new one.
        """

        now = timezone.now()
        last_week = now - timedelta(days=7)

        invited_users = User.objects \
            .filter(proposed_organization__isnull=False) \
            .filter(invitation_date__lte=last_week)

        return invited_users

    def send_invitation(self, invited_user):
        """Send an invitation reminder email."""
        
        base_url = get_base_url()
        reverse_url = reverse("join_organization")
        full_login_url = f"{base_url}{reverse_url}"

        email_context = {
            'user_name' : invited_user.full_name,
            'invitation_author' : invited_user.invitation_author.full_name,
            'organization_name' : invited_user.proposed_organization.name,
            'full_login_url' : full_login_url,
        }

        text_body = render_to_string('emails/invitation_reminder_body.txt', email_context)

        email_subject_prefix = settings.EMAIL_SUBJECT_PREFIX
        email_subject = '{} — Une invitation à rejoindre une organisation est en attente'.format(
            email_subject_prefix,
            timezone.now())

        email_from = settings.DEFAULT_FROM_EMAIL
        email_to = [invited_user.email]
        try:
            send_email(
                subject=email_subject,
                body=text_body,
                recipient_list=email_to,
                from_email=email_from,
                tags=['rappel invitation', settings.ENV_NAME],
                fail_silently=False)
        except Exception as e:
            capture_exception(e)
