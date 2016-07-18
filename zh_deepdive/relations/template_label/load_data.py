# coding: utf-8
import sys
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
def main(in_file):

    pos_count = 0
    neg_count = 0

    P = unicode(this_P)
    num_neagtive = 100000

    with open(in_file) as fin, \
        open("input/sentence.tsv", "w") as fout_sentence, \
        open("input/so_mention.tsv", "w") as fout_mention, \
        open("input/so_candidate.tsv", "w") as fout_candidate, \
        open("input/so_label.tsv", "w") as fout_label:

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

                #  正例
                if label > 0:

                    pos_count += 1

                    wanted = True
                    # so_candidate.tsv
                    fout_candidate.write("%s\t%s\t%s\t%s\n" % (S_id, S_text, O_id, O_text))
                    # so_label.tsv
                    fout_label.write("%s\t%s\t%d\t%s\n" % (S_id, O_id, 1, rule_ids))


                if label < 0 and num_neagtive > 0:
                    wanted = True
                    neg_count += 1
                    # so_candidate.tsv
                    fout_candidate.write("%s\t%s\t%s\t%s\n" % (S_id, S_text, O_id, O_text))
                    # so_label.tsv
                    fout_label.write("%s\t%s\t%d\t%s\n" % (S_id, O_id, -1, rule_ids))

                    num_neagtive -= 1

            if wanted:
                fout_sentence.write(line)
                # [["4fbe2704-4c01-11e6-bcf6-089e016c1d80_17_17", "日本", "4fbe2704-4c01-11e6-bcf6-089e016c1d80", 17, 17], ["4fbe2704-4c01-11e6-bcf6-089e016c1d80_14_14", "饶宗颐", "4fbe2704-4c01-11e6-bcf6-089e016c1d80", 14, 14]]
                mentions = [map(str, mention) for mention in mentions]
                fout_mention.write("\n".join(["\t".join(mention) for mention in mentions]) + "\n")

        print "positive vs negative: %d vs %d" % (pos_count, neg_count)

        fout = open("input/label.log", "w")
        fout.write("positive vs negative: %d vs %d\n" % (pos_count, neg_count))
        fout.close()

if __name__ == '__main__':
    main("/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/SPO_train_data_for_deepdive_label")









