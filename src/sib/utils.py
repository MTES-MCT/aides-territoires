from django.conf import settings


def filter_recipients(recipient_list):
    """
    Filter the recipients through a whitelist.
    """
    if not settings.ENABLE_EMAIL_WHITELIST:
        return recipient_list
    filtered_recipient_list = [
        addr for addr in recipient_list
        if addr in settings.EMAIL_WHITELIST
    ]
    print(filtered_recipient)
    print(settings.EMAIL_WHITELIST)
    return filtered_recipient
