#!/usr/bin/env python
# -*- coding: utf-8 -*-
# qw @ 2018-09-09 13:33:10

import sys
sys.path.append("./")

import logging
logging.basicConfig(level=logging.DEBUG)

import pickle
import multiprocessing

import numpy as np

from config.config import TREE_DEPTH
from config.config import N_ESTIMATORS
from config.config import TEST_DATA_SIZE_PERCENT
from config.config import COLUMN_SPLIT
from config.config import ITEM_SPLIT
from config.config import WORD_TO_VECTOR_MODEL_FILE_PATH

from read_skipgram_model import read_skipgram_model
word2vec_model = read_skipgram_model(WORD_TO_VECTOR_MODEL_FILE_PATH)

from word2vec import word2vec

from sklearn.externals import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

import xgboost as xgb

def transform_data(x_data_train, x_data_test):
    # source, fan_sum, uper_name, desc_keywords, title_keywords
    source_list_train = [line[0] for line in x_data_train]
    uper_name_list_train = [" ".join([w for w in line[2] if w]) for line in x_data_train]
    desc_keywords_list_train = [line[3] for line in x_data_train]
    title_keywords_list_train = [line[4] for line in x_data_train]

    source_list_test = [line[0] for line in x_data_test]
    uper_name_list_test = [" ".join([w for w in line[2] if w]) for line in x_data_test]
    desc_keywords_list_test = [line[3] for line in x_data_test]
    title_keywords_list_test = [line[4] for line in x_data_test]

    #uper_name_enc = OneHotEncoder()
    #uper_name_enc.fit(uper_name_list_train)
    
    source_label_enc = LabelEncoder()
    source_label_enc.fit(source_list_train)
    source_list_train = source_label_enc.transform(source_list_train)
    source_list_test = source_label_enc.transform(source_list_test)

    source_list_train = [[l, ] for l in source_list_train]
    source_list_test = [[l, ] for l in source_list_test]

    source_enc = OneHotEncoder()
    source_enc.fit(source_list_train)
    source_list_train = source_enc.transform(source_list_train).toarray()
    logging.info("source one line:%s" % source_list_train[0])
    source_list_test = source_enc.transform(source_list_test).toarray()

    #uper_name_list_train = uper_name_enc.transform(uper_name_list_train).toarray()

    #uper_name_list_test = uper_name_enc.transform(uper_name_list_test).toarray()

    desc_keywords_list_train = word2vec(desc_keywords_list_train, word2vec_model)
    logging.info("desc keyword one line:%s" % desc_keywords_list_train[0])
    desc_keywords_list_test = word2vec(desc_keywords_list_test, word2vec_model)
    title_keywords_list_train = word2vec(title_keywords_list_train, word2vec_model)
    logging.info("title keyword one line:%s" % title_keywords_list_train[0])
    title_keywords_list_test = word2vec(title_keywords_list_test, word2vec_model)

    x_train = np.concatenate((source_list_train, desc_keywords_list_train, title_keywords_list_train), axis=1)
    x_test = np.concatenate((source_list_test, desc_keywords_list_test, title_keywords_list_test), axis=1)

    return x_train, x_test


def main(file_path):
    new_file_path = file_path + ".w2v"
    lines = [line for line in open(file_path).readlines()]

    y_data = []
    x_data = []

    for line in lines:
        source, uper, label, uper_name, desc_keywords, fan_sum, title_keywords = line.decode("utf8").strip("\n").split(COLUMN_SPLIT) 
        y_data.append(label)
        x_data.append([source, fan_sum, uper_name, desc_keywords, title_keywords])
    logging.info("read file done")

    x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=TEST_DATA_SIZE_PERCENT, random_state=23) 
    x_train, x_test = transform_data(x_train, x_test)
    logging.info("split data to train and test done")

    gbdt = xgb.XGBClassifier(nthread=multiprocessing.cpu_count()/2 + 5, max_depth=TREE_DEPTH, learning_rate=0.001, n_estimators=N_ESTIMATORS, gamma=0,)
    #(n_jobs=24,learnning_rate=0.01,n_estimators=80,max_depth=5,gamma=0,)
    logging.info("please wait train")
    gbdt.fit(x_train,y_train)
    logging.info("model fit complete")

    y_pred_gbdt = gbdt.predict(np.array(x_test))
    with open("result", "w") as fw:
        fw.write(pickle.dumps(classification_report(y_test,y_pred_gbdt)))

    joblib.dump(gbdt,"model.gbdt")

    logging.info("add done")

if __name__ == "__main__":
    main(sys.argv[1])

"""
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

X_str = np.array([['a', 'dog', 'red'], ['b', 'cat', 'green']])
# transform to integer
X_int = LabelEncoder().fit_transform(X_str.ravel()).reshape(*X_str.shape)
# transform to binary
X_bin = OneHotEncoder().fit_transform(X_int).toarray()

print(X_bin)
# [[ 1.  0.  0.  1.  0.  1.]
#  [ 0.  1.  1.  0.  1.  0.]]
"""
