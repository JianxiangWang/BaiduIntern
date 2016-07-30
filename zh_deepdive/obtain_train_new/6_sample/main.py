# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json, pyprind
from collections import Counter
import random

import pyprind


def get_top_n(in_file, N, to_file):

    with open(in_file) as fin, \
         open(to_file, "w") as fout:

        for line in fin:
            if N > 0:
                fout.write(line)
            else:
                break
            N -= 1


def get_random(in_file, p, to_file):

    process_bar = pyprind.ProgPercent(12440969)
    with open(in_file) as fin, \
         open(to_file, "w") as fout:

        for line in fin:
            process_bar.update()
            if random.random() < p:
                fout.write(line)


# 获取所有的正样本, 20w的负样本
def get_all_positive_20wNegative(in_file, to_file):

    fout = open(to_file, "w")

    count = {}
    process_bar = pyprind.ProgPercent(12440969)
    for line in open(in_file):
        process_bar.update()

        wanted = False
        label_info = json.loads(line.split("\t")[-1])

        for P in label_info:

            if P not in count:
                count[P] = {}
                count[P]["positive"] = 0
                count[P]["negative"] = 0
                count[P]["NULL"] = 0

            for so in label_info[P]["candidates"]:

                label = label_info[P]["candidates"][so]["label"]

                if label > 0:
                    wanted = True
                    count[P]["positive"] += 1

                if label < 0 and count[P]["negative"] < 200000 :
                    wanted = True
                    count[P]["negative"] += 1

                if label == 0:
                    count[P]["NULL"] += 1

        if wanted:
            fout.write(line)

    fout.close()


# 获取 1w 正样本, 5w的负样本
def get_1w_positive_5w_negative(in_file, to_file):

    fout = open(to_file, "w")

    count = {}
    process_bar = pyprind.ProgPercent(3500000)
    for line in open(in_file):
        process_bar.update()

        wanted = False
        label_info = json.loads(line.split("\t")[-1])

        for P in label_info:

            if P not in count:
                count[P] = {}
                count[P]["positive"] = 0
                count[P]["negative"] = 0
                count[P]["NULL"] = 0

            for so in label_info[P]["candidates"]:

                label = label_info[P]["candidates"][so]["label"]

                if label > 0 and count[P]["positive"] < 10000 :
                    wanted = True
                    count[P]["positive"] += 1

                if label < 0 and count[P]["negative"] < 50000 :
                    wanted = True
                    count[P]["negative"] += 1

                if label == 0:
                    count[P]["NULL"] += 1

        if wanted:
            fout.write(line)

    fout.close()




if __name__ == '__main__':
    # get_top_n(
    #     "/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/SPO_train_data_84P_for_deepdive_label",
    #     2500000,
    #     "/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/SPO_train_data_84P_for_deepdive_label_top_250w",
    # )

    # get_random(
    #     "/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/SPO_train_data_84P_for_deepdive_label",
    #     0.2,
    #     "/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/SPO_train_data_84P_for_deepdive_label_random.0.2",
    # )

    get_all_positive_20wNegative(
        "/home/disk2/wangjianxiang01/BaiduIntern/zh_deepdive/obtain_train_new/3_filte_sentences_label/SPO_train_data_84P_for_deepdive_label_lihe",
        "/home/disk2/wangjianxiang01/BaiduIntern/zh_deepdive/obtain_train_new/3_filte_sentences_label/SPO_train_data_84P_for_deepdive_label_lihe_all_pos_20w_neg",
    )

    get_1w_positive_5w_negative(
        "/home/disk2/wangjianxiang01/BaiduIntern/zh_deepdive/obtain_train_new/3_filte_sentences_label/SPO_train_data_84P_for_deepdive_label_lihe_all_pos_20w_neg",
        "/home/disk2/wangjianxiang01/BaiduIntern/zh_deepdive/obtain_train_new/3_filte_sentences_label/SPO_train_data_84P_for_deepdive_label_lihe_1w_pos_5w_neg"
    )