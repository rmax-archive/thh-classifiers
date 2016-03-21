# -*- coding: utf-8 -*-
from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.cross_validation import train_test_split
from sklearn.semi_supervised import label_propagation
from sklearn.externals import joblib
from sklearn.pipeline import Pipeline
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn import svm

import pandas as pd
import numpy as np
import skflow
import tensorflow as tf

from mcc.utils import filter_rare_classes


net_params = {}


def cnn_model(X, y):

    # word_vectors = skflow.ops.categorical_variable(X, n_classes=n_words,
    #     embedding_size=net_params["EMBEDDING_SIZE"], name='words')
    # print "word_vectors.1:", word_vectors.get_shape()
    # word_vectors = tf.expand_dims(word_vectors, 3)
    # print "word_vectors.2:", word_vectors.get_shape()
    word_vectors = tf.expand_dims(X, 2)
    print "word_vectors.1:", word_vectors.get_shape()
    word_vectors = tf.expand_dims(word_vectors, 3)
    print "word_vectors.2:", word_vectors.get_shape()

    # with tf.variable_scope('CNN_Layer1'):
    #     conv1 = skflow.ops.conv2d(word_vectors, net_params["N_FILTERS"],
    #                                                        net_params["FILTER_SHAPE1"],
    #                                                        padding='VALID')
    #     print "conv1.1:", conv1.get_shape()
    #     conv1 = tf.nn.relu(conv1)
    #     print "conv1.2:", conv1.get_shape()
    #     pool1 = tf.nn.max_pool(conv1, ksize=[1, net_params["POOLING_WINDOW"], 1, 1],
    #         strides=[1, net_params["POOLING_STRIDE"], 1, 1], padding='SAME')
    #     print "pool1.1:", pool1.get_shape()
    #     pool1 = tf.transpose(pool1, [0, 1, 3, 2])
    #     print "pool1.2:", pool1.get_shape()
    #     # pool1 = skflow.ops.dropout(pool1, 0.5)
    #     # print "pool1.3:", pool1.get_shape()
    # print("---------------------------------------------")
    # with tf.variable_scope('CNN_Layer1_2'):
    #     conv3 = skflow.ops.conv2d(pool1, net_params["N_FILTERS"],
    #                               net_params["FILTER_SHAPE1"],
    #                               padding='VALID')
    #     print "conv3.1:", conv3.get_shape()
    #     conv3 = tf.nn.relu(conv3)
    #     print "conv3.2:", conv3.get_shape()
    #     pool3 = tf.nn.max_pool(conv3, ksize=[1, net_params["POOLING_WINDOW"], 1, 1],
    #         strides=[1, net_params["POOLING_STRIDE"], 1, 1], padding='SAME')
    #     print "pool3.1:", pool3.get_shape()
    #     pool3 = tf.transpose(pool3, [0, 1, 3, 2])
    #     print "pool3.2:", pool3.get_shape()
    #     # print dir(pool3.get_shape())
    #     # print type(pool3.get_shape())
    #     shape = pool3.get_shape().dims
    #     # print shape
    #     new_d2 = (shape[2] * shape[3]).value
    #     new_d1 = (shape[1]).value
    #     # print new_d2
    #     # print dir(new_d2)
    #     pool3 = tf.reshape(pool3, [-1, new_d1, new_d2])
    #     print "pool3.3:", pool3.get_shape()
    #     pool3 = tf.expand_dims(pool3, 3)
    #     print "pool3.4:", pool3.get_shape()
    #     # pool3 = skflow.ops.dropout(pool3, 0.5)
    #     # print "pool3.3:", pool3.get_shape()
    #
    # print("---------------------------------------------")
    # # with tf.variable_scope('CNN_Layer2'):
    # #     conv2 = skflow.ops.conv2d(pool3, net_params["N_FILTERS"],
    # #                               net_params["FILTER_SHAPE1"],
    # #                               padding='VALID')
    # #     print "conv2.1:", conv2.get_shape()
    # #     pool2 = tf.reduce_max(conv2, 1)
    # #     print "pool2.1:", pool2.get_shape()
    # #     pool2 = tf.squeeze(pool2, squeeze_dims=[1])
    # #     print "pool2.2:", pool2.get_shape()
    # out_pool = pool3
    out_pool = word_vectors
    shape = out_pool.get_shape().dims
    new_d1 = (shape[1] * shape[2] * shape[3]).value
    out_pool = tf.reshape(out_pool, [-1, new_d1])
    print "out_pool.1:", out_pool.get_shape()
    print("---------------------------------------------")
    fc1 = skflow.ops.dnn(out_pool, [200, 200, 200, 200, 200], keep_prob=0.5)
    # fc1 = skflow.ops.dnn(out_pool, [20, 20, 20], keep_prob=0.5)
    # fc1 = skflow.ops.dnn(pool2, [100], activation=tf.nn.relu, keep_prob=0.5)
    print "fc1.1:", fc1.get_shape()
    return skflow.models.logistic_regression(fc1, y)



