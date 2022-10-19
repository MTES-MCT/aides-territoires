from django import template
from django.utils.safestring import mark_safe
from django.conf import settings

register = template.Library()


@register.simple_tag
def setting(setting_name):
    """Pulls a value from settings."""

    return getattr(settings, setting_name)


@register.simple_tag
def staging_warning():
    warning_div = ""

    if settings.ENV_NAME == "staging":
        warning_div = """
        <div class="header-warning fr-centered fr-background-alt-pink">
            <div class="container">
                <p class="fr-py-1w">Attention, vous êtes en recette, pas en production !</p>
            </div>
        </div>
        """

    return mark_safe(warning_div)


@register.filter
def phone(raw_phone):
    """Convert a E.164 format french number to a pretty display."""

    phone = raw_phone.replace("+33", "0")
    phone = "{} {} {} {} {}".format(
        phone[0:2], phone[2:4], phone[4:6], phone[6:8], phone[8:10]
    )
    return phone
