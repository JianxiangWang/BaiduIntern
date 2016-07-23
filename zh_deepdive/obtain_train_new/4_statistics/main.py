# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json, pyprind
from collections import Counter


def main(in_file, to_file):

    count = {}

    process_bar = pyprind.ProgPercent(3500000)
    for line in open(in_file):
        process_bar.update()

        label_info = json.loads(line.split("\t")[-1])

        for P in label_info:

            if P not in count:
                count[P] = Counter()

            for so in label_info[P]["candidates"]:

                label = label_info[P]["candidates"][so]["label"]

                if label > 0:
                    count[P]["positive"] += 1
                if label < 0:
                    count[P]["negative"] += 1
                if label == 0:
                    count[P]["NULL"] += 1



    fout = open(to_file, "w")
    fout.write("P,positive,negative,NULL\n")
    for P in sorted(count.keys()):
        fout.write("%s,%d,%d,%d\n" % (P, count[P]["positive"], count[P]["negative"], count[P]["NULL"]) )
    fout.close()


if __name__ == '__main__':

    # main("../../data/SPO_train_data_for_deepdive_label", "../../data/SPO_train_data_for_deepdive_label.statistics.csv")
    # main("../../data/SPO_test_data_for_deepdive_label", "../../data/SPO_test_data_for_deepdive_label.statistics.csv")
    # main("../4_filte_sentences_label/SPO_train_data_for_deepdive_label", "../4_filte_sentences_label/SPO_test_data_for_deepdive_label.statistics.csv")
    # main("../../data/SPO_train_data_for_deepdive_label_sample", "../../data/SPO_train_data_for_deepdive_label_sample.statistics.csv")
    # main("../../data/SPO_train_data_for_deepdive_label_post_processing", "../../data/SPO_train_data_for_deepdive_label_post_processing.statistics.csv")
    # main("../../data/SPO_train_data_for_deepdive_label.new.post_processing_new_rule_score", "../../data/SPO_train_data_for_deepdive_label.new.post_processing_new_rule_score.statistics.csv")

    # main("/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/SPO_train_data_84P_for_deepdive_label",
    #      "/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/SPO_train_data_84P_for_deepdive_label.statistics.csv")

    # main("/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/SPO_train_data_84P_for_deepdive_label_top_250w",
    #      "/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/SPO_train_data_84P_for_deepdive_label_top_250w.statistics.csv")

    # main("/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/SPO_train_data_84P_for_deepdive_label_random.0.2",
    #      "/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/SPO_train_data_84P_for_deepdive_label_random.0.2.statistics.csv")

    # main("/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/SPO_train_data_84P_for_deepdive_label_1w_pos_20w_neg",
    #          "/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/SPO_train_data_84P_for_deepdive_label_1w_pos_20w_neg.statistics.csv")

    main("/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/SPO_train_data_84P_for_deepdive_label_all_pos_20w_neg",
             "/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/SPO_train_data_84P_for_deepdive_label_all_pos_20w_neg.statistics.csv")
