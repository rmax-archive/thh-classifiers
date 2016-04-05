# encoding: utf-8
from urlparse import urljoin, urlparse, ParseResult
import pkgutil
import json
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request, FormRequest
import logging
import os
import io
# from scrapyjs import SplashRequest
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO
import base64
from scrapy import Item, Field
import dirbot.settings as settings


API_ENDPOINT = "https://graph.facebook.com/v2.5/"
_FB_SEARCH_FIELDS = [
    'id', 'name', 'age_range', 'bio', 'gender', 'website', 'work', 'link'
]


class FbSearchItem(Item):
    id = Field()
    name = Field()
    url = Field()
    keywords = Field()
    userinfo = Field()
    friends = Field()


class FB4Spider(Spider):
    name = "fb4"
    imgstorage = "/media/sf_temp/"
    handle_httpstatus_list = [400, 404, 401, 403, 301, 302, 500, 520]
    splash_timeout = 1000
    queries = ["Alexander Peremiatov"]
    start_urls = []
    next_page_delay = 10
    follow_next = False
    store_local = True
    scripts = {
        "fblogin": pkgutil.get_data("dirbot", "resources/fblogin.lua"),
        "fbcook": pkgutil.get_data("dirbot", "resources/fbcook.lua"),
        "fb_info": pkgutil.get_data("dirbot", "resources/fb_info.lua"),
    }
    account = {'email': "nikaskriabina@gmail.com",
                'password':  "F,hfrflf,hf2016"}

    # def fb_login(self):
    #     url = "https://www.facebook.com/login.php"
    #     yield self.get_splash_request(script_name="fblogin",
    #                        cookies={},
    #                        url=url,
    #                        callback=self.parse_main,
    #                        add_args=self.account
    #                     )

    def start_requests(self):
        for query in self.queries:
            self.log("Querying for %s" % query, logging.INFO)
            yield self.get_api_request(query=query,
                                   meta={"keywords": query},
                                   callback=self.parse_api_search_results)

    def get_api_request(self, query=None,
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

    def parse_api_search_results(self, response):
        if response.status != 200:
            self.log(
                'Response %s has a non-200 status with body: %s'
                % (str(response), response.body), level=logging.WARNING )
            return
        data = json.loads(response.body)
        kw = response.meta.get("keywords", "")
        # self.log(data,level=logging.INFO)
        for search_res in data['data']:
            self.log(search_res, level=logging.INFO)
            args = {}
            args.update(self.account)
            item = {}
            item["id"] = search_res["id"]
            item["name"] = search_res["name"]
            item["keywords"] = kw
            item["friends"] = []
            item["userinfo"] = {}
            url = "https://www.facebook.com/login.php"
            yield self.get_splash_request(script_name="fblogin",
                           cookies={},
                           url=url,
                           callback=self.parse_main,
                           add_args=args,
                           add_meta={"item":item}
                        )
            # yield FormRequest(
            #     API_ENDPOINT + search_res["id"],
            #     method="GET",
            #     callback=self.parse_user,
            #     formdata=dict((k, v) for k, v in formdata.iteritems() if v),
            #     meta={}
            # )
        if self.follow_next:
            if 'paging' in data and 'next' in data['paging']:
                yield Request(data['paging']['next'],
                              dont_filter=True,
                              meta={"keywords": kw,
                                    'delay_request': self.next_page_delay,
                              })

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
            item = response.meta["item"]
            link = "https://www.facebook.com/app_scoped_user_id/{}/".format(item["id"])
            # yield Request(url=link, cookies=cookies, callback=self.parse_profile)
            yield self.get_splash_request(script_name="fbcook",
                           cookies=cookies,
                           url=link,
                           callback=self.parse_profile,
                           add_meta={"item": item}
                        )

    def get_splash_request(self, script_name,
                           cookies,
                           url,
                           callback,
                           endpoint="execute",
                           add_args={},
                           add_meta={},
                           ):
        script = self.scripts.get(script_name, "")
        args = {'lua_source': script, "cookies": cookies}
        args.update(add_args)
        # return SplashRequest(url, callback,
        #         args=args,
        #         endpoint=endpoint,
        #     )
        meta={'splash': {'args': args,
                        'endpoint': endpoint,
                        'timeout': self.splash_timeout},
                        }
        meta.update(add_meta)
        return Request(url=url,
                          cookies=cookies,
                          meta=meta,
                          callback=callback,
                          dont_filter=True)

    def parse_profile(self, response):
        if response.status != 200:
            logging.error(response.body)
        else:
            splash_res = json.loads(response.body)
            current_url = splash_res['url']
            item = response.meta["item"]
            item["url"] = current_url
            cookies = splash_res['cookies']
            new_url = current_url + "/info"
            self.store_img("fb_profile22.png", splash_res["png"])
            self.save_response("fb_profile2", splash_res["html"])
            logging.info(current_url)
            logging.info(new_url)
            req = self.get_splash_request(script_name="fb_info",
                           cookies=cookies,
                           url=new_url,
                           callback=self.parse_info,
                           add_meta={"item": item})
            yield req

    def parse_info(self, response):
        if response.status != 200:
            logging.error(response.body)
        else:
            item = response.meta["item"]
            splash_res = json.loads(response.body)
            cookies = splash_res['cookies']
            self.store_img("fb_info.png", splash_res["png"])
            self.save_response("fb_info", splash_res["html"])
            profile_pages = splash_res.get('pages', {})
            # logging.info(splash_res.get('pages', {}).keys())
            for page_name in profile_pages:
                page_text = profile_pages[page_name]
                page_sel = Selector(text=page_text)
                texts = page_sel.xpath('//ul/li[2]/div[contains(@class, "clearfix")]/div[1]//text()').extract()
                logging.info(page_name)
                logging.info(texts)
                item["userinfo"][page_name] = texts
            friends_url = item["url"] + "/friends"
            req = self.get_splash_request(script_name="fbcook",
                           cookies=cookies,
                           url=friends_url,
                           callback=self.parse_friends,
                           add_meta={"item":item}
                        )
            yield req

    def parse_friends(self, response):
        if response.status != 200:
            logging.error(response.body)
        else:
            item = response.meta["item"]
            splash_res = json.loads(response.body)
            self.store_img("fb_friends.png", splash_res["png"])
            self.save_response("fb_friends", splash_res["html"])
            page_sel = Selector(text=splash_res["html"])
            friends = page_sel.xpath('//ul[contains(@data-pnref, "friends")]/li/div/a/@href').extract()
            logging.info(friends)
            item["friends"].extend(friends)
            logging.info(item)
            res_item = FbSearchItem()
            res_item.update(item)
            yield res_item