if __name__ == '__main__':
    sample_size = 0
    min_class_size = 50
    test_sample_size = 0.1
    infile = "/media/sf_temp/func_class_items_texts2.json"

    all_data = pd.read_json(infile)
    # all_data = filter_rare_classes(all_data, class_field="category", min_class_size=100)
    if sample_size:
        data = all_data.sample(n=sample_size)
    else:
        data = all_data

    print(data["category"].value_counts())

    X = data["site_text"]
    y = data["category"]
    le = LabelEncoder()
    le.fit(y)
    y = le.transform(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y,
                            test_size=test_sample_size,
                            random_state=42)
    ### SVC bencmark
    clf = svm.LinearSVC(penalty='l2', dual=False)
    cnt_vect = CountVectorizer(min_df=0.001, max_df=0.99)
    tfidf_pipeline = Pipeline([('vect', cnt_vect),
                        ('tfidf', TfidfTransformer())])
    clf_pipeline = Pipeline([('tfidf', tfidf_pipeline),
                        ('clf', clf)])
    clf_pipeline = clf_pipeline.fit(X_train, y_train)
    y_test_pred = clf_pipeline.predict(X_test)
    print("Baseline test:")
    print(classification_report(y_test, y_test_pred))
    print("====================================================")
    X_train_tfidf = tfidf_pipeline.transform(X_train)
    X_test_tfidf = tfidf_pipeline.transform(X_test)
    print cnt_vect.vocabulary_
    print X_train_tfidf.shape
    print y_train.shape
    print X_test_tfidf.shape
    print y_test.shape
    X_train2 = X_train
    X_test2 = X_test
    X_train = X_train_tfidf.todense()
    X_test = X_test_tfidf.todense()
    # n_topics = X_train_tfidf.shape[0] * 2
    # nmf = NMF(n_components=n_topics,
    #           random_state=1,
    #           alpha=.1,
    #           l1_ratio=.5).fit(X_train_tfidf)
    # X_train = nmf.transform(X_train)
    ### Params

    MAX_DOCUMENT_LENGTH = 2000
    net_params["EMBEDDING_SIZE"] = 50
    net_params["N_FILTERS"] = 20
    net_params["WINDOW_SIZE"] = 5
    net_params["FILTER_SHAPE1"] = [net_params["WINDOW_SIZE"], 1]
    net_params["FILTER_SHAPE2"] = [net_params["WINDOW_SIZE"], net_params["N_FILTERS"]]
    net_params["POOLING_WINDOW"] = 4
    net_params["POOLING_STRIDE"] = 2

    opt_steps = 500
    opt_type = "Adam"
    opt_lr = 0.01
    opt_iterations = 10

    net_dir = "/media/sf_temp/cnn02/"
    log_dir = '/media/sf_temp/word_cnn'

    ### Model

    # vocab_processor = skflow.preprocessing.VocabularyProcessor(MAX_DOCUMENT_LENGTH)
    # X_train = np.array(list(vocab_processor.fit_transform(X_train)))
    # X_test = np.array(list(vocab_processor.transform(X_test)))
    #
    # n_words = len(vocab_processor.vocabulary_)
    # print('Total words: %d' % n_words)

    classifier = skflow.TensorFlowEstimator(model_fn=cnn_model,
                                            n_classes=len(le.classes_),
                                            steps=opt_steps,
                                            optimizer=opt_type,
                                            learning_rate=opt_lr,
                                            continue_training=True)

    classifier.fit(X_train, y_train, logdir=log_dir)
    classifier.save(net_dir)

    for i in range(opt_iterations):
        classifier.fit(X_train, y_train, logdir=log_dir)
        # y_train_pred = classifier.predict(X_train)
        print("starting prediction for test set")
        y_test_pred = classifier.predict(X_test)
        # print("Train:")
        # print(classification_report(y_train, y_train_pred))
        print("Test:")
        print(classification_report(y_test, y_test_pred))
        classifier.save(net_dir)
        print("Saved")

    # print("Completed")