#!/usr/bin/env python
# -*- coding: utf-8 -*-
# qw @ 2018-09-08 23:22:31

import sys
sys.path.append("./")

from config.config import COLUMN_SPLIT
from config.config import ITEM_SPLIT

import jieba
import jieba.analyse

import multiprocessing

def cutword_function(parameter):
    line, return_list = parameter
    line = line.strip().decode("utf8")
    source, uper, label, uper_name, uper_description, fan_sum, title_string = \
        line.split(COLUMN_SPLIT)
    desc_keywords = jieba.analyse.textrank(
            uper_description,
            topK=10, 
            withWeight=True, 
            allowPOS=('ns', 'n', 'vn', 'v'))
    title_keywords = jieba.analyse.textrank(
            title_string,
            topK=30, 
            withWeight=True, 
            allowPOS=('ns', 'n', 'vn', 'v'))
    line = [
        source, uper, label, 
        uper_name, " ".join([word for word,weight in desc_keywords if weight > 0.1]),
        fan_sum, " ".join([word for word,weight in title_keywords if weight > 0.2])]
    return_list.append(ITEM_SPLIT.join(line).encode("utf8"))

def curword(file_path):
    new_file_path = file_path + ".cutword"
    pool = multiprocessing.Pool(multiprocessing.cpu_count() * 2)
    wait_write_list = multiprocessing.Manager().list()
    lines = [[line.strip(), wait_write_list] for line in open(file_path).readlines()]
    pool.map_async(cutword_function, lines)
    pool.close()
    pool.join()
   
    with open(new_file_path, "w") as fw:
        for line in wait_write_list:
            fw.write(line + "\n")

if __name__ == "__main__":
    curword(sys.argv[1])


