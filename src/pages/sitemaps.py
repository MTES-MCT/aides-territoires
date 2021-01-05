from django.contrib.sitemaps import Sitemap

from pages.models import Page


class PageSitemap(Sitemap):
    def items(self):
        """Return the list of all live aids."""

        return Page.objects.all()
