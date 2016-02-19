from alexa import AlexaSpider


class AlexaShopSpider(AlexaSpider):
    name = "alexa_shop"
    start_urls = [
        'http://www.alexa.com/topsites/category/Top/Shopping',
    ]
    category = 'news'
