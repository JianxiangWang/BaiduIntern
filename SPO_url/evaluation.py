#!/usr/bin/env python
# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def main(predict_file, gold_file):
    with open(predict_file) as fin_predict, open(gold_file) as fin_gold_file:
        dict_predict = {}
        for line in fin_predict:
            url, S, P, O = line.strip().split("\t")
            if P not in dict_predict:
                dict_predict[P] = set([])
            dict_predict[P].add(url)

        dict_gold = {}
        for line in fin_gold_file:
            P, url = line.strip().split("\t")
            if P not in dict_gold:
                dict_gold[P] = set([])
            dict_gold[P].add(url)

        for P in dict_predict:
            predicts = dict_predict[P]
            golds = dict_gold[P]
            precision = len((predicts & golds)) / float(len(predicts))
            recall = len((predicts & golds)) / float(len(golds))
            print "%s\tprecision:%.2f%%\trecall:%.2f%%" % (P, precision * 100, recall*100)


if __name__ == '__main__':

    predict_file = sys.argv[1]
    gold_file = "/home/disk2/wangjianxiang01/BaiduIntern/SPO_url/data/test.data"
    main(predict_file, gold_file)