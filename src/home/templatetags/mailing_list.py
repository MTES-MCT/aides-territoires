"""Template helpers to render mailing list providers custom forms."""

from django import template
from django.utils.html import format_html
from django.urls import reverse
from django.conf import settings

register = template.Library()


@register.simple_tag
def mailing_list_form_action():
    """"returns the value of the `action` field for the ml form."""

    return settings.MAILING_LIST_FORM_ACTION


@register.simple_tag(takes_context=True)
def mailing_list_hidden_fields(context):
    """Returns custom hidden fields required to make the ml form work."""

    request = context['request']
    redirection_url = reverse('mailing_list_registration')
    absolute_redirection_url = request.build_absolute_uri(redirection_url)

    return format_html(
        '''
        <input type="hidden" name="listid" id="listid" value="{listid}">
        <input type="hidden" name="from_url" id="from_url" value="yes">
        <input type="hidden" name="hdn_email_txt" id="hdn_email_txt" value="">
        <input type="hidden" name="sib_simple" value="simple">
        <input type="hidden" name="sib_forward_url" value="{redirection_url}">
        ''',
        listid=settings.MAILING_LIST_LIST_ID,
        redirection_url=absolute_redirection_url)
