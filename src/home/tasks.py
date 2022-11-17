from django.template.loader import render_to_string
from django.conf import settings

from core.celery import app
from home.forms import ContactForm
from emails.utils import send_email


CONTACT_SUBJECT_PREFIX = "[Contact] "


@app.task
def send_contact_form_email(form_dict, body_template="emails/contact_form.txt"):  # noqa
    """Send the contact form content to the AT team."""

    subject_display = dict(ContactForm.SUBJECT_CHOICES).get(
        form_dict["subject"]
    )  # noqa
    contact_form_email_body = render_to_string(
        body_template, {"form_dict": form_dict, "subject_display": subject_display}
    )
    send_email(
        subject=CONTACT_SUBJECT_PREFIX + subject_display,
        body=contact_form_email_body,
        recipient_list=[settings.DEFAULT_FROM_EMAIL],
        from_email=settings.DEFAULT_FROM_EMAIL,
        reply_to=[form_dict["email"]],
        tags=["contact", form_dict["subject"], settings.ENV_NAME],
        fail_silently=False,
    )
