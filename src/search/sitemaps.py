from django.contrib.sitemaps import Sitemap

from search.models import SearchPage


class SearchSitemap(Sitemap):
    def items(self):
        """Return the list of all live aids."""

        return SearchPage.objects.all()

    def get_urls(self, page=1, site=None, protocol=None):
        """Return the list of url dicts.

        We need to return absolute urls, so we cannot just implement
        `location`.
        """
        pages = self.items()
        urls = []
        domain = site.domain if site else "aides-territoires.beta.gouv.fr"

        for page in pages:
            url = {
                "item": page,
                "location": f"https://{page.slug}.{domain}",
                "lastmod": page.date_updated,
                "changefreq": None,
                "priority": None,
            }
            urls.append(url)

        return urls
