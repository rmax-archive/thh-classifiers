from scrapy.selector import Selector


def get_basic_information(sel):
    def get_xpath(title):
        return '//span[text()="%s"]/../../ul//text()' % title

    print(sel.xpath(get_xpath('Education')).extract())
    print(sel.xpath(get_xpath('Current City and Hometown')).extract())
    print(sel.xpath(get_xpath('Gender')).extract())
    print(sel.xpath(get_xpath('Relationship Status')).extract())
    print(sel.xpath(get_xpath('Anniversary')).extract())


htmlpath = "/media/sf_temp/{}.html"
page_ids = ["100001665518840", "100000118429707"]

for page_id in page_ids:
    print("------------------------")
    print(page_id)
    with open(htmlpath.format(page_id), "r") as fin:
        fb_sel = Selector(text=fin.read())
    get_basic_information(fb_sel)


