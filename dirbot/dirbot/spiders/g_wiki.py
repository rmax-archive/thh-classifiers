import logging
from urlparse import urljoin
from scrapy import Request, Spider

from dirbot.items import WebsiteItem


class WikiGoogleSpider(Spider):
    name = "ggl_wiki"
    start_urls = [
        'https://www.google.ru/search?q={}',
    ]
    keywords = ['wiki']
    category = "wiki"

    def start_requests(self):
        for url in self.start_urls:
            for kw in self.keywords:
                yield Request(url.format(kw), callback=self.parse)

    def parse(self, response):
        # next_page_url = response.xpath('//td[contains(@class,"navend")]/a/@href').extract()
        next_page_urls = response.xpath("//td/a[contains(@href, 'search')]/@href").extract()
        if next_page_urls:
            logging.debug(next_page_urls)
            next_page_url = next_page_urls[-1]
            yield Request(urljoin(response.url, next_page_url), callback=self.parse)

        urls = response.xpath('//div[@class="g"]//h3/a/@href').extract()
        logging.debug(urls)
        for url in urls:
            item = WebsiteItem()
            item['url'] = url.replace("/url?q=", "")
            item['category'] = self.category
            yield item


class BlogGoogleSpider(WikiGoogleSpider):
    name = "ggl_blogs"
    keywords = ['blog']
    category = "blogs"
