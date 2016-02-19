# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from urlparse import urlparse, urljoin
from dirbot.items import WebsiteItem


class AlexaSpider(Spider):
    name = "alexa"
    allowed_domains = ["www.alexa.com"]
    start_urls = []
    category = ''

    def parse(self, response):
        links = response.xpath("//ul/li[@class='site-listing']/div/p/a/@href").extract()
        domain = urlparse(response.url).netloc
        # u = urlparse(response.url)._replace(path=links[0]).geturl()
        for link in links:
            url = urljoin(response.url, link)
            yield Request(url, callback=self.parsepage, meta={'domain': domain})
        curpn = int(response.xpath("//div[@class='alexa-pagination']/span[@class='pagination-current']/text()").extract()[0])
        nextvals = response.xpath("//div[@class='alexa-pagination']/a[@class='pagination-page']/text()").re('\d+')
        nexturls = response.xpath("//div[@class='alexa-pagination']/a[@class='pagination-page']/@href").extract()
        for i, nv in enumerate(nextvals):
            if int(nv) > curpn:
                nextpage = urljoin(response.url, nexturls[i])
                print nextpage
                yield Request(nextpage, callback=self.parse, meta={'domain': domain})
                break


    def parsepage(self, response):
        siteurl = response.xpath("//li/span[@class='compare-site']/a[@class='offsite_overview']/@href").extract()
        if siteurl:
            item = WebsiteItem()
            item['url'] = urljoin(response.url, siteurl[0])
            item['category'] = self.category
            name = response.xpath("//li/span[@class='compare-site']/a[@class='offsite_overview']/text()").extract()
            if name:
                item['name'] = name[0]
            yield item
