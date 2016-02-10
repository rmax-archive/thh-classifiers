# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.cross_validation import train_test_split
from sklearn.semi_supervised import label_propagation
from sklearn.pipeline import Pipeline
from sklearn import svm
from sklearn.base import TransformerMixin
import pandas as pd
import numpy as np


class DenseTransformer(TransformerMixin):

    def transform(self, X, y=None, **fit_params):
        return X.todense()

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        return self.transform(X)

    def fit(self, X, y=None, **fit_params):
        return self

if __name__ == '__main__':
    sample_size = 0
    sample_size = 0
    min_class_size = 50
    # train by description
    # infile = "/media/sf_temp/items_dmoz_5.json"
    # X_name = "description"
    # train by site page
    infile = "/media/sf_temp/items_dmoz_8_clf_l.json"
    # infile = "./items_dmoz_6_clf_sample.json"
    X_name = "site_text"


    all_data = pd.read_json(infile)
    if sample_size:
        data = all_data.sample(n=sample_size)
    else:
        data = all_data

    print data

    # filter out rare classes
    y_cnt = data["category1"].value_counts()
    y_take = y_cnt.index[y_cnt > min_class_size]
    data = data[data["category1"].isin(y_take)]

    X = data[X_name]
    y = data["category1"]


    X_train, X_test, y_train, y_test = train_test_split(X, y,
                            test_size=0.4, random_state=42)

    clfs = [[svm.LinearSVC(),"LinearSVC, default params, 100% of train data", 0],
            # [svm.LinearSVC(),"LinearSVC, default params, 50% of train data", 0.5],
            # [svm.LinearSVC(),"LinearSVC, default params, 10% of train data", 0.1],
            # [svm.LinearSVC(),"LinearSVC, default params, 5% of train data", 0.05],
            # [svm.LinearSVC(),"LinearSVC, default params, 1% of train data", 0.01],
            # [label_propagation.LabelSpreading(),"Label spreading, 10% of train data", 0.1],
            # [label_propagation.LabelSpreading(),"Label spreading, 30% of train data", 0.3],
            # [label_propagation.LabelSpreading(),"Label spreading, 50% of train data", 0.5],
            # [label_propagation.LabelSpreading(),"Label spreading, 70% of train data", 0.7],
            # [label_propagation.LabelSpreading(),"Label spreading, 100% of train data", 0],
            ]
    rng = np.random.RandomState(0)

    for clf, descr, train_sample in clfs:
        if train_sample:
            # y_sample = np.copy(y_train)
            inc_ind = rng.rand(len(y_train)) < train_sample
            y_sample = y_train[inc_ind]
            X_sample = X_train[inc_ind]
            # y_sample[rng.rand(len(y_train)) < train_sample] = -1
        else:
            y_sample = y_train
            X_sample = X_train
        clf_pipeline = Pipeline([('vect', CountVectorizer()),
                            ('tfidf', TfidfTransformer()),
                            # ('to_dense', DenseTransformer()),
                            ('clf', clf)])
        clf_pipeline = clf_pipeline.fit(X_sample, y_sample)
        y_pred = clf_pipeline.predict(X_test)
        y_train_pred = clf_pipeline.predict(X_sample)
        print descr
        print(classification_report(y_test, y_pred))