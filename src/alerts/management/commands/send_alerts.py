"""This is the "send email alerts upon new saved search results" feature."""

from datetime import timedelta
import logging

from sentry_sdk import capture_exception

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.db.models import Q, Case, When
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from core.utils import is_subdomain, build_host_with_subdomain
from alerts.models import Alert
from stats.utils import log_event
from emails.utils import send_email

from aids.forms import AidSearchForm
from django.http import QueryDict
from search.utils import clean_search_form

logger = logging.getLogger(__name__)
User = get_user_model()


class Command(BaseCommand):
    """Send an email alert upon new aid results."""

    def handle(self, *args, **options):

        alerts = self.get_alerts()
        alerted_alerts = []
        for alert in alerts:
            new_aids = list(alert.get_new_aids())
            if new_aids:
                alerted_alerts.append(alert.token)
                self.send_alert(alert, new_aids)
                logger.info('Sending alert alert email to {}: {} alerts'.format(
                    alert.email,
                    len(new_aids)))

        updated = Alert.objects \
            .filter(token__in=alerted_alerts) \
            .update(latest_alert_date=timezone.now())
        self.stdout.write('{} alerts sent'.format(updated))
        log_event('alert', 'sent', source='send_alerts', value=updated)
        return

    def get_alerts(self):
        """Get alerts that could request a new email.

        Only return alerts with a latest alert date old enough to send
        a new one.
        """

        # Get the two date thresholds (daily and weekly alerts)
        now = timezone.now()
        yesterday = now - timedelta(days=1)
        last_week = now - timedelta(days=7)

        # Create the alert date query condition
        F = Alert.FREQUENCIES
        latest_alert_is_old_enough = Q(latest_alert_date__lte=Case(
            When(alert_frequency=F.daily, then=yesterday),
            When(alert_frequency=F.weekly, then=last_week)
        ))

        alerts = Alert.objects \
            .filter(validated=True) \
            .filter(
                Q(latest_alert_date__isnull=True) |
                latest_alert_is_old_enough)

        return alerts

    def send_alert(self, alert, new_aids):
        """Send an email alert with a summary of the newly published aids."""

        site = Site.objects.get_current()
        domain = site.domain
        domain_with_subdomain = build_host_with_subdomain(site.domain, alert.source)
        in_minisite = is_subdomain(alert.source)

        querydict = QueryDict(alert.querystring)
        search_form = AidSearchForm(querydict)
        if search_form.is_valid():
            current_search_dict = clean_search_form(
                search_form.cleaned_data, remove_extra_fields=True)

        # alert_url is different if on a minisite or not
        alert_url = alert.get_absolute_url(in_minisite=in_minisite)
        # delete_url always redirects to the main site
        delete_url = reverse('alert_delete_view', args=[alert.token])

        email_context = {
            'domain_with_subdomain': domain_with_subdomain,
            'current_search_dict': current_search_dict,
            'nb_aids': len(new_aids),
            'new_aids': new_aids[:3],
            'alert_title': alert.title,
            'alert_url': f'https://{domain_with_subdomain}{alert_url}',
            'alert_email_feedback_form_url': settings.ALERT_EMAIL_FEEDBACK_FORM_URL,
            'alert_delete_url': f'https://{domain}{delete_url}',
        }

        text_body = render_to_string('alerts/alert_body.txt', email_context)
        html_body = render_to_string('alerts/alert_body.html', email_context)

        email_subject_prefix = settings.EMAIL_SUBJECT_PREFIX
        if alert.title == settings.ADDNA_ALERT_TITLE:
            email_subject_prefix = settings.ADDNA_ALERT_EMAIL_SUBJECT_PREFIX
        email_subject = '{}{:%d/%m/%Y} — De nouvelles aides correspondent à vos recherches'.format(
            email_subject_prefix,
            timezone.now())

        email_from = settings.DEFAULT_FROM_EMAIL
        email_to = [alert.email]
        try:
            send_email(
                subject=email_subject,
                body=text_body,
                recipient_list=email_to,
                from_email=email_from,
                html_body=html_body,
                tags=['alerte', alert.source, settings.ENV_NAME],
                fail_silently=False)
        except Exception as e:
            capture_exception(e)
