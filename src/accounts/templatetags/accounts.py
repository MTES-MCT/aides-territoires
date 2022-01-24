"""Account rendering helpers."""

from django import template
from django.utils.encoding import force_str


register = template.Library()


@register.simple_tag
def choices_display(obj, field):
    """Choice field rendering"""

    choices = obj._meta.get_field(field).choices
    choices_dict = dict(choices)

    # set to empty list if None
    keys = getattr(obj, field) or []

    return choices_dict.get(keys)
