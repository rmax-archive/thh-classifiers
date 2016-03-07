# -*- coding: utf-8 -*-
from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import train_test_split
import pandas as pd
import numpy as np
import skflow
import tensorflow as tf
from sklearn import metrics

from mcc.utils import filter_rare_classes


def cnn_model(X, y):
    """2 layer Convolutional network to predict from sequence of words
    to a class."""
    # Convert indexes of words into embeddings.
    # This creates embeddings matrix of [n_words, EMBEDDING_SIZE] and then
    # maps word indexes of the sequence into [batch_size, sequence_length,
    # EMBEDDING_SIZE].
    word_vectors = skflow.ops.categorical_variable(X, n_classes=n_words,
        embedding_size=EMBEDDING_SIZE, name='words')
    word_vectors = tf.expand_dims(word_vectors, 3)
    with tf.variable_scope('CNN_Layer1'):
        # Apply Convolution filtering on input sequence.
        conv1 = skflow.ops.conv2d(word_vectors, N_FILTERS, FILTER_SHAPE1, padding='VALID')
        # Add a RELU for non linearity.
        conv1 = tf.nn.relu(conv1)
        # Max pooling across output of Convlution+Relu.
        pool1 = tf.nn.max_pool(conv1, ksize=[1, POOLING_WINDOW, 1, 1],
            strides=[1, POOLING_STRIDE, 1, 1], padding='SAME')
        # Transpose matrix so that n_filters from convolution becomes width.
        pool1 = tf.transpose(pool1, [0, 1, 3, 2])
    with tf.variable_scope('CNN_Layer2'):
        # Second level of convolution filtering.
        conv2 = skflow.ops.conv2d(pool1, N_FILTERS, FILTER_SHAPE2,
            padding='VALID')
        # Max across each filter to get useful features for classification.
        pool2 = tf.squeeze(tf.reduce_max(conv2, 1), squeeze_dims=[1])
    # Apply regular WX + B and classification.
    return skflow.models.logistic_regression(pool2, y)



if __name__ == '__main__':
    sample_size = 0
    min_class_size = 50
    test_sample_size = 0.3
    infile = "/media/sf_temp/func_class_items_texts.json"

    all_data = pd.read_json(infile)
    # all_data = filter_rare_classes(all_data, class_field="category", min_class_size=100)
    if sample_size:
        data = all_data.sample(n=sample_size)
    else:
        data = all_data

    print data["category"].value_counts()

    X = data["site_text"]
    y = data["category"]
    le = LabelEncoder()
    le.fit(y)
    y = le.transform(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y,
                            test_size=test_sample_size, random_state=42)

    ### Process vocabulary

    MAX_DOCUMENT_LENGTH = 3000

    vocab_processor = skflow.preprocessing.VocabularyProcessor(MAX_DOCUMENT_LENGTH)
    X_train = np.array(list(vocab_processor.fit_transform(X_train)))
    X_test = np.array(list(vocab_processor.transform(X_test)))

    n_words = len(vocab_processor.vocabulary_)
    print('Total words: %d' % n_words)

    ### Models

    EMBEDDING_SIZE = 20
    N_FILTERS = 10
    WINDOW_SIZE = 20
    FILTER_SHAPE1 = [WINDOW_SIZE, EMBEDDING_SIZE]
    FILTER_SHAPE2 = [WINDOW_SIZE, N_FILTERS]
    POOLING_WINDOW = 4
    POOLING_STRIDE = 2


    classifier = skflow.TensorFlowEstimator(model_fn=cnn_model, n_classes=15,
        steps=100, optimizer='Adam', learning_rate=0.01, continue_training=True)
    classifier.fit(X_train, y_train, logdir='/tmp/tf_examples/word_cnn')
    classifier.save("/media/sf_temp/cnn02/")

    while True:
        classifier.fit(X_train, y_train, logdir='/tmp/tf_examples/word_cnn')
        score = metrics.accuracy_score(y_test, classifier.predict(X_test))
        print('Accuracy: {0:f}'.format(score))
        classifier.save("/media/sf_temp/cnn02/")
        print("Saved")

    # print("Completed")