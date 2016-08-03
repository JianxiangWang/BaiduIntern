#!/usr/bin/env python
# coding: utf-8
import csv
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import codecs
import glob
import json
import util


#[{'first_name': 'Baked', 'last_name': 'Beans'}, {'first_name': 'Lovely', 'last_name': 'Spam'}]
def read_dict_from_csv(in_file):
    if not os.path.exists(in_file):
        return []
    with codecs.open(in_file, "r") as csvfile:
        return list(csv.DictReader(csvfile))

def main(to_file):
    fout = open(to_file, "w")
    for file_path in glob.glob('models/*/evaluation.result'):
        with open(file_path) as fin:
            line = fin.read()
            print line.strip()
            fout.write(line)

    fout.close()


def evaluation(model_dir, silver_all_seed_json, silver_sample_seed_json, to_file):

    dict_all_seed = json.load(open(silver_all_seed_json))
    dict_sample_seed = json.load(open(silver_sample_seed_json))

    # 分子, 也就是对的个数
    precision_molecular = 0
    # 分母, 也就是预测的个数
    precision_denominator = 0

    recall_molecular = 0
    recall_denominator = 0

    fout = codecs.open(to_file, "w", encoding="utf-8")

    for predict_file in glob.glob('%s/*/predict.json' % model_dir):

        dict_predict = json.load(open(predict_file))
        for P in dict_predict:
            predicts = set([(s, o) for s, o, prob in dict_predict[P]])
            silver_all = set(map(tuple, dict_all_seed[P]))
            silver_sample = set(map(tuple, dict_sample_seed[P]))

            precision_molecular += len(predicts & silver_all)
            precision_denominator += len(predicts)

            recall_molecular += len(predicts & silver_sample)
            recall_denominator += len(silver_sample)

            # 每个P也计算一下吧
            if len(predicts) == 0:
                precision = 0
                recall = 0
            else:
                precision = len(predicts & silver_all) / float(len(predicts)) * 100
                recall = len(predicts & silver_sample) / float(len(silver_sample)) * 100

            s = "%s\tprecision: %d / %d = %.2f%%\trecall: %d / %d = %.2f%%" % \
                        ( P,
                         len(predicts & silver_all), len(predicts), precision,
                         len(predicts & silver_sample), len(silver_sample), recall)

            print s

            fout.write(s + "\n")


    micro_precision = precision_molecular / float(precision_denominator) * 100
    micro_recall  = recall_molecular / float(recall_denominator) * 100

    s = "%s\tprecision: %d / %d = %.2f%%\trecall: %d / %d = %.2f%%" % \
                        ( "Micro",
                         precision_molecular, precision_denominator, micro_precision,
                         recall_molecular, recall_denominator, micro_recall)
    print s


    fout.write(s + "\n")
    fout.close()


