from django.core.mail import mail_admins
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

from core.celery import app


@app.task
def log_admins(subject, body, url):
    """Send a log email to admins."""

    scheme = 'https'
    site = Site.objects.get_current()
    base_url = '{}://{}'.format(scheme, site.domain)
    log_template = 'emails/log_admins.txt'
    email_body = render_to_string(log_template, {
        'base_url': base_url,
        'log_message': body,
        'url': url})
    mail_admins(
        subject,
        email_body,
        fail_silently=False)
