from anymail.message import AnymailMessage

from sib.utils import filter_recipients


def send_mail(
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
