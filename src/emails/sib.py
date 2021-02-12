from anymail.message import AnymailMessage

from emails.utils import filter_recipients


def send_mail_sib(
        subject, message, from_email, recipient_list,
        fail_silently=False, auth_user=None, auth_password=None,
        connection=None, html_message=None):
    recipient_list = filter_recipients(recipient_list)
    message = AnymailMessage(
        subject=subject,
        body=message,
        from_email=from_email,
        to=recipient_list,
    )
    if html_message:
        message.attach_alternative(html_message, "text/html")
    message.send(fail_silently=fail_silently)


def send_mail_sib_with_template(
        recipient_list, template_id, data=None, tags=None,
        fail_silently=False):
    recipient_list = filter_recipients(recipient_list)
    message = AnymailMessage(to=recipient_list)
    message.template_id = template_id
    if tags:
        message.tags = tags
    message.from_email = None  # use the template's default sender
    if data:
        message.merge_global_data = data
    message.send(fail_silently=fail_silently)
