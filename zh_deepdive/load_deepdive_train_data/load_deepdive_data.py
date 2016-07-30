#!tools/python/bin/python
# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import codecs
import ujson
import pyprind

def load_train_data(in_file, to_file, statistics_file):

    dict_P_to_count = {}

    NUM_NEAGTIVE = 100000

    process_bar = pyprind.ProgPercent(1175201)
    with open(in_file) as fin, \
         open(to_file, "w") as fout:

        for line in fin:
            process_bar.update()

            sent_id, sent_text, tokens, pos_tags, ner_tags, dep_types, dep_tokens,\
            S_O, dict_label_info_string = line.strip().split("\t")

            dict_label_info = ujson.loads(dict_label_info_string)

            # 过滤一下SO识别
            dict_so = ujson.loads(S_O)
            dict_so_new = {}
            for P in dict_so:
                if P in dict_label_info:
                    dict_so_new[P] = dict_so[P]
            dict_so_new_string = ujson.dumps(dict_so_new, ensure_ascii=False)


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

                        S_position = "|_|".join(S_id.split("_")[-2:])
                        O_position = "|_|".join(O_id.split("_")[-2:])
                        out_line = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (sent_text,
                                                                   S_text+"|_|" + S_position,
                                                                   P,
                                                                   O_text+"|_|" + O_position,
                                                                   "1",
                                                                    tokens,
                                                                    dict_so_new_string,
                                                                    dict_label_info_string,

                                                                 )

                        fout.write("%s\n" % out_line)


                    if label < 0 and dict_P_to_count[P]["negative"] < NUM_NEAGTIVE:
                        dict_P_to_count[P]["negative"] += 1

                        S_position = "|_|".join(S_id.split("_")[-2:])
                        O_position = "|_|".join(O_id.split("_")[-2:])
                        out_line = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (sent_text,
                                                                   S_text+"|_|" + S_position,
                                                                   P,
                                                                   O_text+"|_|" + O_position,
                                                                   "-1",
                                                                   tokens,
                                                                   dict_so_new_string,
                                                                   dict_label_info_string,

                                                                 )
                        fout.write("%s\n" % out_line)




    with open(statistics_file, "w") as fout:
        for P in dict_P_to_count:
            fout.write("%s\t%d\t%d\n" % (P, dict_P_to_count[P]["positive"], dict_P_to_count[P]["negative"]))


def tagging_train_data(in_file, to_file, statistics_file):

    dict_P_to_count = {}

    NUM_NEAGTIVE = 100000

    process_bar = pyprind.ProgPercent(1175201)
    with open(in_file) as fin, \
         open(to_file, "w") as fout:

        for line in fin:
            process_bar.update()

            line_list = line.strip().split("\t")
            dict_label_info_string = line_list[-1]
            dict_label_info = ujson.loads(dict_label_info_string)

            # 加载每个P的正负样本:
            for P in dict_label_info:

                if P not in dict_P_to_count:
                    dict_P_to_count[P] = {}
                    dict_P_to_count[P]["positive"] = 0
                    dict_P_to_count[P]["negative"] = 0

                for s_o in dict_label_info[P]["candidates"]:
                    label = dict_label_info[P]["candidates"][s_o]["label"]

                    #  正例
                    if label > 0:
                        dict_P_to_count[P]["positive"] += 1
                        dict_label_info[P]["candidates"][s_o]["wanted"] = 1
                    else:
                        # 负例
                        if label < 0 and dict_P_to_count[P]["negative"] < NUM_NEAGTIVE:
                            dict_P_to_count[P]["negative"] += 1

                            dict_label_info[P]["candidates"][s_o]["wanted"] = 1
                        else:
                            dict_label_info[P]["candidates"][s_o]["wanted"] = 0

            out_line_list = line_list[:-1] + [ujson.dumps(dict_label_info, ensure_ascii=False)]
            fout.write("\t".join(out_line_list) + "\n")



    with open(statistics_file, "w") as fout:
        for P in dict_P_to_count:
            fout.write("%s\t%d\t%d\n" % (P, dict_P_to_count[P]["positive"], dict_P_to_count[P]["negative"]))


def load_train_data_hadoop():

    dict_P_to_count = {}

    NUM_NEAGTIVE = 100000

    for line in sys.stdin:

        sent_id, sent_text, tokens, pos_tags, ner_tags, dep_types, dep_tokens,\
        S_O, dict_label_info = line.strip().split("\t")

        dict_label_info = ujson.loads(dict_label_info)

        # 过滤一下SO识别
        dict_so = ujson.loads(S_O)
        dict_so_new = {}
        for P in dict_so:
            if P in dict_label_info:
                dict_so_new[P] = dict_so[P]


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

                    print "%s\t%s\t%s\t%s\t%s\t%s\t%s" % (sent_text, S_text, P, O_text, "1",
                                                             ujson.dumps(dict_label_info, ensure_ascii=False),
                                                             ujson.dumps(dict_so_new, ensure_ascii=False),
                                                             )


                if label < 0 and dict_P_to_count[P]["negative"] < NUM_NEAGTIVE:
                    dict_P_to_count[P]["negative"] += 1
                    print "%s\t%s\t%s\t%s\t%s\t%s\t%s" % (sent_text, S_text, P, O_text, "-1",
                                                             ujson.dumps(dict_label_info, ensure_ascii=False),
                                                             ujson.dumps(dict_so_new, ensure_ascii=False),
                                                             )




if __name__ == '__main__':
    # load_train_data("/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/SPO_train_data_for_deepdive_label")
    # load_train_data(
    #     "/home/disk2/wangjianxiang01/downloads/SPO_train_data_84P_for_deepdive_label_1w_pos_5w_neg",
    #     "/home/disk2/wangjianxiang01/downloads/SPO_train_data_84P_for_deepdive_label_1w_pos_10w.spo.sent",
    #     "/home/disk2/wangjianxiang01/downloads/SPO_train_data_84P_for_deepdive_label_1w_pos_10w.spo.sent.statistics",
    # )

    tagging_train_data(
        "/home/disk2/wangjianxiang01/BaiduIntern/zh_deepdive/obtain_train_new/3_filte_sentences_label/SPO_train_data_84P_for_deepdive_label_lihe_1w_pos_5w_neg",
        "/home/disk2/wangjianxiang01/BaiduIntern/zh_deepdive/obtain_train_new/3_filte_sentences_label/SPO_train_data_84P_for_deepdive_label_lihe_1w_pos_5w_neg.tagged",
        "/home/disk2/wangjianxiang01/BaiduIntern/zh_deepdive/obtain_train_new/3_filte_sentences_label/SPO_train_data_84P_for_deepdive_label_lihe_1w_pos_5w_neg.statistics",
    )

    # load_train_data_hadoop()








