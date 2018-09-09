#!/usr/bin/env python
# -*- coding: utf-8 -*-
# qw @ 2018-09-09 13:33:10

import sys
sys.path.append("./")

import pickle

from config.config import COLUMN_SPLIT
from config.config import ITEM_SPLIT
from config.config import WORD_TO_VECTOR_MODEL_FILE_PATH

from read_skipgram_model import read_skipgram_model.py
word2vec_model = read_skipgram_model(WORD_TO_VECTOR_MODEL_FILE_PATH)

from word2vec import word2vec

from sklearn.externals import joblib
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import classification_report

import xgboost as xgb

def transform_data(x_data_train, x_data_test):
    # source, fan_sum, uper_name, desc_keywords, title_keywords
    source_list_train = [line[0] for line in x_data_train]
    uper_name_list_train = [" ".join([w for w in line[2] if w]) for line in x_data_train]
    desc_keywords_list_train = [line[3] for line in x_data_train]
    title_keywords_list_train = [line[4] for line in x_data_train]

    source_list_test = [line[:2] for line in x_data_test]
    uper_name_list_test = [" ".join([w for w in line[2] if w]) for line in x_data_test]
    desc_keywords_list_test = [line[3] for line in x_data_test]
    title_keywords_list_test = [line[4] for line in x_data_test]

    uper_name_enc = OneHotEncoder()
    uper_name_enc.fit(uper_name_list_train)

    source_enc = OneHotEncoder()
    source_enc.fit(source_list_train)

    source_list_train = source_enc.transform(source_list_train).toarray()
    uper_name_list_train = uper_name_enc.transform(uper_name_list_train).toarray()

    source_list_test = source_enc.transform(source_list_test).toarray()
    uper_name_list_test = uper_name_enc.transform(uper_name_list_test).toarray()

    desc_keywords_list_train, desc_keywords_list_test = word2vec(desc_keywords_list_train, desc_keywords_list_test)
    title_keywords_list_train, title_keywords_list_test = word2vec(title_keywords_list_train, title_keywords_list_test)

    x_train = np.concatenate(source_list_train, uper_name_list_train, desc_keywords_list_train, title_keywords_list_train)
    x_test = np.concatenate(source_list_test, uper_name_list_test, desc_keywords_list_test, title_keywords_list_test)

    return x_train, x_test


def main(file_path):
    new_file_path = file_path + ".w2v"
    lines = [line.strip() for line in open(file_path).readlines()]

    y_data = []
    x_data = []

    for line in lines:
        source, uper, label, uper_name, desc_keywords, fan_sum, title_keywords = line.decode("utf8").strip("\n").split(COLUMN_SPLIT) 
        y_data.append(label)
        x_data.append(source, fan_sum, uper_name, desc_keywords, title_keywords)

    x_train, x_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.3,random_state=23) 
    x_tran, x_test = transform_data(x_tran, x_test)

    gbdt = xgb.XGBClassifier(nthread=24,max_depth=10,learning_rate=0.001,n_estimators=100,gamma=0,)
    #(n_jobs=24,learnning_rate=0.01,n_estimators=80,max_depth=5,gamma=0,)
    gbdt.fit(x_train,y_train)
    joblib.dump(gbdt,"model.gbdt")
    y_pred_gbdt = gbdt.predict(np.array(X_test))
    with open("result", "w") as fw:
        fw.write(pickle.dumps(classification_report(y_test_pre,y_pred_gbdt)))

