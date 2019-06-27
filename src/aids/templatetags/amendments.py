"""Amendment UI helpers."""

import difflib

from django import template
from django.utils.safestring import mark_safe
from django.utils.html import format_html


register = template.Library()


@register.simple_tag
def field_diff(aid, amendment, field):
    try:
        v1 = getattr(aid, field).splitlines()
        v2 = getattr(amendment, field).splitlines()
        diff = list(difflib.ndiff(v1, v2))
    except:
        diff = []

    html_diff = [make_html_diff_line(line) for line in diff]
    return mark_safe('\n'.join(html_diff))


def make_html_diff_line(line):
    if not line:
        return None

    prefix = line[0]
    content = line[2:]
    diff_class = {
        '+': 'add',
        '-': 'rm',
        '?': 'info',
        ' ': 'common',
    }.get(prefix)
    html = format_html(
        '<pre class="diff-line {}"><span class="prefix">{} </span>{}</pre>',
        diff_class, prefix, content)
    return html
