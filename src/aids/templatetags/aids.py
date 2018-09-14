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


@register.simple_tag
def grouped_choices_display(obj, field):
    """Correct rendering of `ChoiceArrayField` values.."""

    choices = obj._meta.get_field(field).base_field.choices
    flat_values = []
    for group, values in choices:
        flat_values += values
    choices_dict = dict(flat_values)

    keys = set(getattr(obj, field))
    values = [force_text(choices_dict[key]) for key in keys]
    return ', '.join(values)
