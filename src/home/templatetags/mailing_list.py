"""Template helpers to render mailing list providers custom forms."""

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def mailing_list_url():
    """ "returns the url of the sendinblue mailing list registration form."""

    return settings.MAILING_LIST_URL
