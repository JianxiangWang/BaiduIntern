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



def get_62_P_list():

    dict_pinyin_to_hanzi = {}
    for d in read_dict_from_csv("data/全网SPO挖掘通用领域P梳理文档2.csv"):
        P_hanzi = d["领域"] + "_" + d["P"]
        P_pinyin = d["拼音"]
        dict_pinyin_to_hanzi[P_pinyin] = P_hanzi

    train_P_list = []
    with open("data/62P.output") as fin:
        for line in fin:
            pinyin = line.strip()
            train_P_list.append(dict_pinyin_to_hanzi[pinyin])
    return sorted(train_P_list)


def get_22_P_list():

    P_list = []
    with open("data/22.bag_of_word.dict") as fin:
        for line in fin:
            P_list.append("人物_" + line.strip().split("\t")[0])

    return sorted(P_list)

def get_ALL_P_List(to_file):
    P_List = get_62_P_list() + get_22_P_list()

    fout = open(to_file, "w")
    fout.write("\n".join(P_List))
    fout.close()

if __name__ == '__main__':
    get_ALL_P_List("data/train_all_P.txt")