def evaluation_with_statistics(model_dir, statistics_file , silver_all_seed_json, silver_sample_seed_json, to_file):

    statistics_list = read_dict_from_csv(statistics_file)

    dict_result = {}
    positive_count = 0
    negative_count = 0
    NULL_count = 0
    for x in statistics_list:
        P, positive, negative, null_ = x["P"], x["positive"], x["negative"], x["NULL"]
        P = unicode(P)
        dict_result[P] = {}
        dict_result[P]["positive"] = int(positive)
        dict_result[P]["negative"] = int(negative)
        dict_result[P]["NULL"] = int(null_)

        positive_count += int(positive)
        negative_count += int(negative)
        NULL_count += int(null_)


    dict_all_seed = json.load(open(silver_all_seed_json))
    dict_sample_seed = json.load(open(silver_sample_seed_json))

    # 分子, 也就是对的个数
    precision_molecular = 0
    # 分母, 也就是预测的个数
    precision_denominator = 0

    recall_molecular = 0
    recall_denominator = 0

    #
    N = 0
    macro_precision = 0.0
    macro_recall = 0.0

    for predict_file in glob.glob('%s/*/predict.json' % model_dir):

        dict_predict = json.load(open(predict_file))
        for P in dict_predict:
            predicts = set([(s, o) for s, o, prob in dict_predict[P]])
            silver_all = set(map(tuple, dict_all_seed[P]))
            silver_sample = set(map(tuple, dict_sample_seed[P]))

            precision_molecular += len(predicts & silver_all)
            precision_denominator += len(predicts)

            recall_molecular += len(predicts & silver_sample)
            recall_denominator += len(silver_sample)

            # 每个P也计算一下吧
            if len(predicts) == 0:
                precision = 0
                recall = 0
            else:
                precision = len(predicts & silver_all) / float(len(predicts)) * 100
                recall = len(predicts & silver_sample) / float(len(silver_sample)) * 100

            N += 1
            macro_precision += precision
            macro_recall += recall



            dict_result[P]["precision"] = "%d / %d = %.2f%%" %\
                                          (len(predicts & silver_all), len(predicts), precision)

            dict_result[P]["recall"] = "%d / %d = %.2f%%" % (len(predicts & silver_sample), len(silver_sample), recall)


            s = "%s\tprecision: %d / %d = %.2f%%\trecall: %d / %d = %.2f%%" % \
                        ( P,
                         len(predicts & silver_all), len(predicts), precision,
                         len(predicts & silver_sample), len(silver_sample), recall)

            print s



    micro_precision = precision_molecular / float(precision_denominator) * 100
    micro_recall  = recall_molecular / float(recall_denominator) * 100

    macro_precision = macro_precision / N
    macro_recall = macro_recall / N


    dict_result["Micro"] = {}
    dict_result["Micro"]["positive"] = positive_count
    dict_result["Micro"]["negative"] = negative_count
    dict_result["Micro"]["NULL"] = NULL_count
    dict_result["Micro"]["precision"] = "%d / %d = %.2f%%" % (precision_molecular, precision_denominator, micro_precision)
    dict_result["Micro"]["recall"] = "%d / %d = %.2f%%" % (recall_molecular, recall_denominator, micro_recall)


    dict_result["Macro"] = {}
    dict_result["Macro"]["positive"] = ""
    dict_result["Macro"]["negative"] = ""
    dict_result["Macro"]["NULL"] = ""
    dict_result["Macro"]["precision"] = "%.2f%%" % (macro_precision)
    dict_result["Macro"]["recall"] = "%.2f%%" % (macro_recall)


    s = "%s\tprecision: %d / %d = %.2f%%\trecall: %d / %d = %.2f%%" % \
                        ( "Micro",
                         precision_molecular, precision_denominator, micro_precision,
                         recall_molecular, recall_denominator, micro_recall)
    print s



    fout = codecs.open(to_file, "w", encoding="utf-8")
    fout.write("P,positive,negative,NULL,precision,recall\n")
    for P in sorted(dict_result.keys()):
        fout.write("%s,%s,%s,%s,%s,%s\n" % (P,
                                            dict_result[P]["positive"],
                                            dict_result[P]["negative"],
                                            dict_result[P]["NULL"],
                                            dict_result[P]["precision"],
                                            dict_result[P]["recall"],
        )
    )
    fout.close()



def get_predict_result(model_dir, to_file):

    dict_predict = {}
    for predict_file in glob.glob('%s/*/predict.json' % model_dir):
        dict_predict.update(json.load(open(predict_file)))

    print len(dict_predict)

    json.dump(dict_predict, open(to_file, "w"), ensure_ascii=False)


# 获取正负样本的统计
def get_statistics(model_dir, to_file):

    out_lines = []
    for relation_dir in util.listdir_no_hidden(model_dir):
        P = open("%s/%s/P" % (model_dir, relation_dir)).read().strip()

        label_log = open("%s/%s/input/label.log" % (model_dir, relation_dir))
        line = label_log.readlines()[0].strip()
        positive = line.split(" vs ")[1].split(": ")[-1]
        negative = line.split(" vs ")[-1]

        out_lines.append("%s,%s,%s" % (P, positive, negative))

    fout = open(to_file, "w")
    fout.write("P,positive,negative\n")
    fout.write("\n".join(out_lines))
    fout.close()


