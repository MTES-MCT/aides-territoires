"""This is the "send email alerts upon new saved search results" feature."""

from datetime import timedelta
import logging

from django.utils import timezone
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.db.models import Q, Case, When
from django.urls import reverse
from django.conf import settings

from bookmarks.models import Bookmark


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Send an email alert upon new aid results."""

    def handle(self, *args, **options):

        bookmarks = self.get_bookmarks()
        alerted_bookmarks = []
        for bookmark in bookmarks:
            new_aids = list(bookmark.get_new_aids())
            if new_aids:
                alerted_bookmarks.append(bookmark.id)
                self.send_alert(bookmark, new_aids)
                logger.info('Sending bookmark alert email to {} ({}) : {} '
                            'bookmarks'.format(
                                bookmark.owner.full_name,
                                bookmark.owner.email,
                                len(new_aids)
                            ))

        Bookmark.objects \
            .filter(id__in=alerted_bookmarks) \
            .update(latest_alert_date=timezone.now())
        return

    def get_bookmarks(self):
        """Get bookmarks to send alerts.

        Only return bookmarks with a latest alert date old enough to send
        a new one.
        """

        # Get the two date thresholds (daily and weekly alerts)
        now = timezone.now()
        yesterday = now - timedelta(days=1)
        last_week = now - timedelta(days=7)

        # Create the alert date query condition
        F = Bookmark.FREQUENCIES
        latest_alert_is_old_enough = Q(latest_alert_date__lte=Case(
            When(alert_frequency=F.daily, then=yesterday),
            When(alert_frequency=F.weekly, then=last_week)
        ))

        bookmarks = Bookmark.objects \
            .select_related('owner') \
            .filter(send_email_alert=True) \
            .filter(
                Q(latest_alert_date__isnull=True) |
                latest_alert_is_old_enough) \
            .order_by('owner')

        return bookmarks

    def send_alert(self, bookmark, new_aids):
        """Send an email alert with a summary of the newly published aids."""

        owner = bookmark.owner
        site = Site.objects.get_current()
        email_context = {
            'domain': site.domain,
            'bookmark': bookmark,
            'owner': owner,
            'nb_aids': len(new_aids),
            'new_aids': new_aids[:3],
            'bookmarks_url': reverse('bookmark_list_view'),
        }

        text_body = render_to_string(
            'bookmarks/alert_body.txt', email_context)
        html_body = render_to_string(
            'bookmarks/alert_body.html', email_context)
        email_subject = 'De nouvelles aides correspondent à vos recherches'
        email_from = settings.DEFAULT_FROM_EMAIL
        email_to = [owner.email]

        send_mail(
            '{}{}'.format(settings.EMAIL_SUBJECT_PREFIX, email_subject),
            text_body,
            email_from,
            email_to,
            html_message=html_body,
            fail_silently=False)
