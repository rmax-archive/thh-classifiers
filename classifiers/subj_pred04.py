# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
# from sklearn.metrics import classification_report
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.semi_supervised import label_propagation
from sklearn.pipeline import Pipeline
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.base import TransformerMixin
import pandas as pd


# import numpy as np
class DenseTransformer(TransformerMixin):
    def transform(self, X, y=None, **fit_params):
        return X.todense()

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        return self.transform(X)

    def fit(self, X, y=None, **fit_params):
        return self


class TreeClassifier(TransformerMixin):
    def __init__(self, classifier=None, params=None):
        self.tree = {}
        if classifier:
            self.classifier = classifier
        else:
            self.classifier = svm.LinearSVC
        self.params = params

    # def transform(self, X, y=None, **fit_params):
    #     return X.todense()

    # def fit_transform(self, X, y=None, **fit_params):
    #     self.fit(X, y, **fit_params)
    #     return self.transform(X)

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

    def fit_branch(self, x, ftree):
        for branch in ftree.itervalues():
            # tdata = data.ix[branch['ixs']]
            xx = []
            yy = []
            cats = branch['cats']
            if len(cats) > 1:
                for cat, val in cats.iteritems():
                    ixs = val['ixs']
                    # tdata = data.ix[ixs]
                    xx += x.ix[ixs].tolist()
                    yy += [cat for _ in range(len(ixs))]
                    self.fit_branch(x.ix[ixs], {cat: val})
                    # val = res.values()[0]
                    # val['clf'] = cat
                # print cats
                branch['clf'] = self.make_classification(xx, yy)
            elif cats:
                cat, val = cats.items()[0]
                ixs = val['ixs']
                self.fit_branch(x.ix[ixs], {cat: val})
                # val = res.values()[0]
        return ftree

    def predict_branch(self, x, ftree, res=None):
        if not isinstance(res, pd.DataFrame):
            res = pd.DataFrame({'res': [['Top'] for _ in range(len(x))]})
            x = pd.DataFrame({'x': x})
            x.index = res.index
        branch = ftree[ftree.keys()[0]]
        if 'clf' in branch:  # Two or more elements in 'cats'
            # prediction = branch['clf'].predict(x['x'])
            prediction = self.make_prediction(x['x'], branch['clf'])
            prediction = pd.DataFrame({'x': x['x'], 'pred': prediction})
            for cat in branch['cats']:
                prx = prediction[prediction['pred'] == cat]
                if not prx.empty:
                    prx = prediction[prediction['pred'] == cat].index
                    for i in res.ix[prx].iterrows():
                        i[1]['res'].append(cat)
                    self.predict_branch(x.ix[prx], {cat: branch['cats'][cat]}, res)
        else:
            cat = ftree.keys()[0]
            for i in res.ix[x.index].iterrows():
                if i[1]['res'][-1] != cat:
                    i[1]['res'].append(cat)
            if branch['cats']:  # One element in 'cats'
                cat = branch['cats'].keys()[0]
                self.predict_branch(x, {cat: branch['cats'][cat]}, res)
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
            clf.fit(transform, yy)
            # clf_pipe = Pipeline([('vect', self.vectorizer),  #  CountVectorizer()),
            #                      ('tfidf', self.transformer),
            #                      ('to_dense', DenseTransformer()),
            #                      ('clf', clf)])
            # clf_pipe = clf_pipe.fit(xx, yy)
            return clf
        return None

    def make_prediction(self, xx, clf):
        vect = self.vectorizer.transform(xx)
        transform = self.transformer.transform(vect)
        # dense = DenseTransformer()
        # den = dense.fit_transform(transform)
        result = clf.predict(transform)
        return result


def check_prediction(result):
    predl = res['pred'].apply(lambda l: l[1])
    testl = res['test'].apply(lambda l: l[1])
    return accuracy_score(predl, testl)


if __name__ == '__main__':
    sample_size = 1500
    min_class_size = 50
    # train by description
    # infile = "/media/sf_temp/items_dmoz_5.json"
    # X_name = "description"
    # train by site page
    # infile = "./items_dmoz_6_clf_sample.json"
    infile = "/media/sf_temp/items_dmoz_8_clf_l.json"
    X_name = "site_text"
    y_name = "categories"

    all_data = pd.read_json(infile)
    if sample_size:
        all_data = all_data.sample(n=sample_size)

    X = all_data[X_name]
    y = all_data[y_name]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    # Random Forest Classifier
    # pr = {'max_depth': 5, 'n_estimators': 10, 'max_features': 1, 'random_state': 100}
    # treeclf = TreeClassifier(classifier=RandomForestClassifier, params=None)

    # Gaussian
    # treeclf = TreeClassifier(classifier=GaussianNB)

    # pr = {'kernel': "linear", 'C': 0.025}
    # treeclf = TreeClassifier(classifier=svm.SVC, params=pr)
    treeclf = TreeClassifier(classifier=svm.LinearSVC)
    treeclf.fit(X_train, y_train)
    pred = treeclf.predict(X_test)
    # print(pred)
    res = pd.DataFrame({'test': y_test.tolist(), 'pred': pred.tolist()})
    print res.head()
    res1 = check_prediction(res)
    print '{0:.2%}'.format(res1)