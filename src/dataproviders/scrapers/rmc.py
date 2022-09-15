import scrapy
from dataproviders.utils import content_prettify


class RMCSpider(scrapy.Spider):
    name = "rmc"

    BASE_URL = "https://www.eaurmc.fr/"
    start_urls = [
        "https://www.eaurmc.fr/jcms/gbr_5503/fr/les-aides-financieres-primes-et-appels-a-projets?cids=cbl_43675&PortalAction_ppi_6464_start=0&PortalAction_ppi_6464_pageSize=12&PortalAction_ppi_6464_pagerAll=true&PortalAction_ppi_6464_sort=&PortalAction_ppi_6464_reverse=false",  # noqa
    ]

    def parse(self, response):
        links = response.css('li.weaurmc-redevance a::attr("href")').getall()
        for link in links:
            absolute_url = self.BASE_URL + link
            yield scrapy.Request(absolute_url, callback=self.aid_parse)

    def aid_parse(self, response):
        title = response.css("h1.weaurmc-publication-title::text").get()
        description = response.xpath('//meta[@name="description"]/@content').get()

        current_url = response.request.url
        unique_id = current_url.split("/")[-3]

        yield {
            "title": title,
            "description": content_prettify(description, base_url=self.BASE_URL),
            "current_url": current_url,
            "uniqueid": unique_id,
        }