def _test_SPO_to_json(in_file, to_file):

    with open(in_file) as fin, open(to_file, "w") as fout:

        dict_P_to_so_list = {}
        for line in fin:
            s, P, o = line.strip().split("\t")

            if P not in dict_P_to_so_list:
                dict_P_to_so_list[P] = []
            dict_P_to_so_list[P].append((s, o))

        for P in dict_P_to_so_list:
            dict_P_to_so_list[P] = sorted(set(dict_P_to_so_list[P]))

        json.dump(dict_P_to_so_list, fout, ensure_ascii=False)


def _test_SPO_to_json_new(in_file, to_file):

    with open(in_file) as fin, open(to_file, "w") as fout:

        dict_P_to_so_list = {}
        for line in fin:
            # print line.strip().split("\t")[-1]
            spo_list = eval(line.strip().split("\t")[-1])

            for x in spo_list:

                if x.strip() == "":
                    continue

                s, P, o = x.split("-")

                if P not in dict_P_to_so_list:
                    dict_P_to_so_list[P] = []
                dict_P_to_so_list[P].append((s, o))

        for P in dict_P_to_so_list:
            dict_P_to_so_list[P] = sorted(set(dict_P_to_so_list[P]))

        json.dump(dict_P_to_so_list, fout, ensure_ascii=False)


def _test_predict_SPO_to_json(in_file, to_file):

    dict_predict = json.load(open(in_file))

    for P in dict_predict:
        dict_predict[P] = sorted(set([(s, o) for s, o, prob in dict_predict[P]]))

    json.dump(dict_predict, open(to_file, "w"), ensure_ascii=False)

# 根据test过滤so, 只保留test中有的so
def _test_predict_SPO_to_json_only_test_so(test_file, predict_file, threshold, to_file):

    fin = open("../data/reversed_P")
    reversed_P = set([unicode(line.strip()) for line in fin])
    fin.close()

    test_so = set([])
    dict_test = json.load(open(test_file))
    for P in dict_test:
        test_so |= set(map(tuple, dict_test[P]))

    dict_predict = json.load(open(predict_file))
    for P in dict_predict:

        # 对于某些P, s o 反转
        if P in reversed_P:
            t = []
            for s, o, prob in dict_predict[P]:
                t.append([s, o, prob])
                t.append([o, s, prob])
            dict_predict[P] = t

        dict_predict[P] = sorted(set([(s, o) for s, o, prob in dict_predict[P] if (s, o) in test_so and prob >= threshold]))

    json.dump(dict_predict, open(to_file, "w"), ensure_ascii=False)


def evaluate(statistics_file, predict_json_file, gold_json_file, to_file):

    dict_predict = json.load(open(predict_json_file))
    dict_gold = json.load(open(gold_json_file))

    # micro
    # 分子, 也就是对的个数
    precision_molecular = 0
    # 分母, 也就是预测的个数
    precision_denominator = 0

    recall_molecular = 0
    recall_denominator = 0

    # Macro
    precision_N = 0
    recall_N = 0
    macro_precision = 0.0
    macro_recall = 0.0

    dict_result = {}
    for P in dict_predict:

        dict_result[P] = {}

        predicts = set(map(tuple, dict_predict[P]))

        if P in dict_gold:
            golds = set(map(tuple, dict_gold[P]))

            precision_molecular += len(predicts & golds)
            precision_denominator += len(predicts)

            recall_molecular += len(predicts & golds)
            recall_denominator += len(golds)


            if len(predicts) == 0:
                precision = 0

                recall = 0
                recall_N += 1

            else:
                precision_N += 1
                recall_N += 1
                precision = len(predicts & golds) / float(len(predicts)) * 100
                recall = len(predicts & golds) / float(len(golds)) * 100

            macro_precision += precision
            macro_recall += recall



            dict_result[P]["precision"] = "%d / %d = %.2f%%" % (
                len(predicts & golds), len(predicts), precision
            )

            dict_result[P]["recall"] = "%d / %d = %.2f%%" % (
                len(predicts & golds), len(golds), recall
            )

        else:

            precision_molecular += 0
            precision_denominator += len(predicts)

            recall_molecular += 0
            recall_denominator += 0

            # N += 1
            macro_precision += 0
            macro_recall += 0

            dict_result[P]["precision"] = "0 / %d = 0%%" % (len(predicts))
            dict_result[P]["recall"] = "0 / 0 = 0%"


    micro_precision = precision_molecular / float(precision_denominator) * 100
    micro_recall  = recall_molecular / float(recall_denominator) * 100
    dict_result["Micro"] = {}
    dict_result["Micro"]["positive"] = ""
    dict_result["Micro"]["negative"] = ""
    dict_result["Micro"]["precision"] = "%d / %d = %.2f%%" % (precision_molecular, precision_denominator, micro_precision)
    dict_result["Micro"]["recall"] = "%d / %d = %.2f%%" % (recall_molecular, recall_denominator, micro_recall)

    macro_precision = macro_precision / precision_N
    macro_recall = macro_recall / recall_N
    dict_result["Macro"] = {}
    dict_result["Macro"]["positive"] = ""
    dict_result["Macro"]["negative"] = ""
    dict_result["Macro"]["precision"] = "%.2f%%" % (macro_precision)
    dict_result["Macro"]["recall"] = "%.2f%%" % (macro_recall)



    # 加统计
    statistics_list = read_dict_from_csv(statistics_file)

    for x in statistics_list:
        P, positive, negative = x["P"], x["positive"], x["negative"]
        P = unicode(P)
        dict_result[P]["positive"] = int(positive)
        dict_result[P]["negative"] = int(negative)


    fout = codecs.open(to_file, "w", encoding="gb18030")
    fout.write("P,训练集正例SPO个数,训练集负例SPO个数,precision,recall\n")
    for P in sorted(dict_result.keys()):
        fout.write("%s,%s,%s,%s,%s\n" % (P,
                                            dict_result[P]["positive"],
                                            dict_result[P]["negative"],
                                            dict_result[P]["precision"],
                                            dict_result[P]["recall"],
        )
    )
    fout.close()


