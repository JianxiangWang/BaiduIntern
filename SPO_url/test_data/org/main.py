# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from confusion_matrix import Alphabet, ConfusionMatrix
import random
import codecs


def main(end_words, p, to_file):

    print "=> %s" % p

    with open("../../data/org") as fin, open(to_file, "w") as fout:

        pos = []
        neg = []

        for line in fin:
            line_list = line.strip().split("\t")
            query = line_list[0]
            url   = line_list[1]
            label = line_list[2]

            if query.endswith(end_words) and "fakeurl" not in url:
                x = "%s\t%s\t%s" % (p, url, label)
                if label == "1":
                    pos.append(x)
                if label == "0":
                    neg.append(x)
        if len(pos) > 60:
            pos = random.sample(pos, 60)
        if len(neg) > 60:

            neg = random.sample(neg, 60)

        fout.write("\n".join(pos) + "\n")
        fout.write("\n".join(neg) + "\n")


def filter_no_pack_urls(in_file, to_file):

    dict_url_to_json_info = {}

    # org  文件
    fin_org = open("../../data/org.all")
    for line in fin_org:
        line_list = line.strip().split("\t")
        url = line_list[0]
        json_info = line_list[-1]
        dict_url_to_json_info[url] = json_info

    with open(in_file) as fin, open(to_file, "w") as fout:
        for line in fin:
            url = line.strip().split("\t")[1]
            if url in dict_url_to_json_info:
                fout.write(line.strip() + "\t" + dict_url_to_json_info[url] + "\n")




def evaluate(gold_file, pred_file):

    with codecs.open(gold_file, encoding="utf-8") as fin_gold, codecs.open(pred_file, encoding="utf-8") as fin_pred:

        dict_P_to_url_label = {}
        for line in fin_gold:
            P, url, label, _ = line.strip().split("\t")
            if P not in dict_P_to_url_label:
                dict_P_to_url_label[P] = set()
            dict_P_to_url_label[P].add((url.strip(), label))

        #
        predict_set = set()
        for line in fin_pred:
            url, s, p, o, confidence = line.strip().split("\t")
            predict_set.add((url.strip(), p))

        alphabet = Alphabet()
        alphabet.add("0")
        alphabet.add("1")

        # 评估
        for P in sorted(dict_P_to_url_label.keys()):

            confusionMatrix = ConfusionMatrix(alphabet)
            for url, label in dict_P_to_url_label[P]:

                pred = "0"
                if (url, P) in predict_set:
                    pred = "1"

                confusionMatrix.add(pred, label)

            print "==" * 40
            print P
            print "==" * 40
            confusionMatrix.print_out()




if __name__ == '__main__':
    # main("吧", "吧", "ba.test.data")
    # main("视频", "视频", "shipin.test.data")
    # main("小说", "小说", "xiaoshuo.test.data")
    # main("下载", "下载", "xiazai.test.data")
    # main("歌曲", "音频", "yinpin.test.data")
    # main("评测", "评测", "pingce.test.data")
    # main("简介", "简介", "jianjie.test.data")
    # main("个人资料", "个人资料", "gerenziliao.test.data")
    # main("百科", "百科", "baike.test.data")
    # main("微博", "微博", "weibo.test.data")
    # main("商品", "商品", "shangpin.test.data")

    # filter_no_pack_urls("org.test.data", "org.test.data.filtered")

    evaluate("org.test.data.filtered", "org.test.data.filtered.spo")