# -*- coding: utf-8 -*-
import json
import logging
import requests


if __name__ == '__main__':
    data_url = 'http://127.0.0.1'
    data_url = 'http://www.rusarmy.com/forum/'
    url = 'http://127.0.0.1:8889/functional-classifier'
    url = 'https://127.0.0.1/functional-classifier/111'
    # url = 'https://54.191.238.117/crawler/start'
    headers = {'Authorization': 'Basic YWRtaW46bWVtZXhwYXNz',
                "Content-Type": "application/json"}
    data_r = requests.get(data_url)
    data = {"html": data_r.text}
    r = requests.post(url, data=json.dumps(data),
                      headers=headers,
                      verify=False)
    print r
    print r.text
    print r.json
    print "---------------------"