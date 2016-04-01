import logging
import csv
import cStringIO
import re
import random
from datetime import datetime

from scrapy import log
from scrapy.conf import settings
from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
from scrapy.spider import Spider


class FB2Spider(Spider):
    name = 'fb2'
    account = {}

    def start_requests(self):
        self.account['email'] = "nikaskriabina@gmail.com"
        self.account['password'] = "F,hfrflf,hf2016"
        # dob = "1990.01.01"
        self.account['year'] = "1990"
        self.account['month'] = "1"
        self.account['day'] = "1"
        yield Request('https://www.facebook.com', callback=self.log_in)

    def log_in(self, response):
        self.save_response("fb_before_login", response.body)
        # set current account
        self.current_account = self.account
        logging.debug('Logging in with: %s' % self.current_account['email'])
        return FormRequest.from_response(
            response,
            formdata={'email': self.current_account['email'],
                      'pass': self.current_account['password']},
            callback=self.check_log_in,
            dont_filter=True
        )

    def check_log_in(self, response):
        if 'checkpoint' in response.url:
            return FormRequest.from_response(
                response,
                formdata={'submit[Continue]': 'Continue'},
                callback=self.birthday_captcha,
                dont_filter=True
            )
        else:
            return self.login_finished(response)

    def birthday_captcha(self, response):
        return FormRequest.from_response(
            response,
            formdata={'birthday_captcha_month': self.current_account['month'],
                      'birthday_captcha_day': self.current_account['day'],
                      'birthday_captcha_year': self.current_account['year'],
                      'submit[Continue]': 'Continue'},
            callback=self.confirm_location,
            dont_filter=True
        )

    def confirm_location(self, response):
        if 'checkpoint' in response.url:
            return FormRequest.from_response(
                response,
                formdata={'submit[This was me]': 'This was me'},
                callback=self.login_finished,
                dont_filter=True
            )
        else:
            return self.login_finished(response)

    def login_finished(self, response):
        self.save_response("fb_after_login", response.body)
        facebook_ids = ["100001665518840", "100000118429707"]
        reqs = []
        for facebook_id in facebook_ids:
            reqs.append(Request('https://www.facebook.com/%s' % facebook_id,
                          callback=self.parse_profile,
                          meta={"id":facebook_id}))
        return reqs

    def parse_profile(self, response):
        self.save_response("fb_profile", response.body)
        return Request(response.url + '/info',
                       callback=self.parse_about,
                       meta={"id":response.meta["id"]})

    def save_response(self,page_name, page_body):
        with open("/media/sf_temp/{}.html".format(page_name), "w") as fout:
            fout.write(page_body)

    def parse_about(self, response):
        self.save_response(response.meta["id"], response.body)
        sel = Selector(response)
        logging.info("name = {}".format(sel.xpath('//title').extract()))
        for comment in sel.xpath('//*[not(self::script)]/comment()'):
            comment_string = u''.join(comment.extract()).strip()
            m = re.compile(r'<!..(.+)..>', re.UNICODE).search(comment_string)
            if m:
                logging.info(m.group(1).strip())