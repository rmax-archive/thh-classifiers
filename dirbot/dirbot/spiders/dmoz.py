from urlparse import urljoin
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
import logging
from dirbot.items import Website


class DmozSpider(Spider):
    name = "dmoz"
    # allowed_domains = ["dmoz.org"]
    follow_site_url = 0
    start_urls = [
        "http://www.dmoz.org/Computers/",
        "http://www.dmoz.org/Arts/",
        "http://www.dmoz.org/Business/",
        "http://www.dmoz.org/Games/",
        "http://www.dmoz.org/Health/",
        "http://www.dmoz.org/Home/",
        "http://www.dmoz.org/Recreation/",
        "http://www.dmoz.org/Science/",
        "http://www.dmoz.org/Sports/",
        "http://www.dmoz.org/Society/",
        "http://www.dmoz.org/Regional/",
        "http://www.dmoz.org/News/",
        "http://www.dmoz.org/Reference/",
        "http://www.dmoz.org/Shopping/",
        # "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        # "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/",
    ]

    def parse(self, response):
        sel = Selector(response)
        category = response.xpath('//ul[@class="navigate"]/li[@class="last"]/strong/text()').extract()[0]
        category1 = response.xpath('//ul[@class="navigate"]/li[2]/a/text()').extract()
        categories = response.xpath('//ul[@class="navigate"]/li//text()').extract()
        if not category1:
            category1 = response.xpath('//ul[@class="navigate"]/li[2]/strong/text()').extract()
        if category1:
            category1 = category1[0]
        else:
            category1 = None
        logging.debug(category)
        logging.debug(category1)
        dirs = sel.xpath('//ul[@class="directory dir-col"]/li/a/@href')
        for dir_entry in dirs:
            # logging.debug(dir_entry)
            dir_url = dir_entry.extract()
            if dir_url:
                dir_url = urljoin(response.url, dir_url)
                # logging.debug(dir_url)
                yield Request(url=dir_url,
                              callback=self.parse)

        sites = sel.xpath('//ul[@class="directory-url"]/li')
        for site in sites:
            item = Website()
            item["dmoz_page"] = response.url
            url = site.xpath('a/@href').extract()
            if url:
                item['category'] = category
                item['categories'] = categories
                item["category1"] = category1
                item['url'] = url[0]
                item['name'] = site.xpath('a/text()').extract()[0]
                item['description'] = site.xpath('text()').re('-\s[^\n]*\\r')[0]
                if self.follow_site_url:
                    yield Request(url=item['url'],
                                  callback=self.parse_site_head,
                                  meta={"item":item})
                else:
                    yield item

    def parse_site_head(self, response):
        item = response.meta["item"]
        item["html_code"] = response.body
        text_list = response.xpath('//*/text()').extract()
        item["page_text"] = " ".join(text_list)
        yield item