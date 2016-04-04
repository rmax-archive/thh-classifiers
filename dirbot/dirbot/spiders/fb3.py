# encoding: utf-8
from urlparse import urljoin, urlparse, ParseResult
import pkgutil
import json
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
import logging
import os
import io
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO
import base64


class FB3Spider(Spider):
    name = "fb3"
    imgstorage = "/media/sf_temp/"
    img_count = 0
    handle_httpstatus_list = [400, 404, 401, 403, 301, 302, 500, 520]
    splash_timeout = 1000
    facebook_ids = ["100001665518840", "100000118429707"]
    start_urls = []
    scripts = {
        "fblogin": pkgutil.get_data("dirbot", "resources/fblogin.lua"),
        "fbcook": pkgutil.get_data("dirbot", "resources/fbcook.lua"),
        "fb_info": pkgutil.get_data("dirbot", "resources/fb_info.lua"),
    }
    account = {'email': "nikaskriabina@gmail.com",
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
            fout.write(self.img_convert(file_content))
        return full_path

    def img_convert(self, image_splash):
        image_string = StringIO(base64.b64decode(image_splash))
        return image_string.read()

    def save_response(self,page_name, page_body):
        _u = lambda t: t.decode('UTF-8', 'ignore') if isinstance(t, str) else t
        with io.open("/media/sf_temp/{}.html".format(page_name), "w", encoding="utf-8") as fout:
            fout.write(unicode(_u(page_body)))
            # fout.write(page_body.encode("utf8", errors="ignore"))

    def get_profile_base(self, url):
        o = urlparse(url)
        o2 = ParseResult(o.scheme, o.netloc, o.path, params="", query="", fragment="")
        return o2.geturl()

    def parse_main(self, response):
        # logging.info(response.body)
        if response.status != 200:
            logging.error(response.body)
        else:
            splash_res = json.loads(response.body)
            cookies = splash_res['cookies']
            self.store_img("fb_after_login2.png", splash_res["png"])
            self.save_response("fb_after_login2", splash_res["html"])
            link = "https://www.facebook.com/app_scoped_user_id/834835679993544/"
            # yield Request(url=link, cookies=cookies, callback=self.parse_profile)
            yield self.get_splash_request(script_name="fbcook",
                           cookies=cookies,
                           url=link,
                           callback=self.parse_profile,
                        )
            # script_text = pkgutil.get_data("dirbot", "resources/fbcook.lua")
            # yield Request(url=link,
            #               cookies=cookies,
            #               meta={
            #                     'splash': {
            #                     'args': {'lua_source': script_text,
            #                              "cookies": cookies},
            #                     'endpoint': 'execute',
            #                     'timeout': self.splash_timeout},
            #                 },
            #               callback=self.parse_profile)

    def get_splash_request(self, script_name,
                           cookies,
                           url,
                           callback,
                           endpoint="execute",
                           ):
        script = self.scripts.get(script_name, "")
        return Request(url=url,
                          cookies=cookies,
                          meta={
                                'splash': {
                                'args': {'lua_source': script,
                                         "cookies": cookies},
                                'endpoint': endpoint,
                                'timeout': self.splash_timeout},
                            },
                          callback=callback,
                          dont_filter=True)

    def parse_profile(self, response):
        if response.status != 200:
            logging.error(response.body)
        else:
            splash_res = json.loads(response.body)
            cookies = splash_res['cookies']
            current_url = splash_res['url']
            new_url = current_url + "/info"
            self.store_img("fb_profile22.png", splash_res["png"])
            self.save_response("fb_profile2", splash_res["html"])
            logging.info(current_url)
            logging.info(new_url)
            req = self.get_splash_request(script_name="fb_info",
                           cookies=cookies,
                           url=new_url,
                           callback=self.parse_info,
                        )
            req.meta["profile_url"] = current_url
            yield req

    def parse_info(self, response):
        if response.status != 200:
            logging.error(response.body)
        else:
            splash_res = json.loads(response.body)
            cookies = splash_res['cookies']
            current_url = splash_res['url']
            # new_url = current_url + "/info"
            self.store_img("fb_info.png", splash_res["png"])
            self.save_response("fb_info", splash_res["html"])
            # self.save_response("fb_info", splash_res["html"])
            profile_pages = splash_res.get('pages', {})
            # logging.info(splash_res.get('pages', {}).keys())
            for page_name in profile_pages:
                page_text = profile_pages[page_name]
                page_sel = Selector(text=page_text)
                texts = page_sel.xpath('//ul/li[2]/div[contains(@class, "clearfix")]/div[1]//text()').extract()
                logging.info(page_name)
                logging.info(texts)
            friends_url = response.meta["profile_url"] + "/friends"
            req = self.get_splash_request(script_name="fbcook",
                           cookies=cookies,
                           url=friends_url,
                           callback=self.parse_friends,
                        )
            req.meta["profile_url"] = response.meta["profile_url"]
            yield req

    def parse_friends(self, response):
        if response.status != 200:
            logging.error(response.body)
        else:
            splash_res = json.loads(response.body)
            self.store_img("fb_friends.png", splash_res["png"])
            self.save_response("fb_friends", splash_res["html"])
            page_sel = Selector(text=splash_res["html"])
            friends = page_sel.xpath('//ul[contains(@data-pnref, "friends")]/li/div/a/@href').extract()
            logging.info(friends)

