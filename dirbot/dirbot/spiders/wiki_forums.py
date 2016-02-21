from wiki_wiki import WikiSpider


class WikiForumsSpider(WikiSpider):
    name = "wiki_forums"
    start_urls = [
        'https://en.wikipedia.org/wiki/List_of_Internet_forums'
    ]
    category = 'forums'
    links_xpath = "//div[@id='mw-content-text']/ul/li/a[starts-with(@href, '/wiki')]/@href"
