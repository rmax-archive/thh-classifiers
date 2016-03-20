# Scrapy settings for dirbot project

SPIDER_MODULES = ['dirbot.spiders']
NEWSPIDER_MODULE = 'dirbot.spiders'
DEFAULT_ITEM_CLASS = 'dirbot.items.Website'

ITEM_PIPELINES = {
    'dirbot.pipelines.PageHtmlMiddleware': 1
}

DOWNLOADER_MIDDLEWARES = {
     'scrapyjs.SplashMiddleware': 725,
    'dirbot.splashmware.CustomSplashMiddleware': 700,
}

EXTENSIONS = {
    'scrapy.extensions.throttle.AutoThrottle': None,
}

SPLASH_URL = 'http://localhost:8050/'
SPLASH_USER = ''
SPLASH_PASS = ''

FB_TOKEN = "ae4bfa92ab0c89e8a078ba04c5fe4cd8"
FB_CLIENT_ID = "465686606933602"
FB_CLIENT_SECRET = "4db6181216f67a9ec566ed6339e2425f"



