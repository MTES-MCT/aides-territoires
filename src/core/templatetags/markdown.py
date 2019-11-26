from django import template
from django.template.defaultfilters import stringfilter
from markdown import markdown

register = template.Library()


@register.filter(name='markdown', is_safe=True)
@stringfilter
def markdown_filter(content):
    return markdown(content, extensions=['markdown.extensions.fenced_code'])