def get_predict_to_sent_spo(model_dir, to_file):

    dict_sent_to_spo_list = {}
    for predict_file in glob.glob('%s/*/predict.sent.json' % model_dir):
        dict_predict = json.load(open(predict_file))
        for P in dict_predict:
            for s, o, prob, sent_text in dict_predict[P]:

                if sent_text not in dict_sent_to_spo_list:
                    dict_sent_to_spo_list[sent_text] = []
                dict_sent_to_spo_list[sent_text].append((s, P, o))

    # 去重复 & 排序 & to_file
    fout = open(to_file, "w")
    for sent_text in sorted(dict_sent_to_spo_list.keys()):
        spo_list = sorted(set(dict_sent_to_spo_list[sent_text]))
        fout.write("%s\t[%s]\n" % (sent_text,", ".join(["[%s, %s, %s]" % (s, p, o) for s, p, o in spo_list])))

    fout.close()

if __name__ == '__main__':
    # main("evaluation.result")
    # evaluation("models",
    #            "/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/seed.test.json",
    #             "/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/seed.test.data.sample.json",
    #             "evaluation.result")


    # evaluation_with_statistics("models",
    #            "/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/SPO_train_data_for_deepdive_label_post_processing.statistics.csv",
    #            "/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/seed.test.json",
    #             "/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/seed.test.data.sample.json",
    #             "evaluation.result.csv")

    # get_predict_result("models_84P_new_so", "predict_84P_new_so.json")
    # get_statistics("models_84P", "train_label_statistics.csv")

    # _test_SPO_to_json_new("SPO.all.set.data.all.res", "SPO.all.set.data.all.res.json")
    _test_SPO_to_json_new("sent_all_SPO.format.res.all", "SPO.all.set.data.all.res.json")
    _test_predict_SPO_to_json_only_test_so("SPO.all.set.data.all.res.json", "predict_84P_new_so.json", 0.9, "predict_84P_only_test_so_prob_0.9.json")
    # _test_predict_SPO_to_json("predict_84P.json", "predict_84P_only_so.json")

    evaluate("train_label_statistics.csv", "predict_84P_only_test_so_prob_0.9.json", "SPO.all.set.data.all.res.json", "evaluate_500_sents_only_test_so_reverseP_new_so_prob_0.9.gb18030.csv")

    # get_predict_to_sent_spo("models_84P", "predict_sent_spo.txt")

