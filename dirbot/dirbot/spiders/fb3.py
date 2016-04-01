# encoding: utf-8
from urlparse import urljoin
import pkgutil
import json
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
import logging
import os
import io
import urlparse


class FB3Spider(Spider):
    name = "fb3"
    imgstorage = "/media/sf_temp/"
    img_count = 0
    handle_httpstatus_list = [400, 404, 401, 403, 301, 302, 500, 520]
    splash_timeout = 1000
    facebook_ids = ["100001665518840", "100000118429707"]
    start_urls = []
    account = { 'email': "nikaskriabina@gmail.com",
                'password':  "F,hfrflf,hf2016"}

    def start_requests(self):
        script_text = pkgutil.get_data("dirbot", "resources/fblogin.lua")
        url = "https://www.facebook.com/login.php"
        req = Request(url,
                meta={
                    'splash': {
                    'args': {'lua_source': script_text},
                    'endpoint': 'execute',
                    'timeout': self.splash_timeout},
                }, callback=self.parse_main)
        yield req

    def store_img(self, file_name, file_content):
        full_path = os.path.join(self.imgstorage, file_name)
        with open(full_path, "w") as fout:
            fout.write(file_content)
        return full_path

    def save_response(self,page_name, page_body):
        _u = lambda t: t.decode('UTF-8', 'ignore') if isinstance(t, str) else t
        with io.open("/media/sf_temp/{}.html".format(page_name), "w", encoding="utf-8") as fout:
            fout.write(unicode(_u(page_body)))
            # fout.write(page_body.encode("utf8", errors="ignore"))

    def parse_main(self, response):
        if response.status != 200:
            logging.error(response.body)
        else:
            splash_res = json.loads(response.body)
            cookies = splash_res['cookies']
            self.store_img("fb_after_login2.png", splash_res["png"])
            self.save_response("fb_after_login2", splash_res["html"])
            link = "https://www.facebook.com/100000118429707/info"
            # yield Request(url=link, cookies=cookies, callback=self.parse_profile)
            script_text = pkgutil.get_data("dirbot", "resources/fbcook.lua")
            yield Request(url=link,
                          cookies=cookies,
                          meta={
                                'splash': {
                                'args': {'lua_source': script_text,
                                         "cookies": cookies},
                                'endpoint': 'execute',
                                'timeout': self.splash_timeout},
                            },
                          callback=self.parse_profile2)

    def parse_profile(self, response):
        self.save_response("fb_profile", response.body)

    def parse_profile2(self, response):
        if response.status != 200:
            logging.error(response.body)
        else:
            splash_res = json.loads(response.body)
            cookies = splash_res['cookies']
            self.store_img("fb_profile22.png", splash_res["png"])
            self.save_response("fb_profile2", splash_res["html"])