from django import template
from django.conf import settings

from analytics.utils import get_goal


register = template.Library()


@register.simple_tag
def analytics_enabled():
    """ "True if analytics in enabled in settings."""

    return settings.ANALYTICS_ENABLED


@register.simple_tag
def analytics_siteid():

    return settings.ANALYTICS_SITEID


@register.simple_tag(takes_context=True)
def analytics_goalid(context):
    """Returns the value of the goal to track."""

    request = context["request"]
    goalid = get_goal(request.session)
    return goalid


@register.simple_tag
def hotjar_siteid():
    return settings.HOTJAR_SITEID
