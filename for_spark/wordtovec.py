#!/usr/bin/env python
# -*- coding: utf-8 -*-
# qw @ 2018-09-09 13:33:10

import sys
sys.path.append("./")

def wordtovec(file_path):
    new_file_path = file_path + ".w2v"
    lines = [line.strip() for line in open(file_path).readlines()]
    
