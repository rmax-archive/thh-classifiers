import json
import pkgutil
import scrapy
import logging
from scrapy.contrib.linkextractors import LinkExtractor

from dirbot.items import PageTypeItem


class FullPageSpider(scrapy.Spider):
    name = 'fullpage'
    follow_all = False
    follow = []
    skip = []
    max_depth = 4

    def start_requests(self):
        urls_data = json.loads(pkgutil.get_data("dirbot", "resources/full_urls.json"))
        for url_data in urls_data:
            url = url_data["url"]
            yield scrapy.Request(url, meta={'fullpage_depth': 0,
                                 "pagetype": url_data["pagetype"],
                                 "siteurl": url})

    def parse(self, response):
        str_fix = lambda x : x.decode('utf-8', errors="ignore").strip()
        pagetype = response.meta["pagetype"]
        siteurl = response.meta["siteurl"]
        logging.debug("{} @ {}".format(pagetype, response.url))
        item = PageTypeItem()
        item['pageurl'] = response.url
        item['siteurl'] = siteurl
        item['pagetype'] = pagetype
        item['html_code'] = str_fix(response.body)
        yield item

        depth = 0
        if self.max_depth > 0:
            depth = response.meta.get('fullpage_depth', 0)
            if depth > self.max_depth:
                return

        deny = self.skip
        if self.follow_all:
            allow = None
        elif not self.follow:
            return
        else:
            allow = self.follow

        links = LinkExtractor(allow=allow, deny=deny).extract_links(response)
        for link in links:
            yield scrapy.Request(link.url, meta={'fullpage_depth': depth + 1,
                                                 "pagetype": pagetype,
                                                 "siteurl": siteurl})