"""Aid rendering helpers."""

from urllib.parse import quote

from django import template
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.conf import settings

from aids.models import Aid
from aids.constants import AID_TYPE_CHOICES, TYPES_ALL


register = template.Library()


@register.simple_tag
def choices_display(obj, field):
    """Correct rendering of `ChoiceArrayField` values.."""

    choices = obj._meta.get_field(field).base_field.choices
    choices_dict = dict(choices)

    # set to empty list if None
    keys = getattr(obj, field) or []

    values = [force_str(choices_dict.get(key, '')) for key in keys]
    return ', '.join(filter(None, values))


@register.simple_tag
def grouped_choices_display(obj, field):
    """Correct rendering of grouped `ChoiceArrayField` values.."""

    choices = obj._meta.get_field(field).base_field.choices
    flat_values = []
    for group, values in choices:
        flat_values += values
    choices_dict = dict(flat_values)

    keys = set(getattr(obj, field))

    values = [force_str(choices_dict[key]) for key in keys]
    return ', '.join(values)


@register.simple_tag
def form_choices_display(obj, field):
    """Correct rendering of `MultipleChoiceField` values.."""

    choices_dict = dict()

    if field == 'targeted_audiences':
        choices_dict = dict(Aid.AUDIENCES)
    elif field in ['aid_type', 'aid_types']:
        choices_dict = dict(AID_TYPE_CHOICES)
    elif field in ['financial_aids', 'technical_aids']:
        choices_dict = dict(TYPES_ALL)
    elif field in ['mobilization_step', 'mobilization_steps']:
        choices_dict = dict(Aid.STEPS)
    elif field == 'destinations':
        choices_dict = dict(Aid.DESTINATIONS)
    # recurrence ? ChoiceField

    # set to empty list if None
    keys = obj.get(field, [])

    values = [force_str(choices_dict.get(key, '')) for key in keys]
    return ', '.join(filter(None, values))


@register.simple_tag(takes_context=True)
def sortable_header(context, name, field):
    """Generates a sortable table header."""
    # Extract url and sort parameters from request
    current_url = context['request'].path
    get_params = context['request'].GET.copy()
    order_value = context['ordering']
    order_field = order_value.lstrip('-')
    icon = ''

    if field != order_field:
        new_order = field
    else:
        if order_value.startswith('-'):
            new_order = field
            icon = mark_safe('<span class="fas fa-chevron-up"></span>')
        else:
            new_order = '-%s' % field
            icon = mark_safe('<span class="fas fa-chevron-down"></span>')

    get_params['order'] = new_order

    # Pagination needs to be removed if the order must be changed
    if 'page' in get_params:
        get_params.pop('page')

    return format_html(
        '<a href="{}?{}">{} {}</a>',
        current_url,
        get_params.urlencode(),
        name,
        icon
    )


@register.simple_tag
def stats_url(aid):
    aid_url = '{}{}'.format(
        'https://aides-territoires.beta.gouv.fr',
        aid.get_absolute_url())

    matomo_url = 'https://stats.data.gouv.fr/index.php?module=Overlay&period=month&date=today&idSite={}#?l={}'.format(  # noqa
        settings.ANALYTICS_SITEID,
        quote(aid_url, safe='').replace('%', '$'),
    )
    return matomo_url


@register.simple_tag
def get(dict_object, key, default=None):
    return dict_object.get(key, default)
