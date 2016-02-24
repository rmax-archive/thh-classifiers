from one_page import OnePage


class OneBlogsPage(OnePage):
    name = "one_search"
    start_urls = [
        'http://www.thesearchenginelist.com/'
    ]
    category = 'search_engines'
    links_xpath = "//table[@class='search-list']/tr/td/a/@href"
