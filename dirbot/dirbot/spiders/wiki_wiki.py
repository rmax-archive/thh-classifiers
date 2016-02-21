from dirbot.spiders import PagesCollectionSpider
from dirbot.items import WebsiteItem


class WikiSpider(PagesCollectionSpider):
    name = "wiki_wiki"
    allowed_domains = ["wikipedia.org"]
    start_urls = [
        'https://en.wikipedia.org/wiki/List_of_online_encyclopedias',
        'https://en.wikipedia.org/wiki/List_of_wikis',
    ]
    category = 'wiki'
    pages = False
    links_xpath = "//table[contains(@class,'wikitable')]/tr/td[1]/a/@href"

    def parsepage(self, response):
        siteurls = response.xpath("//table[contains(@class, 'infobox')]//td//a[@rel='nofollow']/@href").extract()
        print siteurls
        if siteurls:
            for siteurl in siteurls:
                item = WebsiteItem()
                item['url'] = siteurl
                item['category'] = self.category
                name = response.xpath("//h1[@id='firstHeading']/text()").extract()
                if name:
                    item['name'] = name[0]
                yield item
