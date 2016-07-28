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
        dict_url_to_P = {}
        for line in fin_gold_file:
            P, url = line.strip().split("\t")
            dict_url_to_P[url] = P

            if P not in dict_gold:
                dict_gold[P] = set([])
            dict_gold[P].add(url)

        for P in dict_predict:
            predicts = dict_predict[P]
            golds = dict_gold[P]

            # errors
            for predict in predicts - golds:
                url = predict
                label = dict_url_to_P[url]
                pred = P
                print "%s\t%s-->%s" % (url, label, pred)

            precision = len((predicts & golds)) / float(len(predicts))
            recall = len((predicts & golds)) / float(len(golds))
            print "%s\tprecision: %d / %d = %.2f%%\trecall: %d / %d = %.2f%%" \
                  % (P,
                     len((predicts & golds)), len(predicts), precision * 100,
                     len((predicts & golds)), len(golds), recall*100)


if __name__ == '__main__':

    predict_file = sys.argv[1]
    gold_file = "/home/disk2/wangjianxiang01/BaiduIntern/SPO_url/data/test.data"
    main(predict_file, gold_file)