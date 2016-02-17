# -*- coding: utf-8 -*-
import os
import json
import pandas as pd
from sklearn.externals import joblib
from sklearn.cross_validation import train_test_split
from sklearn import svm

from mcc.categorize import TreeCategorize


if __name__ == '__main__':
    infile = "/media/sf_temp/items_dmoz_8.json"
    with open(infile, "r") as fin:
        cnt = 0
        for text_line in fin:
            item = json.loads(text_line)
            cats = [x.replace("\r\n\r\n", "").strip() for x in item["categories"]]
            cats = [x for x in cats if x and len(x)>1]
            cats.remove("Top")
            html = item["html_code"]
            url = item["url"]
            categorizer = TreeCategorize(url=url, html=html)
            res = categorizer.categorize()
            print "real: {}".format(cats)
            print "predicted: {}".format(res)
            cnt += 1
            if cnt > 100:
                break
    print "Completed"
