#!/usr/bin/env python
# -*- coding: utf-8 -*-
# qw @ 2018-09-09 13:51:52

import sys
sys.path.append("./")

from gensim import models

def read_skipgram_model(file_path):
    return models.keyedvectors.KeyedVectors.load_word2vec_format(file_path,binary=True, unicode_errors='ignore')
