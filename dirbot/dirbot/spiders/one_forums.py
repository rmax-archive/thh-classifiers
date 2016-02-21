from one_page import OnePage


class OneForumsPage(OnePage):
    name = "one_forums"
    start_urls = [
        'http://www.bloggersideas.com/do-follow-high-pr-forums-list',
    ]
    category = 'forums'
    links_xpath = "//div[@id='content']//table//tr/td/a[not(@class)]/@href"
