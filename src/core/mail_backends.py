import json
import requests
import smtplib

from django.core.mail.backends.smtp import EmailBackend
from django.core.mail.message import sanitize_address
from django.conf import settings


API_HEADERS = {
    'accept': 'application/json',
    'content-type': 'application/json',
    'api-key': settings.SIB_API_KEY,
}


def send_mail_sib(subject, email_body, to_email, from_email=settings.DEFAULT_FROM_EMAIL, email_body_type='text', tag_list=None):  # noqa
    """
    Sends emails using the Sendinblue Transactional API.
    """
    endpoint = settings.SIB_TRANSACTIONAL_API_ENDPOINT
    post_data = {
        'sender': {'email': from_email},
        'to': [{'email': to_email}],
        'subject': subject,
    }
    if email_body_type == 'html':
        post_data['htmlContent'] = email_body
    else:
        post_data['textContent'] = email_body
    if tag_list:
        post_data['tags'] = tag_list
    requests.post(endpoint, headers=API_HEADERS, data=json.dumps(post_data))


class StagingEmailBackend(EmailBackend):
    """Custom email backend for staging purpose.

    This backend uses smtp to send email to whitelisted addresses.
    All other emails are just discarded.
    """

    def _send(self, email_message):
        """Sends the message.

        This is a copy of the original `_send` method with only a difference:
        we filter the recipient list and only keep the whitelisted ones.
        """

        encoding = email_message.encoding or settings.DEFAULT_CHARSET
        from_email = sanitize_address(email_message.from_email, encoding)
        message = email_message.message()

        # Here is the bit where we filter the recipients
        # This is very sensitive code, so treat carefully!
        recipients = [
            sanitize_address(addr, encoding)
            for addr in email_message.recipients()
            if addr in settings.EMAIL_WHITELIST]
        if not recipients:
            return False

        try:
            self.connection.sendmail(
                from_email, recipients, message.as_bytes(linesep='\r\n'))
        except smtplib.SMTPException:
            if not self.fail_silently:
                raise
            return False
        return True
