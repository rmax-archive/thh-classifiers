# -*- coding: utf-8 -*-
import json
import logging
import requests


if __name__ == '__main__':
    # data_url = 'http://127.0.0.1'
    data_url = 'http://www.rusarmy.com/forum/'
    data_url = 'https://www.punkspider.org'
    data_url = 'http://www.riflegear.com/p-1282-cx4-storm-bullet-button-9mm40sw.aspx'
    # data_url = 'https://www.reddit.com/gold?goldtype=gift'
    url = 'http://127.0.0.1:8889/functional-classifier'
    # url = 'https://127.0.0.1/functional-classifier/'
    # url = 'https://54.200.77.2/functional-classifier/4321432'
    headers = {'Authorization': 'Basic YWRtaW46bWVtZXhwYXNz',
                "Content-Type": "application/json"}
    data_r = requests.get(data_url, verify=False)
    data = {"html": data_r.text}
    # data = {"html": "hello world"}
    r = requests.post(url, data=json.dumps(data),
                      headers=headers,
                      verify=False)
    print r.status_code
    print r.text
    print r.json()
    print "---------------------"