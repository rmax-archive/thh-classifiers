from one_page import OnePage


class OneClassifiedPage2(OnePage):
    name = "one_classified2"
    start_urls = [
        'http://free-classifieds-website-list.blogspot.ru/p/blog-page_7.html',
    ]
    category = 'classified'
    links_xpath = "//div[starts-with(@id,'post-body')]/div/a/@href"
