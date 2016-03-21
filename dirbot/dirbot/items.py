from scrapy.item import Item, Field


class WebsiteItem(Item):
    name = Field()
    category1 = Field()
    category = Field()
    categories = Field()
    description = Field()
    url = Field()
    dmoz_page = Field()
    html_code = Field()
    page_text = Field()


class PageTypeItem(Item):
    pagetype = Field()
    pageurl = Field()
    siteurl = Field()
    html_code = Field()
    img_path = Field()
