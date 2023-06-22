from django.conf import settings

from anymail.message import AnymailMessage


def send_email(
    subject,
    body,
    recipient_list,
    from_email=settings.DEFAULT_FROM_EMAIL,
    reply_to=None,
    html_body=None,
    tags=None,
    fail_silently=False,
):
    message = AnymailMessage(subject=subject, body=body, to=recipient_list)

    message.from_email = from_email

    if reply_to:
        message.reply_to = reply_to

    if html_body:
        message.attach_alternative(html_body, "text/html")

    # Tags can then be found and filtered in the ESP's analytics dashboard
    if tags:
        message.tags = tags

    message.send(fail_silently=fail_silently)


def send_email_with_template(
    recipient_list, template_id, data=None, tags=None, fail_silently=False
):
    """Use the "template" feature provided by our ESP"""
    message = AnymailMessage(to=recipient_list)
    message.template_id = template_id
    message.from_email = None  # use the template's default sender

    # Tags can then be found and filtered in the ESP's analytics dashboard
    if tags:
        message.tags = tags

    # Provide data for template replacements
    if data:
        # Currently working with Brevo
        message.merge_global_data = data

    message.send(fail_silently=fail_silently)
