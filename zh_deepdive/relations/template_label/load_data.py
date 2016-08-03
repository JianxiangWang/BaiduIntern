#!/usr/bin/env python
# coding: utf-8
import sys

import pyprind

reload(sys)
sys.setdefaultencoding('utf-8')
import codecs, json


# 读取当前P
fin = open("P")
this_P = fin.read().strip()
fin.close()

# print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
#                 sent_id, sent_sent, tokens, pos_tags, ner_tags, dep_types, dep_tokens, S_O,
#                 json.dumps(dict_label_info, ensure_ascii=False)
#             )
def load_train_data(in_file):

    pos_count = 0
    neg_count = 0

    P = unicode(this_P)
    NUM_NEAGTIVE = 100000

    print "==" * 20
    print "\t%s" % P
    print "==" * 20

    print "load train data..."

    process_bar = pyprind.ProgPercent(1175207)
    with open(in_file) as fin, \
        open("input/sentence.tsv", "w") as fout_sentence, \
        open("input/so_mention.tsv", "w") as fout_mention, \
        open("input/so_candidate.tsv", "w") as fout_candidate, \
        open("input/so_label.tsv", "w") as fout_label:

        for line in fin:
            process_bar.update()

            sent_id, sent_sent, tokens, pos_tags, ner_tags, dep_types, dep_tokens,\
            S_O, dict_label_info = line.strip().split("\t")

            dict_label_info = json.loads(dict_label_info)
            # 句子没有当前P的候选集合
            if P not in dict_label_info:
                continue

            # 如果有
            wanted = False
            mentions = dict_label_info[P]["mentions"]

            for s_o in dict_label_info[P]["candidates"]:
                S_id, S_text, O_id, O_text = s_o.split("|~|")
                label = dict_label_info[P]["candidates"][s_o]["label"]
                rule_ids = "&".join(
                    [rule for _, rule, _ in dict_label_info[P]["candidates"][s_o]["label_info"]])

                #  正例
                if label > 0:

                    pos_count += 1

                    wanted = True
                    # so_candidate.tsv
                    fout_candidate.write("%s\t%s\t%s\t%s\n" % (S_id, S_text, O_id, O_text))
                    # so_label.tsv
                    fout_label.write("%s\t%s\t%d\t%s\n" % (S_id, O_id, 1, rule_ids))

                    print "\r==> positive: %d; negative: %d" % (pos_count, neg_count),


                if label < 0 and NUM_NEAGTIVE > 0:
                    wanted = True
                    neg_count += 1
                    # so_candidate.tsv
                    fout_candidate.write("%s\t%s\t%s\t%s\n" % (S_id, S_text, O_id, O_text))
                    # so_label.tsv
                    fout_label.write("%s\t%s\t%d\t%s\n" % (S_id, O_id, -1, rule_ids))

                    print "\r==> positive: %d; negative: %d" % (pos_count, neg_count),

                    NUM_NEAGTIVE -= 1

            if wanted:
                fout_sentence.write(line)
                # [["4fbe2704-4c01-11e6-bcf6-089e016c1d80_17_17", "日本", "4fbe2704-4c01-11e6-bcf6-089e016c1d80", 17, 17], ["4fbe2704-4c01-11e6-bcf6-089e016c1d80_14_14", "饶宗颐", "4fbe2704-4c01-11e6-bcf6-089e016c1d80", 14, 14]]
                mentions = [map(str, mention) for mention in mentions]
                fout_mention.write("\n".join(["\t".join(mention) for mention in mentions]) + "\n")

        print "\r==> positive: %d; negative: %d" % (pos_count, neg_count)

        fout = open("input/label.log", "w")
        fout.write("train positive vs negative: %d vs %d\n" % (pos_count, neg_count))
        fout.close()


def load_test_data(in_file):

    num = 0

    P = unicode(this_P)

    print "load test data..."

    with open(in_file) as fin, \
        open("input/sentence.tsv", "a") as fout_sentence, \
        open("input/so_mention.tsv", "a") as fout_mention, \
        open("input/so_candidate.tsv", "a") as fout_candidate, \
        open("input/so_label.tsv", "a") as fout_label:

        for line in fin:

            sent_id, sent_sent, tokens, pos_tags, ner_tags, dep_types, dep_tokens,\
            S_O, dict_label_info = line.strip().split("\t")

            dict_label_info = json.loads(dict_label_info)
            # 句子没有当前P的候选集合
            if P not in dict_label_info:
                continue

            # 如果有
            wanted = False
            mentions = dict_label_info[P]["mentions"]

            for s_o in dict_label_info[P]["candidates"]:
                S_id, S_text, O_id, O_text = s_o.split("|~|")
                label = dict_label_info[P]["candidates"][s_o]["label"]
                rule_ids = "&".join(
                    [rule for _, rule, _ in dict_label_info[P]["candidates"][s_o]["label_info"]])

                wanted = True
                # so_candidate.tsv
                fout_candidate.write("%s\t%s\t%s\t%s\n" % (S_id, S_text, O_id, O_text))
                # so_label.tsv
                fout_label.write("%s\t%s\t%d\t%s\n" % (S_id, O_id, -1, rule_ids))

                num += 1

                print "\r==> test: %d" % (num),

            if wanted:
                fout_sentence.write(line)
                # [["4fbe2704-4c01-11e6-bcf6-089e016c1d80_17_17", "日本", "4fbe2704-4c01-11e6-bcf6-089e016c1d80", 17, 17], ["4fbe2704-4c01-11e6-bcf6-089e016c1d80_14_14", "饶宗颐", "4fbe2704-4c01-11e6-bcf6-089e016c1d80", 14, 14]]
                mentions = [map(str, mention) for mention in mentions]
                fout_mention.write("\n".join(["\t".join(mention) for mention in mentions]) + "\n")

        print ("test: %d\n" % num)
        fout = open("input/label.log", "a")
        fout.write("test: %d\n" % (num))
        fout.close()

if __name__ == '__main__':
    # load_train_data("/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/SPO_train_data_for_deepdive_label")
    load_train_data("/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/SPO_train_data_84P_for_deepdive_label_1w_pos_5w_neg")
    load_test_data("/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/SPO_test_data_84P_for_deepdive_label_new_data_new_so")








