#!/usr/bin/env python
# -*- coding: utf-8 -*-
# qw @ 2018-09-08 22:33:49

import sys
sys.path.append("./")

import json
import pickle
import base64

from config.config import COLUMN_SPLIT
from config.config import ITEM_SPLIT

def format_data(file_path):
    new_file_path = file_path + ".spark"
    with open(file_path) as fr:
        with open(new_file_path, "w") as fw:
            while 1:
                line = fr.readline()
                if line == "":
                    break
                line = json.loads(line.strip())
                source = line["source"]
                uper = line["id"]
                label = line["label"]
    
                profile = pickle.loads(base64.b64decode(line["profile"]))
                if profile:
                    pass
                else:
                    continue
                uper_name = profile[0]["uper_name"]
                uper_description = profile[0]["uper_description"]
                fan_sum = str(profile[0]["fan_sum"])
                
                videos = pickle.loads(base64.b64decode(line["videos"]))
                titles = []
                for video in videos:
                    title = video["video_title"]
                    if title:
                        titles.append(title)
                title_string  = ITEM_SPLIT.join(titles)
    
                new_line = COLUMN_SPLIT.join(
                    [source, uper, label, uper_name, uper_description, fan_sum, title_string]
                    ).encode("utf8").replace("\n", " \\n ")
    
                fw.write(new_line + "\n")

if __name__ == "__main__":
    format_data(sys.argv[1])



