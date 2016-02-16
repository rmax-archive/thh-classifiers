from urlparse import urljoin
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
import logging
import os
import urlparse

from dirbot.items import PageTypeItem


class TypeScreenshotsSpider(Spider):
    name = "typescr"
    imgstorage = "/media/sf_temp/scr"
    img_count = 0
    handle_httpstatus_list = [400, 404, 401, 403, 301, 302, 500, 520]

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
        url = "https://www.ulmart.ru"
        req = Request(url,
                meta={'splash': {
                        'args': {"wait":10,
                                 # "render_all":1
                        },
                        'endpoint': "render.html",
                        'timeout': 1000},
                      'source_url': url,
                      'extract_objects': False,
                      'extract_list': True,
                },   callback=self.parse_main)
        yield req
        # for pagetype, urllst in self.start_urls.items():
        #     for url in urllst:
        #         req = Request(url,
        #         meta={'splash': {
        #                 'args': {"wait":3, "render_all":1},
        #                 'endpoint': "render.png",
        #                 'timeout': 1000},
        #               'source_url': url,
        #               'pagetype': pagetype
        #         },   callback=self.parse)
        #         yield req

    def parse(self, response):
        if response.status != 200:
            logging.error(response.body)
        else:
            item = PageTypeItem()
            item['pagetype'] = response.meta['pagetype']
            item['url'] = response.meta['source_url']
            url = item['url']
            pic = response.body
            self.img_count += 1
            img_num = self.img_count
            img_file_name = "{}_{}.png".format(item['pagetype'], img_num)
            logging.debug("img file name {}".format(img_file_name))
            item["img_path"] = self.store_img(img_file_name, pic)
            yield item

    def store_img(self, file_name, file_content):
        full_path = os.path.join(self.imgstorage, file_name)
        with open(full_path, "w") as fout:
            fout.write(file_content)
        return full_path

    def create_render_request(self, url,
                              pagetype):
        req = Request(url,
                      meta={'splash': {
                          'args': {"wait": 10,
                                   # "scale_method":"vector",
                                   # "width": 1900,
                                   # "height": 1080,
                                   "render_all":1
                          },
                          'endpoint': "render.png",
                          'timeout': 1000},
                            'source_url': url,
                            'pagetype': pagetype,
                      }, callback=self.parse)
        return req

    def parse_main(self, response):
        if response.status != 200:
            logging.error(response.body)
        else:
            sel = Selector(response)
            if response.meta['extract_objects']:
                pass
                # obj_urls = sel.xpath('//div/div[contains(@class, "b-product__title")]/span/a[contains(@class, "js-gtm-product-click")]/@href').extract()
                # for obj_url in obj_urls:
                #     url = urlparse.urljoin(response.meta["source_url"], obj_url)
                #     logging.debug(url)
                #     req = self.create_render_request(url,
                #                                      pagetype="object")
                #     yield req
                #     break
            if response.meta['extract_list']:
                catalog_urls = sel.xpath('//li[contains(@class, "b-list__item")]/a[contains(@class, "js-gtm-click-menu") and contains(@href, "catalog")]/@href').extract()
                for cat_url in catalog_urls:
                    url = urlparse.urljoin(response.meta["source_url"], cat_url)
                    logging.debug(url)
                    req = self.create_render_request(url,
                                                     pagetype="list")
                    yield req
                    # req = Request(url,
                    # meta={'splash': {
                    #         'args': {"wait":3,
                    #                  # "render_all":1
                    #         },
                    #         'endpoint': "render.html",
                    #         'timeout': 1000},
                    #       'source_url': url,
                    #       'extract_objects': True,
                    #       'extract_list': False,
                    # },   callback=self.parse_main)
                    # yield req


