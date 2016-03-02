# -*- coding: utf-8 -*-
from __future__ import print_function

from pprint import pprint
from time import time
import logging
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.cross_validation import train_test_split
from sklearn.semi_supervised import label_propagation
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn import svm
from sklearn.base import TransformerMixin
from sklearn.linear_model import SGDClassifier
from sklearn.grid_search import GridSearchCV
import pandas as pd
import numpy as np

from mcc.utils import filter_rare_classes
from mcc.classifier import FilteredSVC


sample_size = 0
min_class_size = 100
test_sample_size = 0.3
infile = "/media/sf_temp/func_class_items_texts.json"
class_field = "category"
all_data = pd.read_json(infile)
all_data = filter_rare_classes(all_data,
                               class_field=class_field,
                               min_class_size=min_class_size)
if sample_size:
    data = all_data.sample(n=sample_size)
else:
    data = all_data

print(data[class_field].value_counts())

X = data["site_text"]
y = data[class_field]

X_train, X_test, y_train, y_test = train_test_split(X, y,
                        test_size=test_sample_size, random_state=42)

pipeline = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', SGDClassifier()),
])
parameters = {
    'vect__max_df': (0.5, 0.75, 1.0),
    'vect__max_features': (None, 5000, 10000, 50000),
    'vect__ngram_range': ((1, 1), (1, 2)),  # unigrams or bigrams
    # 'tfidf__use_idf': (True, False),
    # 'tfidf__norm': ('l1', 'l2'),
    'clf__alpha': (0.00001, 0.000001),
    'clf__penalty': ('l2', 'elasticnet'),
    # 'clf__n_iter': (10, 50, 80),
}

if __name__ == "__main__":
    # multiprocessing requires the fork to happen in a __main__ protected
    # block

    # find the best parameters for both the feature extraction and the
    # classifier
    grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1)

    print("Performing grid search...")
    print("pipeline:", [name for name, _ in pipeline.steps])
    print("parameters:")
    pprint(parameters)
    t0 = time()
    grid_search.fit(X, y)
    print("done in %0.3fs" % (time() - t0))
    print()

    print("Best score: %0.3f" % grid_search.best_score_)
    print("Best parameters set:")
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))

