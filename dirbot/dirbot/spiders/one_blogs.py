from one_page import OnePage


class OneBlogsPage(OnePage):
    name = "one_blogs"
    start_urls = [
        'http://dailytekk.com/2013/11/18/the-100-best-most-interesting-blogs-and-websites-of-2014-2/?reading=continue',
        'http://dailytekk.com/2015/01/01/the-100-best-most-interesting-blogs-and-websites-of-2015/?reading=continue'
    ]
    category = 'blogs'
    links_xpath = "//ol/li/a[@target='_blank']/@href"
