# -*- coding: utf-8 -*-
import os
import requests
from html2text import html2text
from lxml.html.clean import Cleaner
from lxml import etree
from sklearn.externals import joblib

from classifier import TreeClassifier

_clf = {}


def get_classifier(path):
    if path not in _clf:
        _clf[path] = joblib.load(path)
    return _clf[path]


class TreeCategorize(object):
    text = None
    matched_categories = []
    clf_path = os.path.join("/media/sf_temp", "clftest", "treeclf.pkl")

    def __init__(self, url, html=None, text_extraction="html2text"):

        if not html:
            self.r = requests.get(url)
            self.html = self.r.text
        else:
            self.html = html

        if text_extraction == "html2text":
            self.text = html2text(self.html)
        elif text_extraction == "xpath":
            self.cleaner = Cleaner()
            self.cleaner.javascript = False
            self.cleaner.style = False
            self.raw_tree = etree.HTML(self.html)
            self.tree = etree.HTML(self.cleaner.clean_html(self.html))
            self.text = self.tree.text_content()

    def categorize(self):
        clf = get_classifier(self.clf_path)
        cats = clf.predict([self.text])
        # print cats
        if len(cats):
            cats = cats[0]
            if cats[0] == "Top":
                cats.remove("Top")
        return cats

