from alexa import AlexaSpider


class AlexaNewsSpider(AlexaSpider):
    name = "alexa_news"
    start_urls = [
        'http://www.alexa.com/topsites/category/Top/News',
    ]
    category = 'news'
