from dirbot.items import WebsiteItem
from scrapy import Spider


class OnePage(Spider):
    link_xpath = ''
    category = ''
    links_xpath = ''

    def parse(self, response):
        links = response.xpath(self.links_xpath).extract()
        for link in links:
            if link and len(link) > 3:
                item = WebsiteItem()
                item['url'] = link
                item['category'] = self.category
                yield item
