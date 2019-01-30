from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def analytics_enabled():
    """"True if analytics in enabled in settings."""

    return settings.ANALYTICS_ENABLED


@register.simple_tag
def analytics_siteid():

    return settings.ANALYTICS_SITEID
