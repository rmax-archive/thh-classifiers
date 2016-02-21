from wiki_wiki import WikiSpider


class WikiBlogsSpider(WikiSpider):
    name = "wiki_blogs"
    start_urls = [
        'https://en.wikipedia.org/wiki/List_of_blogs'
    ]
    category = 'blogs'
