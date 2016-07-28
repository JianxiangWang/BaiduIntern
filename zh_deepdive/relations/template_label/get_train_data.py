#!/usr/bin/env python
#encoding: utf-8
import codecs
import psycopg2
import json,sys
from pypinyin import lazy_pinyin
reload(sys)
sys.setdefaultencoding("utf-8")


def load_train_data(to_dir):
    with open("P") as P_file:
        P = P_file.read().strip()

    with open("db.url") as db_url_file, open(to_dir + "/" + hanzi_to_pinyi(P) + ".train.data", "w") as fout:

        database = db_url_file.read().strip().split("/")[-1]

        try:
            conn = psycopg2.connect(host="222.204.232.208", database=database, user='jianxiang', password='123456')

            cur = conn.cursor()

            query = """select * from so_label WHERE s_id not like 'test_' and label=1 limit 1000"""

            cur.execute(query)

            rows = cur.fetchall()
            for row in rows:
                s_id, o_id, label, rule_ids = row[0], row[1], row[2], row[3]

                # 获取对应的句子
                sent_id = "_".join(s_id.split("_")[:-2])
                sent_query = "select sent_text from sentence where sent_id='%s'" % sent_id
                cur.execute(sent_query)
                sent_text = cur.fetchall()[0][0]
                # 获取 S, O 的名称
                mention_query = "select mention_text from so_mention where mention_id='%s'" % s_id
                cur.execute(mention_query)
                s_name = cur.fetchall()[0][0]
                mention_query = "select mention_text from so_mention where mention_id='%s'" % o_id
                cur.execute(mention_query)
                o_name = cur.fetchall()[0][0]

                fout.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (sent_text, s_name, P, o_name, label, rule_ids))



            query = """select * from so_label WHERE s_id not like 'test_' and label=-1 limit 1000"""

            cur.execute(query)

            rows = cur.fetchall()
            for row in rows:
                s_id, o_id, label, rule_ids = row[0], row[1], row[2], row[3]

                # 获取对应的句子
                sent_id = "_".join(s_id.split("_")[:-2])
                sent_query = "select sent_text from sentence where sent_id='%s'" % sent_id
                cur.execute(sent_query)
                sent_text = cur.fetchall()[0][0]
                # 获取 S, O 的名称
                mention_query = "select mention_text from so_mention where mention_id='%s'" % s_id
                cur.execute(mention_query)
                s_name = cur.fetchall()[0][0]
                mention_query = "select mention_text from so_mention where mention_id='%s'" % o_id
                cur.execute(mention_query)
                o_name = cur.fetchall()[0][0]

                fout.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (sent_text, s_name, P, o_name, label, rule_ids))



            conn.close()

        except:
            print "can not connect to the database..."

def hanzi_to_pinyi(hanzi):
    s = "".join(map(lambda x: x[0].upper() + x[1:], lazy_pinyin(unicode(hanzi))))
    return s[0].lower() + s[1:]

if __name__ == '__main__':
    load_train_data("/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/train_data")
