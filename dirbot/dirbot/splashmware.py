from w3lib.http import basic_auth_header
from scrapy.exceptions import NotConfigured
from scrapyjs import SplashMiddleware
from scrapy.http import Request
from scrapy import log
import traceback


class CustomSplashMiddleware(SplashMiddleware):

    @classmethod
    def from_crawler(cls, crawler):
        obj = super(CustomSplashMiddleware, cls).from_crawler(crawler)
        settings = crawler.settings
        user = settings.get('SPLASH_USER')
        if not user:
            raise NotConfigured
        obj.auth_header = basic_auth_header(user,
                settings.get('SPLASH_PASS', ''))
        return obj

    def process_request(self, request, spider):
        # log.msg(request.method, level=log.DEBUG)
        # log.msg(request.url, level=log.DEBUG)
        # log.msg(str(request.meta), level=log.DEBUG)
        result = super(CustomSplashMiddleware, self).process_request(request, spider)
        if isinstance(result, Request) and result != request \
                and 'Authorization' not in result.headers:
            result.headers['Authorization'] = self.auth_header
        return result