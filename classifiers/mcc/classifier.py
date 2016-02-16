# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
# from sklearn.cross_validation import train_test_split
# from sklearn.pipeline import Pipeline
from sklearn import svm
from sklearn.base import TransformerMixin
import pandas as pd
# import re


# # import numpy as np
# class DenseTransformer(TransformerMixin):
#     def transform(self, X, y=None, **fit_params):
#         return X.todense()
#
#     def fit_transform(self, X, y=None, **fit_params):
#         self.fit(X, y, **fit_params)
#         return self.transform(X)
#
#     def fit(self, X, y=None, **fit_params):
#         return self


class TreeClassifier(TransformerMixin):

    def __init__(self, classifier=None, params=None, maxlevel=None):
        self.tree = {}
        if classifier:
            self.classifier = classifier
        else:
            self.classifier = svm.LinearSVC
        self.params = params
        self.maxlevel = maxlevel

    def fit(self, X, y=None, **fit_params):
        self.tree = self.create_tree(y, True)
        self.vectorizer = CountVectorizer()
        vect = self.vectorizer.fit_transform(X)
        self.transformer = TfidfTransformer()
        self.transformer.fit_transform(vect)
        self.clean_tree()
        self.fit_branch(X, self.tree)
        return self

    def predict(self, X):
        # x_test = self.vectorizer.transform(X)
        result = self.predict_branch(X, self.tree)
        return result

    def clean_tree(self, key='Top'):
        self.tree = {key: self.tree[key]}

    def create_tree(self, y, new=False):
        xdata = pd.DataFrame({'categories': y})
        if new:
            ftree = {}
        else:
            ftree = self.tree
        for ix, xd in xdata.iterrows():
            branch = ftree
            for cat in xd["categories"]:
                if cat in branch:
                    branch[cat]['count'] += 1
                    branch[cat]['ixs'].append(ix)
                    # branch = branch[cat]
                else:
                    branch[cat] = {'ixs': [ix], 'cats': {}, 'count': 0}
                branch = branch[cat]['cats']
                # branch['ixs'].append(ix)
        return ftree

    def fit_branch(self, x, ftree, current_level=0):
        if current_level <= self.maxlevel or not self.maxlevel:
            for cat_name, branch in ftree.items():
                # print cat_name, current_level
                # tdata = data.ix[branch['ixs']]
                xx = []
                yy = []
                cats = branch['cats']
                # print cats
                if len(cats) > 1:
                    for cat, val in cats.iteritems():
                        ixs = val['ixs']
                        # tdata = data.ix[ixs]
                        #FIXME: possible memory problem
                        xx += x.ix[ixs].tolist()
                        yy += [cat for _ in range(len(ixs))]
                        self.fit_branch(x.ix[ixs],
                                        ftree={cat: val},
                                        current_level=current_level+1)
                        # val = res.values()[0]
                        # val['clf'] = cat
                    # print cats
                    # print current_level, set(yy)
                    branch['clf'] = self.make_classification(xx, yy)
                elif cats:
                    cat, val = cats.items()[0]
                    ixs = val['ixs']
                    self.fit_branch(x.ix[ixs],
                                    ftree={cat: val},
                                    current_level=current_level+1)
                    # val = res.values()[0]
        return ftree

    def predict_branch(self, x, ftree, res=None, level=0):
        if not isinstance(res, pd.DataFrame):
            res = pd.DataFrame({'res': [['Top'] for _ in range(len(x))]})
            x = pd.DataFrame({'x': x})
            x.index = res.index
        branch = ftree[ftree.keys()[0]]
        if level <= self.maxlevel or not self.maxlevel:
            if 'clf' in branch:  # Two or more elements in 'cats'
                # prediction = branch['clf'].predict(x['x'])
                prediction = self.make_prediction(x['x'], branch['clf'])
                # print level, set(prediction)
                prediction = pd.DataFrame({'x': x['x'], 'pred': prediction})
                for cat in branch['cats']:
                    prx = prediction[prediction['pred'] == cat]
                    if not prx.empty:
                        prx = prediction[prediction['pred'] == cat].index
                        for i in res.ix[prx].iterrows():
                            i[1]['res'].append(cat)
                        self.predict_branch(x.ix[prx], {cat: branch['cats'][cat]}, res, level=level+1)
            else:# one element at branch
                cat = ftree.keys()[0]
                for i in res.ix[x.index].iterrows():
                    if i[1]['res'][-1] != cat:
                        i[1]['res'].append(cat)
                if branch['cats']:  # One element in 'cats'
                    cat = branch['cats'].keys()[0]
                    self.predict_branch(x, {cat: branch['cats'][cat]}, res, level=level+1)
            # print(res.ix[x.index])
        return res['res']

    def make_classification(self, xx, yy):
        if xx:
            if self.params:
                clf = self.classifier(**self.params)
            else:
                clf = self.classifier()
            vect = self.vectorizer.transform(xx)
            transform = self.transformer.transform(vect)
            # dense = DenseTransformer()
            # den = dense.fit_transform(transform)
            # clf.fit(den, yy)
            clf.fit(transform, yy)
            return clf
        return None

    def make_prediction(self, xx, clf):
        vect = self.vectorizer.transform(xx)
        transform = self.transformer.transform(vect)
        # dense = DenseTransformer()
        # den = dense.fit_transform(transform)
        # result = clf.predict(den)
        result = clf.predict(transform)
        return result