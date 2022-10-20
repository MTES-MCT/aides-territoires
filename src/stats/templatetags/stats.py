"""Stat rendering helpers."""

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def percent_display(part, whole, ndigits=2):
    """Percent rendering"""
    percent = 100 * float(part) / float(whole)
    round_percent = round(percent, ndigits)
    return mark_safe(f"{round_percent}&#8239;%")
