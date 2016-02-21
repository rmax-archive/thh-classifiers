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


