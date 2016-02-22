# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.cross_validation import train_test_split
from sklearn.semi_supervised import label_propagation
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn import svm
from sklearn.base import TransformerMixin
import pandas as pd
import numpy as np

from mcc.utils import filter_rare_classes


class FilteredSVC(object):

    def __init__(self, clf, filter=True, min_distance=0.0, replace_class="UNDEFINED"):
        self.clf = clf
        self.filter = filter
        self.replace_class = replace_class
        self.min_distance = min_distance

    def decision_function(self,X):
        return self.clf.decision_function(X)

    def get_params(self, deep=True):
        return self.clf.get_params(deep)

    def predict(self, X):
        prediction = self.clf.predict(X)
        if self.filter:
            decision = self.clf.decision_function(X)
            decision_fail = decision.max(axis=1) < self.min_distance
            prediction[decision_fail] = self.replace_class
        return prediction

    # def transform(self, X, y=None, **fit_params):
    #     return X.todense()
    #
    # def fit_transform(self, X, y=None, **fit_params):
    #     self.fit(X, y, **fit_params)
    #     return self.transform(X)

    def fit(self, X, y, sample_weight=None):
        return self.clf.fit(X, y)


if __name__ == '__main__':
    sample_size = 0
    min_class_size = 50
    test_sample_size = 0.3
    infile = "/media/sf_temp/func_class_items_texts.json"

    all_data = pd.read_json(infile)
    all_data = filter_rare_classes(all_data, class_field="category", min_class_size=100)
    if sample_size:
        data = all_data.sample(n=sample_size)
    else:
        data = all_data

    print data["category"].value_counts()

    X = data["site_text"]
    y = data["category"]


    X_train, X_test, y_train, y_test = train_test_split(X, y,
                            test_size=test_sample_size, random_state=42)

    y_sample = y_train
    X_sample = X_train
    # clf = svm.SVC(probability=True, verbose=True)
    clf = svm.LinearSVC()
    clf = FilteredSVC(clf, min_distance=0.1)
    clf_pipeline = Pipeline([('vect', CountVectorizer()),
                        ('tfidf', TfidfTransformer()),
                        ('clf', clf)])
    clf_pipeline = clf_pipeline.fit(X_sample, y_sample)
    y_test_pred = clf_pipeline.predict(X_test)
    y_test_prob = clf_pipeline.decision_function(X_test)
    y_train_pred = clf_pipeline.predict(X_sample)

    # print y_test.shape
    # print y_test_pred.shape
    # print y_test_prob.shape
    # print y_test[:10]
    # print y_test_pred[:10]
    print "Train:"
    print(classification_report(y_train, y_train_pred))
    print "Test:"
    print(classification_report(y_test, y_test_pred))
    prod_data = pd.DataFrame(data=y_test_prob, columns=clf.clf.classes_)
    prod_data["max_dist"] = y_test_prob.max(axis=1)
    prod_data["y_pred"] = y_test_pred
    prod_data["y_true"] = y_test.values
    prod_data["y_true"] = y_test.values
    prod_data["correct"] = prod_data["y_pred"] == prod_data["y_true"]
    prod_data["ltz"] = prod_data["max_dist"] > 0
    # y_test = prod_data["y_true"][prod_data["max_dist"] > 0.05]
    # y_test_pred = prod_data["y_pred"][prod_data["max_dist"] > 0.05]
    # print(classification_report(y_test, y_test_pred))
    out_path = "/media/sf_temp/y_proba.csv"
    prod_data.to_csv(out_path, sep=";", index_label="id", decimal=",")
    # lr_X = prod_data["max_dist"].values.reshape(-1, 1)
    # lr_y = prod_data["correct"].values.reshape(-1, 1)
    # print lr_X.shape, lr_y.shape
    # lr = LogisticRegression()
    # lr.fit(lr_X, lr_y)
    # print(classification_report(lr_y, lr.predict(lr_X)))
