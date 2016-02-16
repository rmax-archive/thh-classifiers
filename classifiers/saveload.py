# -*- coding: utf-8 -*-
import os
import pandas as pd
from sklearn.externals import joblib
from sklearn.cross_validation import train_test_split
from sklearn import svm

from mcc.classifier import TreeClassifier
from mcc.metrics import mc_accuracy_score


if __name__ == '__main__':
    # data preparation
    # TODO: separate data preparation
    sample_size = 5000
    min_class_size = 50
    mcc_max_level = 2
    infile = "/media/sf_temp/items_dmoz_8_clf_l.json"
    X_name = "site_text"
    y_name = "categories"
    all_data = pd.read_json(infile)
    if sample_size:
        all_data = all_data.sample(n=sample_size)
    X = all_data[X_name]
    y = all_data[y_name]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    print "data preparation completed"
    # classifier train
    dir_name = "clftest"
    clf_path = os.path.join(".", dir_name, "treeclf.pkl")
    treeclf = TreeClassifier(classifier=svm.LinearSVC, maxlevel=mcc_max_level)
    treeclf.fit(X_train, y_train)
    print "fit completed"
    # classifier dump
    joblib.dump(treeclf, clf_path)
    # classifier load
    treeclf2 = joblib.load(clf_path)
    y_pred = treeclf.predict(X_test)
    print y_pred
    y_pred2 = treeclf2.predict(X_test)
    for level in range(1,3):
        print "Level {}".format(level)
        print "trained accuracy: {}".format(mc_accuracy_score(y_test, y_pred, level=level))
        print "loaded accuracy: {}".format(mc_accuracy_score(y_test, y_pred2, level=level))
        print "Completed"
