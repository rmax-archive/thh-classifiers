from dirbot.spiders import PagesCollectionSpider


class AlexaNewsSpider(PagesCollectionSpider):
    name = "alexa_news"
    start_urls = [
        'http://www.alexa.com/topsites/category/Top/News',
    ]
    category = 'news'
    pages = True
