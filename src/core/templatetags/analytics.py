from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def analytics_enabled():
    """"True if analytics in enabled in settings."""

    return settings.ANALYTICS_ENABLED


@register.simple_tag
def analytics_siteid():

    return settings.ANALYTICS_SITEID


@register.simple_tag
def analytics_setup():
    """"Embed the js tracking code setup."""

    site_id = settings.ANALYTICS_SITEID
    tag = '''
    <script type="text/javascript">
      var _paq = _paq || [];
      _paq.push(["setDomains", ["*.aides-territoires.beta.gouv.fr"]]);
      _paq.push(['trackPageView']);
      _paq.push(['enableLinkTracking']);
      _paq.push(['setTrackerUrl', '//stats.data.gouv.fr/piwik.php']);
      _paq.push(['setSiteId', '{siteid}']);
    </script>
    '''.format(siteid=site_id)
    return mark_safe(tag)
