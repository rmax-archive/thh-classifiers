# Scrapy settings for dirbot project

SPIDER_MODULES = ['dirbot.spiders']
NEWSPIDER_MODULE = 'dirbot.spiders'
DEFAULT_ITEM_CLASS = 'dirbot.items.Website'

ITEM_PIPELINES = {
    'dirbot.pipelines.PageHtmlMiddleware': 1
}

DOWNLOADER_MIDDLEWARES = {
    'dirbot.middleware.DelayedRequestsMiddleware': 100,
    'scrapyjs.SplashMiddleware': 725,
    'dirbot.splashmware.CustomSplashMiddleware': 700,
}

EXTENSIONS = {
    'scrapy.extensions.throttle.AutoThrottle': None,
}

SPLASH_URL = 'http://localhost:8050/'
SPLASH_USER = ''
SPLASH_PASS = ''

FB_TOKEN = "CAAGnihzIbmIBABfzHEP6OuZBO5h01ZAszJTn8KoJ3XBDO6EKQbsKnzeCzZB2Ew4rm1rDMmZCjdjN54AZAd4kgXVhHBcbATjZAZAVmMBSDIgIH3uFnqH6S9SyLXid6WxAZB1GdV3KLG7PKuOkXf6R5Y2oVVCLRnMa4qkrtSw1AdZB7qwqC36SPA92jzflSI26ntwUZD"
FB_CLIENT_ID = "465686606933602"
FB_CLIENT_SECRET = "4db6181216f67a9ec566ed6339e2425f"



