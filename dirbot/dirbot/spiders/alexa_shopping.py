from dirbot.spiders import PagesCollectionSpider


class AlexaShopSpider(PagesCollectionSpider):
    name = "alexa_shop"
    start_urls = [
        'http://www.alexa.com/topsites/category/Top/Shopping',
    ]
    category = 'shopping'
    pages = True