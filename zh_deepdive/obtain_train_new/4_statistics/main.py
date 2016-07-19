# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from collections import Counter


def main(in_file, to_file):

    count = {}

    for line in open(in_file):
        label_info = json.loads(line.split("\t")[-1])

        for P in label_info:

            if P not in count:
                count[P] = Counter()

            for so in label_info[P]["candidates"]:
                label_rules = label_info[P]["candidates"][so]["label_info"]

                pos_exist = False
                neg_far_apart_exist = False

                label = 0
                for x, rule, _ in label_rules:
                    label += x
                    if rule.startswith("pos"):
                        pos_exist = True
                    if rule == "neg:far_apart":
                        neg_far_apart_exist = True

                    # if rule == "neg: from seeds" or rule == "pos: from seeds":
                    #     print P, so

                # 有pos了,那么neg: far apart 就不算了
                if pos_exist and neg_far_apart_exist:
                    label += 1

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
    main("../../data/SPO_test_data_for_deepdive_label", "../../data/SPO_test_data_for_deepdive_label.statistics.csv")
