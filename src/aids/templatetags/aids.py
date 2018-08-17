"""Aid rendering helpers."""

from django import template
from django.utils.encoding import force_text

register = template.Library()


@register.simple_tag
def choices_display(obj, field):
    """Correct rendering of `ChoiceArrayField` values.."""

    choices = obj._meta.get_field(field).base_field.choices
    choices_dict = dict(choices)

    keys = getattr(obj, field)
    values = [force_text(choices_dict[key]) for key in keys]
    return ', '.join(values)
