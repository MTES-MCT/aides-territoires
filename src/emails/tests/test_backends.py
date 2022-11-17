import pytest

from django.core.mail import send_mail


@pytest.fixture(autouse=True)
def override_email_backend(settings):
    """Override the email backend for all the tests in this file."""

    settings.EMAIL_BACKEND = "emails.backends.LocmemWhitelistEmailBackend"
    settings.EMAIL_WHITELIST = ["allowed1@example.org", "allowed2@example.org"]


def test_whitelisted_emails_are_sent(settings, mailoutbox):
    send_mail("Test", "Test", "from@example.org", ["allowed1@example.org"])
    assert len(mailoutbox) == 1


def test_non_whitelisted_emails_are_rejected(settings, mailoutbox):
    send_mail("Test", "Test", "from@example.org", ["disallowed1@example.org"])
    assert len(mailoutbox) == 0


def test_partial_whitelist_emails_are_rejected(settings, mailoutbox):
    send_mail(
        "Test",
        "Test",
        "from@example.org",
        ["allowed1@example.org", "disallowed1@example.org"],
    )
    assert len(mailoutbox) == 0


def test_emails_with_many_whitelisted_contacts_are_sent(settings, mailoutbox):
    send_mail(
        "Test",
        "Test",
        "from@example.org",
        ["allowed1@example.org", "allowed2@example.org"],
    )
    assert len(mailoutbox) == 1
