from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from core.celery import app
from alerts.models import Alert


TEMPLATE = 'emails/alert_validate.txt'
SUBJECT = _('Please confirm your Aides-territoires alert')


@app.task
def send_alert_confirmation_email(user_email, alert_token):
    """Send an alert confirmation link to the user.

    The email contains a token that can be used to validate the login.
    """
    try:
        alert = Alert.objects.get(token=alert_token)
    except (Alert.DoesNotExist):
        # In case we could not find any valid user with the given email
        # we don't raise any exception, because we can't give any hints
        # about whether or not any particular email has an account
        # on our site.
        return

    site = Site.objects.get_current()
    scheme = 'https'
    base_url = '{scheme}://{domain}'.format(
        scheme=scheme,
        domain=site.domain)
    alert_validation_link = reverse('alert_validate_view', args=[alert_token])

    if alert.alert_frequency == Alert.FREQUENCIES.daily:
        frequency = _('You will receive a daily email whenever new matching aids will be published.')  # noqa
    else:
        frequency = _('You will receive a weekly email whenever new matching aids will be published.')  # noqa

    email_body = render_to_string(TEMPLATE, {
        'base_url': base_url,
        'alert': alert,
        'frequency': frequency,
        'alert_validation_link': '{}{}'.format(base_url, alert_validation_link)
    })
    send_mail(
        SUBJECT,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False)
