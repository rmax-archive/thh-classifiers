# -*- coding: utf-8 -*-
import json
import logging
import requests


if __name__ == '__main__':
    urls_file = "/media/sf_temp/urls"
    url = 'http://127.0.0.1:8889/functional-classifier/{}'
    # url = 'https://127.0.0.1/functional-classifier/'
    url = 'https://54.200.77.2/functional-classifier/{}'
    headers = {'Authorization': 'Basic YWRtaW46bWVtZXhwYXNz',
                "Content-Type": "application/json"}
    with open(urls_file, "r") as fin:
        for data_url in fin:
            data_r = requests.get(data_url, verify=False)
            data = {"html": data_r.text}
            r = requests.post(url.format(data_url), data=json.dumps(data),
                              headers=headers,
                              verify=False)
            print data_url
            print r.status_code, r.text
            print "---------------------"