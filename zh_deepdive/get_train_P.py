# coding: utf-8
import json
import sys,codecs
import cPickle
reload(sys)
sys.setdefaultencoding('utf-8')
import codecs
import csv
import os


#[{'first_name': 'Baked', 'last_name': 'Beans'}, {'first_name': 'Lovely', 'last_name': 'Spam'}]
def read_dict_from_csv(in_file):
    if not os.path.exists(in_file):
        return []
    with codecs.open(in_file, "r") as csvfile:
        return list(csv.DictReader(csvfile))




dict_pinyin_to_hanzi = {}
for d in read_dict_from_csv("data/全网SPO挖掘通用领域P梳理文档2.csv"):
    P_hanzi = d["领域"] + "_" + d["P"]
    P_pinyin = d["拼音"]
    dict_pinyin_to_hanzi[P_pinyin] = P_hanzi


with open("data/62P.output") as fin,\
     open("data/train_P.txt", "w") as fout:
    train_P_list = []
    for line in fin:
        pinyin = line.strip()
        train_P_list.append(dict_pinyin_to_hanzi[pinyin])


    fout.write("\n".join(sorted(train_P_list)))
