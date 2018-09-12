# flake8: noqa

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def analytics_tag():
    """"Embed the js tracking code, if it's enabled."""

    if not settings.ANALYTICS_ENABLED:
        return ''

    site_id = settings.ANALYTICS_SITEID
    tag = '''
    <script type="text/javascript">
      var _paq = _paq || [];
      _paq.push(["setDomains", ["*.aides-territoires.beta.gouv.fr"]]);
      _paq.push(['trackPageView']);
      _paq.push(['enableLinkTracking']);
      (function() {
        var u="//stats.data.gouv.fr/";
        _paq.push(['setTrackerUrl', u+'piwik.php']);
        _paq.push(['setSiteId', '{siteid}']);
        var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
        g.type='text/javascript'; g.async=true; g.defer=true; g.src=u+'piwik.js'; s.parentNode.insertBefore(g,s);
      })();
    </script>
    <noscript><p><img src="//stats.data.gouv.fr/piwik.php?idsite={siteid}" style="border:0;" alt="" /></p></noscript>
    '''.format(site_id)
    return tag
