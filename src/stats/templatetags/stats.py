"""Stat rendering helpers."""

from django import template


register = template.Library()

@register.simple_tag
def percent_display(part, whole):
    """Percent rendering"""
    percent = 100 * float(part)/float(whole)
    round_percent = round(percent, 2)
    return str(round_percent) + "%"
