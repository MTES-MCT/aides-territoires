from django import template
from django.utils.safestring import mark_safe
from django.conf import settings

register = template.Library()


@register.simple_tag
def setting(setting_name):
    """Pulls a value from settings."""

    return getattr(settings, setting_name)


@register.simple_tag
def staging_warning():
    warning_div = ''

    if settings.ENV_NAME == 'staging':
        warning_div = '''
        <div id="staging-warning">
            <div class="container">
                <p>Attention, vous êtes en recette, pas en production !</p>
            </div>
        </div>
        '''

    return mark_safe(warning_div)
