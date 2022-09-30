from django.contrib.sitemaps import Sitemap

from aids.models import Aid


class AidSitemap(Sitemap):
    def items(self):
        """Return the list of all live aids."""

        return Aid.objects.live().order_by("-date_published")

    def lastmod(self, item):
        return item.date_updated
