from one_page import OnePage


class OneClassifiedPage(OnePage):
    name = "one_classified"
    start_urls = [
        'http://bestclassifiedsiteinindia.elcraz.com/2014/04/300-free-classified-ad-list-2014.html',
    ]
    category = 'classified'
    links_xpath = "//div[@id='main']//table//tr/td/a/@href"
