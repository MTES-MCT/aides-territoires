from operator import attrgetter
from itertools import groupby
from datetime import timedelta
import logging

from django.utils import timezone
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.db.models import Q
from django.urls import reverse
from django.conf import settings

from bookmarks.models import Bookmark


# XXX Issue We need to add a `date_published`


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Send an email alert upon new aid results."""

    def handle(self, *args, **options):

        alert_threshold = timezone.now() - timedelta(days=60)
        owner_bookmarks = self.get_bookmarks(alert_threshold)

        for owner, bookmarks in owner_bookmarks:
            new_aids = self.get_new_aids(bookmarks, alert_threshold)
            if new_aids:
                self.send_alert(owner, new_aids)
                logger.info('Sending bookmark alert email to {} ({}) : {} '
                            'bookmarks'.format(
                                owner.full_name,
                                owner.email,
                                len(new_aids)
                            ))
        return

    def get_bookmarks(self, threshold):
        """Returns bookmark with a latest alert date older than `threshold`."""

        bookmarks = Bookmark.objects \
            .filter(
                Q(latest_alert_date__isnull=True) |
                Q(latest_alert_date__lte=threshold)) \
            .order_by('owner')
        get_by_owner = attrgetter('owner')
        grouped_bookmarks = groupby(bookmarks, key=get_by_owner)

        return grouped_bookmarks

    def get_new_aids(self, bookmarks, threshold):
        """Get newly published aids for every bookmark.

        returns a list of tuples of this format:
            (bookmark, number of new aids, list of new aids)
        """

        owner_new_aids = []
        for bookmark in bookmarks:
            new_aids = list(bookmark.get_aids(published_after=threshold))
            nb_new_aids = len(new_aids)
            if nb_new_aids > 0:
                owner_new_aids.append(
                    (bookmark, nb_new_aids, new_aids[:3])
                )
        return owner_new_aids

    def send_alert(self, owner, new_aids):
        """Send an email alert with a summary of the newly published aids."""

        site = Site.objects.get_current()
        email_context = {
            'domain': site.domain,
            'owner': owner,
            'new_aids': new_aids,
            'bookmarks_url': reverse('bookmark_list_view'),
        }

        text_body = render_to_string(
            'bookmarks/new_bookmark_alerts.txt', email_context)
        html_body = render_to_string(
            'bookmarks/new_bookmark_alerts.html', email_context)
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