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
from mcc.classifier import TreeClassifier


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