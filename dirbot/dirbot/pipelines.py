import scrapy
from twisted.internet.defer import inlineCallbacks, returnValue


class PageHtmlMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        cls.crawler = crawler
        return cls()

    @inlineCallbacks
    def process_item(self, item, spider):
        str_fix = lambda x : x.decode('utf-8', errors="ignore").strip()
        url = item.get("url", None)
        if url:
            try:
                page_request = scrapy.Request(url)
                page_response = yield self.crawler.engine.download(page_request,
                                                                    spider)
                item["html_code"] = str_fix(page_response.body)
            except Exception as exc:
                spider.log('Error while execution additional page request (%s): %s' %
                           (url, exc))
        returnValue(item)
