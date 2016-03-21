# -*- coding: utf-8 -*-
import json
from datetime import datetime
import logging

from scrapy import Spider
from scrapy import FormRequest
from scrapy import Item, Field
from scrapy.http import Request

import dirbot.settings as settings

API_ENDPOINT = "https://graph.facebook.com/v2.5/"
API_TOKEN_ENDPOINT = "https://graph.facebook.com/v2.5/oauth/access_token"

_FB_SEARCH_FIELDS = [
    'id', 'name',
]


class FbSearchItem(Item):
    id = Field()
    name = Field()
    keywords = Field()


class FbGraphSearchSpider(Spider):
    name = "fb_search"
    query = "Egorov"
    # query delay in seconds
    next_page_delay = 10

    def get_request(self, query=None,
                    obj_type="user",
                    callback=None,
                    meta={}):
        formdata = {
            'type': obj_type,
            'access_token': settings.FB_TOKEN,
            'q': query,
            'fields': ",".join(_FB_SEARCH_FIELDS),
        }
        return FormRequest(
            API_ENDPOINT + "search",
            method="GET",
            formdata=dict((k, v) for k, v in formdata.iteritems() if v),
            callback=callback if callback else self.parse,
            meta=meta
        )

    def start_requests(self):
        if self.query:
            self.log("Querying for %s" % self.query, logging.INFO)
            yield self.get_request(query=self.query,
                                   meta={"keywords": self.query})

    def parse(self, response):
        if response.status != 200:
            self.log(
                'Response %s has a non-200 status with body: %s'
                % (str(response), response.body),
                level=logging.WARNING
            )
            return
        data = json.loads(response.body)
        kw = response.meta.get("keywords", "")
        # self.log(data,
        #         level=logging.INFO
        # )
        for search_res in data['data']:
            item = FbSearchItem()
            item["id"] = search_res["id"]
            item["name"] = search_res["name"]
            item["keywords"] = kw
            yield item

        if 'paging' in data and 'next' in data['paging']:
            yield Request(data['paging']['next'],
                          dont_filter=True,
                          meta={"keywords": kw,
                                'delay_request': self.next_page_delay,
                          })


class FbLongLiveTokenSpider(Spider):
    name = "fb_token"

    def get_request(self):
        formdata = {
            'grant_type': "fb_exchange_token",
            'fb_exchange_token': settings.FB_TOKEN,
            'client_id': settings.FB_CLIENT_ID,
            'client_secret': settings.FB_CLIENT_SECRET,
        }
        return FormRequest(
            API_TOKEN_ENDPOINT,
            method="GET",
            formdata=dict((k, v) for k, v in formdata.iteritems() if v),
            callback=self.parse
        )

    def start_requests(self):
        yield self.get_request()

    def parse(self, response):
        if response.status != 200:
            self.log(
                'Response %s has a non-200 status with body: %s'
                % (str(response), response.body),
                level=logging.WARNING
            )
            return
        self.log(response.body,
                level=logging.INFO
        )

