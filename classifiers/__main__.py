# -*- coding: utf-8 -*-
import os
import logging
from urlparse import urlparse
import tornado.ioloop
import tornado.web
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
from sklearn import svm
import pandas as pd

from mcc.utils import get_text_from_html, check_input_string
from mcc.classifier import FilteredSVC


logging.basicConfig(level=logging.DEBUG)

from ConfigParser import SafeConfigParser

_ROOT = os.path.abspath(os.path.dirname(__file__))

FILENAMES = [
    os.path.join(_ROOT, 'settings', 'defaults.conf'),
]


known_domains = {
    "www.facebook.com": "social",
    "www.pinterest.com": "social",
    "plus.google.com": "social",
    "www.reddit.com": "news"
}


def load_settings(config_files=(), overrides=()):
    cp = SafeConfigParser()
    # cp.read(FILENAMES + config_files)
    cp.read(FILENAMES)

    for section, option, value in overrides:
        if value is not None:
            if isinstance(value, bool):
                value = int(value)
            cp.set(section, option, str(value))

    return {
        section: dict(cp.items(section))
        for section in cp.sections()
    }


_clf = {}


class ClassifyHandler(tornado.web.RequestHandler):

    def post(self, *args, **kwargs):
        logging.debug(self.request.uri)
        undef_cats = ["UNDEFINED"]
        res = []
        data = tornado.escape.json_decode(self.request.body)
        html_text = data["html"]
        if check_input_string(html_text):
            method_path_base = "/functional-classifier/"
            site_url = self.request.uri.replace(method_path_base, "")
            parse_res = urlparse(site_url)
            if parse_res.netloc in known_domains:
                res = [known_domains[parse_res.netloc]]
            else:
                clean_text = get_text_from_html(html_text, use_markdown=True)
                logging.debug(parse_res.netloc)
                # logging.debug(self.request.uri)
                # logging.debug(self.request.path)
                # logging.debug(self.request.query)
                logging.debug(len(html_text))
                logging.debug(len(clean_text))
                fclf = _clf["function"]
                page_cat = fclf.predict([clean_text])
                page_cat = [x for x in page_cat if not x in undef_cats]
                res.extend(page_cat)
        else:
            res = []
        self.write({"categories":res})


def make_app():
    app = tornado.web.Application([
        (r"/functional-classifier", ClassifyHandler),
        (r"/functional-classifier/(.*)", ClassifyHandler),
    ])
    return app


def make_func_clf(data_file, min_distance=0.0, debug=False):
    logging.info("Classifier training started")
    all_data = pd.read_json(data_file)
    X = all_data["site_text"]
    y = all_data["category"]
    c = 1
    svmclf = svm.LinearSVC(penalty='l2', dual=False, C=c)
    clf = FilteredSVC(svmclf, min_distance=min_distance)
    clf_pipeline = Pipeline([('vect', CountVectorizer()),
                        ('tfidf', TfidfTransformer()),
                        ('clf', clf)])
    clf_pipeline = clf_pipeline.fit(X, y)
    if debug:
        #FIXME: testing on training dataset
        y_test_pred = clf_pipeline.predict(X)
        logging.debug(classification_report(y, y_test_pred))
    logging.info("Classifier training completed")
    return clf_pipeline


if __name__ == "__main__":
    opts = load_settings()
    clf_opts = opts["classifier"]
    port = int(clf_opts['port'])
    host = clf_opts['host']
    debug = clf_opts['debug']
    data_file = clf_opts['data_file']
    clf_file = clf_opts['clf_file']
    min_distance = 0.2
    if not os.path.exists(clf_file):
        fclf = make_func_clf(data_file, min_distance, debug)
        joblib.dump(fclf, clf_file)
    else:
        logging.info("Classifier load started")
        fclf = joblib.load(clf_file)
        logging.info("Classifier loaded")
    _clf["function"] = fclf
    app = make_app()
    app.listen(int(port), host)
    tornado.ioloop.IOLoop.current().start()