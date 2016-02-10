from scrapy.item import Item, Field


class Website(Item):
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
    url = Field()
    html_code = Field()
    page_text = Field()
    img_path = Field()
