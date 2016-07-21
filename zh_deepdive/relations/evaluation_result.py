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



if __name__ == '__main__':
    # main("evaluation.result")
    # evaluation("models",
    #            "/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/seed.test.json",
    #             "/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/seed.test.data.sample.json",
    #             "evaluation.result")


    evaluation_with_statistics("models",
               "/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/SPO_train_data_for_deepdive_label_post_processing.statistics.csv",
               "/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/seed.test.json",
                "/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/seed.test.data.sample.json",
                "evaluation.result.csv")