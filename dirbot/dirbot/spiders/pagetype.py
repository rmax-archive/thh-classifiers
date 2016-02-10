from urlparse import urljoin
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
import logging
import os

from dirbot.items import PageTypeItem


class TypeScreenshotsSpider(Spider):
    name = "typescr"
    imgstorage = "/media/sf_temp"

    start_urls = {
        "list": [
            "http://www.ulmart.ru/catalog/93938?sort=5&viewType=1&rec=true",
            "http://www.ulmart.ru/catalog/93939?sort=5&viewType=1&rec=true",
            "http://mxp.ulmart.ru/catalog/mxp?sort=5&viewType=1&rec=true",
            "http://www.ulmart.ru/catalog/brand_computers?sort=5&viewType=1&rec=true",
            "http://www.ulmart.ru/catalog/monobloks_pc?sort=5&viewType=1&rec=true"
        ],
        "object": [
            "https://www.ulmart.ru/goods/1008645",
            "https://www.ulmart.ru/goods/1005293",
            "https://www.ulmart.ru/goods/3413914",
            "https://www.ulmart.ru/goods/3715191",
            "https://www.ulmart.ru/goods/3740036",
            "https://www.ulmart.ru/goods/3684996"
        ]
    }

    def start_requests(self):
        for pagetype, urllst in self.start_urls.items():
            for url in urllst:
                req = Request(url,
                meta={'splash': {
                        'args': {"wait":3, "render_all":1},
                        'endpoint': "render.png",
                        'timeout': 1000},
                      'source_url': url,
                      'pagetype': pagetype
                },   callback=self.parse)
                yield req

    def parse(self, response):
        if response.status != 200:
            logging.error(response.body)
        else:
            item = PageTypeItem()
            item['pagetype'] = response.meta['pagetype']
            item['url'] = response.meta['source_url']
            url = item['url']
            pic = response.body
            img_file_name = "{}.png".format(url.replace("/", "_").replace(":", "").replace("?", ""))
            logging.debug(img_file_name)
            item["img_path"] = self.store_img(img_file_name, pic)
            yield item

    def store_img(self, file_name, file_content):
        full_path = os.path.join(self.imgstorage, file_name)
        with open(full_path, "w") as fout:
            fout.write(file_content)
        return full_path