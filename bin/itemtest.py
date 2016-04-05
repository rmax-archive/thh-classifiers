from scrapy import Item, Field


class FbSearchItem(Item):
    id = Field()
    name = Field()
    url = Field()
    keywords = Field()
    userinfo = Field()
    friends = Field()


d = {"id": 123}
item = FbSearchItem()
item.update(d)
print item