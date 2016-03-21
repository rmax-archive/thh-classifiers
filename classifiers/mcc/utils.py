# -*- coding: utf-8 -*-
from html2text import html2text
from lxml.html.clean import Cleaner
from lxml import etree
import lxml.html


def filter_rare_classes(data, class_field, min_class_size,
                        mode="remove", replace_class=None):
    class_cnt = data[class_field].value_counts()
    if mode == "remove":
        class_take = class_cnt.index[class_cnt >= min_class_size]
        data = data[data[class_field].isin(class_take)]
    elif mode == "rename":
        class_rename = class_cnt.index[class_cnt < min_class_size]
        data[class_field][class_rename] = replace_class
    return data


def get_text_from_html(html_text, use_markdown=True):
    if use_markdown:
        text = html2text(html_text)
    else:
        cleaner = Cleaner()
        cleaner.javascript = False
        cleaner.style = False
        # raw_tree = etree.HTML(html_text)
        tree = lxml.html.fromstring(cleaner.clean_html(html_text))
        text = tree.text_content()
    return text


def check_input_string(text):
    return len(text) > 100
