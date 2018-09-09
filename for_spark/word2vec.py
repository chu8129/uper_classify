#!/usr/bin/env python
# -*- coding: utf-8 -*-
# qw @ 2018-09-09 13:49:36

import sys
sys.path.append("./")

import numpy as np

def word2vec(text_data, w2v_model, size=300):
    """将文本转为词向量形式
        异常处理：当句子中词汇在词向量库中均不存在，用1向量代替"""
    global count_zero_keyword_count
    word2vec_list = []
    for each_sen in text_data:
        sum_array = np.zeros(size)
        cnt = 0.0
        for j in each_sen.split(' '):
            word = j
            if word in w2v_model:
                sum_array += np.array(w2v_model[word])# 平移，满足bayes输入不能小于0
                cnt += 1.0
            else:
                pass
        if cnt == 0.0:
            word2vec_list.append(np.ones(300))
        else:
            word2vec_list.append(sum_array)#/cnt)
    return word2vec_list
