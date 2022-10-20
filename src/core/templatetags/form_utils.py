"""Form template helpers."""

from django import template
from django.forms import CheckboxInput

register = template.Library()


@register.filter
def is_checkbox(field):
    """ "Is the given field a checkbox input?."""

    return isinstance(field.field.widget, CheckboxInput)
