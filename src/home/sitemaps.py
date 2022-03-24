from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class HomeSitemap(Sitemap):
    """Index pages with hard-coded urls (homepage, etc.)."""

    def items(self):
        return ['home', 'legal_mentions', 'privacy_policy', 'accessibility']

    def location(self, item):
        return reverse(item)
