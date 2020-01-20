import smtplib

from django.core.mail.backends.smtp import EmailBackend
from django.core.mail.message import sanitize_address
from django.conf import settings


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
