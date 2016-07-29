#!/usr/bin/env python
# coding: utf-8
import sys

import pyprind

reload(sys)
sys.setdefaultencoding('utf-8')
import codecs, json

def load_train_data(in_file, to_file, statistics_file):

    dict_P_to_count = {}

    NUM_NEAGTIVE = 100000

    process_bar = pyprind.ProgPercent(1175207)
    with open(in_file) as fin, \
         open(to_file, "w") as fout:

        for line in fin:
            process_bar.update()

            sent_id, sent_text, tokens, pos_tags, ner_tags, dep_types, dep_tokens,\
            S_O, dict_label_info = line.strip().split("\t")

            dict_label_info = json.loads(dict_label_info)

            # 加载每个P的正负样本:
            for P in dict_label_info:

                if P not in dict_P_to_count:
                    dict_P_to_count[P] = {}
                    dict_P_to_count[P]["positive"] = 0
                    dict_P_to_count[P]["negative"] = 0

                for s_o in dict_label_info[P]["candidates"]:
                    S_id, S_text, O_id, O_text = s_o.split("|~|")
                    label = dict_label_info[P]["candidates"][s_o]["label"]

                    #  正例
                    if label > 0:
                        dict_P_to_count[P]["positive"] += 1
                        fout.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (sent_text, S_text, P, O_text, "1", line.strip()))


                    if label < 0 and dict_P_to_count[P]["negative"] < NUM_NEAGTIVE:
                        dict_P_to_count[P]["negative"] += 1
                        fout.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (sent_text, S_text, P, O_text, "-1", line.strip()))

    with open(statistics_file, "w") as fout:
        for P in dict_P_to_count:
            fout.write("%s\t%d\t%d\n" % (P, dict_P_to_count[P]["positive"], dict_P_to_count[P]["negative"]))


if __name__ == '__main__':
    # load_train_data("/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/SPO_train_data_for_deepdive_label")
    load_train_data(
        "/home/disk2/wangjianxiang01/downloads/SPO_train_data_84P_for_deepdive_label_1w_pos_5w_neg.head1000",
        "/home/disk2/wangjianxiang01/downloads/SPO_train_data_84P_for_deepdive_label_1w_pos_10w.spo.sent",
        "/home/disk2/wangjianxiang01/downloads/SPO_train_data_84P_for_deepdive_label_1w_pos_10w.spo.sent.statistics",
    )








