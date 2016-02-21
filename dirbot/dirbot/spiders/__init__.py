# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from urlparse import urlparse, urljoin
from dirbot.items import WebsiteItem


class PagesCollectionSpider(Spider):
    allowed_domains = ["www.alexa.com"]
    pages = False
    start_urls = []
    category = ''
    links_xpath = "//ul/li[@class='site-listing']/div/p/a/@href"

    def pagenate(self, response):
        nexturls = response.xpath("//div[@class='alexa-pagination']/a[@class='pagination-page']/@href").extract()
        for url in nexturls:
            nextpage = urljoin(response.url, url)
            self.log(nextpage)
            yield Request(nextpage, callback=self.parse, meta={'domain': ''})

    def parse(self, response):
        links = response.xpath(self.links_xpath).extract()
        domain = urlparse(response.url).netloc
        # u = urlparse(response.url)._replace(path=links[0]).geturl()
        for link in links:
            url = urljoin(response.url, link)
            yield Request(url, callback=self.parsepage, meta={'domain': domain})
        if self.pages:
            for req in self.pagenate(response):
                yield req

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
