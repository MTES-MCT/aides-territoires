from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class DataSitemap(Sitemap):
    """Add the "Données et API" page to the sitemap."""

    def items(self):
        return ["data_doc"]

    def location(self, item):
        return reverse(item)
