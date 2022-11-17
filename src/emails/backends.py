from anymail.backends.sendinblue import EmailBackend as AnymailEmailBackend
from django.core.mail.backends.locmem import EmailBackend as LocmemEmailBackend

from django.conf import settings


def is_whitelisted(message):
    """Returns true if the message's recipients are all whitelisted."""

    recipients = set(message.to)
    whitelist = set(settings.EMAIL_WHITELIST)

    # We only send the message if ALL adresses in the recipient list are
    # in the whitelist
    return recipients.issubset(whitelist)


class EmailBackend(AnymailEmailBackend):
    """The default email backend to use in prod."""

    pass


class WhitelistMixin:
    """Mixin with the whitelist checking behavior."""

    def send_messages(self, messages):
        filtered_messages = filter(is_whitelisted, messages)
        return super().send_messages(filtered_messages)


class WhitelistEmailBackend(WhitelistMixin, AnymailEmailBackend):
    """Custom email backend that filters sent messages.

    All messages to addresses that are not in the whitelist are discarded.

    For testing / staging purpose.
    """

    pass


class LocmemWhitelistEmailBackend(WhitelistMixin, LocmemEmailBackend):
    """Dummy email backend with whitelist behavior.

    During testing, django automatically replaces the email backend with
    a dummy `Locmem` email backend.

    This class has a single purpose: testing the `WhitelistEmailBackend`
    behavior without risking to send real emails.
    """

    pass
