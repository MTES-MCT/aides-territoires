from django.conf import settings
from django.contrib.sites.models import Site
from django.core import management
from django.core.mail import mail_admins
from django.template.loader import render_to_string

from core.celery import app
from django.apps import apps
from emails.utils import send_email_with_template


@app.task
def log_admins(subject, body, url):
    """Send a log email to admins."""

    scheme = "https"
    site = Site.objects.get_current()
    base_url = "{}://{}".format(scheme, site.domain)
    log_template = "emails/log_admins.txt"
    email_body = render_to_string(
        log_template, {"base_url": base_url, "log_message": body, "url": url}
    )
    mail_admins(subject, email_body, fail_silently=False)


@app.task
def send_publication_email(aid_id):
    """
    Sends an email when an aid gets published.
    """
    if not settings.SIB_PUBLICATION_EMAIL_ENABLED:
        return

    Aid = apps.get_model("aids.Aid")
    aid = Aid.objects.get(pk=aid_id)
    author = aid.author
    site = Site.objects.get_current()
    base_url = "https://{}".format(site.domain)
    data = {
        "PRENOM": author.first_name,
        "NOM": author.last_name,
        "AIDE_NOM": aid.name,
        "AIDE_URL": aid.get_absolute_url(),
        "BASE_URL": base_url,
    }
    send_email_with_template(
        recipient_list=[author.email],
        template_id=settings.SIB_PUBLICATION_EMAIL_TEMPLATE_ID,
        data=data,
        tags=["publication", settings.ENV_NAME],
        fail_silently=True,
    )


@app.task
def dump_all_aids_as_json():
    """Dumps all aids as json file."""
    management.call_command("dump_all_aids_as_json", verbosity=1)
