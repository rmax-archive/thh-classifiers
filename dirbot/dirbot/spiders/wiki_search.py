from wiki_wiki import WikiSpider


class WikiBlogsSpider(WikiSpider):
    name = "wiki_search"
    start_urls = [
        'https://en.wikipedia.org/wiki/List_of_search_engines'
    ]
    category = 'search_engines'
