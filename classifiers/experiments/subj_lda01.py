# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import json
import nltk
from gensim.corpora import Dictionary
from gensim.utils import tokenize
from gensim.models.ldamodel import LdaModel
from gensim.models.ldamulticore import LdaMulticore


def get_tokens(data):
    stopwords = set(nltk.corpus.stopwords.words("english"))
    # stopwords = set([])
    tokens = []
    for text_item in data:
        toks = tokenize(text_item,
                        lowercase=True,
                        deacc=True,
                        errors="ignore")
        ltokens = []
        for token in toks:
            if token not in stopwords:
                ltokens.append(token)
        tokens.append(ltokens)
    # dict = Dictionary(tokens.values())
    return tokens


def train(data, topics=10, iterations=100):
    tokens = get_tokens(data)
    text_dict = Dictionary(tokens)
    corpus = [text_dict.doc2bow(text) for text in tokens]
    lda = LdaModel(corpus=corpus,
                   num_topics=topics,
                   id2word=text_dict,
                   )
    # lda = LdaMulticore(corpus=corpus,
    #                    id2word=text_dict,
    #                    num_topics=topics,
    #                    chunksize=10000,
    #                    passes=1,
    #                    iterations=iterations,
    #                    workers=1)
    # model = lda.LDA(n_topics=20, n_iter=500, random_state=1)
    # model.fit(X)
    # lh = lda.log_perplexity(corpus)
    return lda


if __name__ == '__main__':
    sample_size = 500
    min_class_size = 50
    # train by description
    infile = "/media/sf_temp/items_dmoz_5.json"
    X_name = "description"
    # train by site page
    infile = "/media/sf_temp/items_dmoz_6_sample.json"
    X_name = "page_text"


    all_data = pd.read_json(infile)
    if sample_size:
        data = all_data.sample(n=sample_size)
    else:
        data = all_data

    # filter out rare classes
    y_cnt = data["category1"].value_counts()
    y_take = y_cnt.index[y_cnt > min_class_size]
    data = data[data["category1"].isin(y_take)]
    print data

    X = data[X_name]
    y = data["category1"]
    num_topics = len(y_cnt)
    lda_model = train(X, topics=num_topics)
    print lda_model
    topics = lda_model.print_topics(num_topics=num_topics,
                 num_words=15)
    print topics

