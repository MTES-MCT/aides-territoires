from anymail.message import AnymailMessage

from django.conf import settings


def filter_recipients(recipient_list):
    """
    Filter the recipients through a whitelist.
    """
    if not settings.ENABLE_EMAIL_WHITELIST:
        return recipient_list
    filtered_recipient = [
        addr for addr in recipient_list
        if addr in settings.EMAIL_WHITELIST
    ]
    print(filtered_recipient)
    print(settings.EMAIL_WHITELIST)
    return filtered_recipient


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
