from anymail.message import AnymailMessage


def send_mail(
        subject, message, from_email, recipient_list,
        fail_silently=False, auth_user=None, auth_password=None,
        connection=None, html_message=None):
    message = AnymailMessage(
        subject=subject,
        body=message,
        from_email=from_email,
        to=recipient_list,
    )
    if html_message:
        message.attach_alternative(html_message, "text/html")
    message.send(fail_silently=fail_silently)
