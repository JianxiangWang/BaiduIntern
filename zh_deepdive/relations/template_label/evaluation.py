#!/usr/bin/env python
import codecs
import psycopg2
import json


def write_predict_to_json(threshold, to_file):
    with open("db.url") as db_url_file, \
         open("P") as P_file:

        database = db_url_file.read().strip().split("/")[-1]
        P = P_file.read().strip()

        dict_predict = {}
        dict_predict[P] = []

        try:
            conn = psycopg2.connect(host="222.204.232.208", database=database, user='jianxiang', password='123456')

            cur = conn.cursor()

            query = """SELECT * from has_relation_label_inference where id in
                           (select variable_id from dd_graph_variables_holdout)
                           and expectation > %f order by expectation desc
            """ % threshold

            cur.execute(query)

            rows = cur.fetchall()
            for row in rows:
                s, o, prob = row[1], row[3], row[-1]
                dict_predict[P].append([s, o, prob])


            json.dump(dict_predict, open(to_file, "w"), ensure_ascii=False)


            conn.close()

        except:
            print "can not connect to the database..."


def calculate_P_R(predict_json, silver_all_seed_json, silver_sample_seed_json, to_file):

    #
    dict_predict = json.load(open(predict_json))
    dict_all_seed = json.load(open(silver_all_seed_json))
    dict_sample_seed = json.load(open(silver_sample_seed_json))

    fout = codecs.open(to_file, "w", encoding="utf-8")
    for P in dict_predict:
        predicts = set([(s, o) for s, o, prob in dict_predict[P]])
        silver_all = set(map(tuple, dict_all_seed[P]))
        silver_sample = set(map(tuple, dict_sample_seed[P]))

        precision = len(predicts & silver_all) / float(len(predicts)) * 100
        recall = len(predicts & silver_sample) / float(len(silver_sample)) * 100

        print "%s\tprecision: %.2f%%\trecall: %.2f%%" % (P, precision, recall)
        fout.write("%s\tprecision: %.2f%%\trecall: %.2f%%\n" % (P, precision, recall))

    fout.close()

if __name__ == '__main__':
    write_predict_to_json(0.6, "predict.json")
    calculate_P_R("predict.json",
                  "/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/seed.test.json",
                  "/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/seed.test.data.sample.json",
                  "evaluation.result"
    )