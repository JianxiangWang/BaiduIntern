# coding: utf-8
import json
import sys,codecs
import cPickle
reload(sys)
sys.setdefaultencoding('utf-8')
import csv
import os


#[{'first_name': 'Baked', 'last_name': 'Beans'}, {'first_name': 'Lovely', 'last_name': 'Spam'}]
def read_dict_from_csv(in_file):
    if not os.path.exists(in_file):
        return []
    with codecs.open(in_file, "r") as csvfile:
        return list(csv.DictReader(csvfile))


def get_P_to_positive_guide_words(in_file):

    dict_P_to_positive_guide_words = {}

    for d in read_dict_from_csv(in_file):
        P = "%s_%s" % (d["领域"], d["P"])
        guide_words = []
        # 1
        guide_words.append(d["P"])
        # 2
        if d["引导词"].strip():
            guide_words += d["引导词"].strip().split(";")
        # 3
        if d["引导词扩充"].strip():
            guide_words += d["引导词扩充"].strip().split(";")

        dict_P_to_positive_guide_words[P] = set(guide_words)


    return dict_P_to_positive_guide_words

# 获取positive 和 negative的 guide
def get_guide_words_to_json(P_guide_words_file, P_similar_file, to_file):
    dict_P_to_positive_guide_words = get_P_to_positive_guide_words(P_guide_words_file)

    dict_P_to_guide_words = {}
    for line in open(P_similar_file):
        print line
        P, Q = line.strip().split("-->")
        Q_list = Q.split(",")
        Q_list.append(P) # 与自己是互斥的
        # positive
        dict_P_to_guide_words[P] = {}
        dict_P_to_guide_words[P]["positive"] = list(sorted(dict_P_to_positive_guide_words[P]))
        # negative
        negative_guide_words = set()
        for curr_P in dict_P_to_positive_guide_words:
            guide_words = dict_P_to_positive_guide_words[curr_P]
            if curr_P not in Q_list:
                negative_guide_words |= guide_words

        # 去掉正的有的
        negative_guide_words -= dict_P_to_positive_guide_words[P]
        dict_P_to_guide_words[P]["negative"] = list(sorted(negative_guide_words))

    json.dump(dict_P_to_guide_words, open(to_file, "w"), ensure_ascii=False)

# 获取positive 和 negative的 guide
def get_guide_words_to_pkl(P_guide_words_file, P_similar_file, to_file):
    dict_P_to_positive_guide_words = get_P_to_positive_guide_words(P_guide_words_file)

    dict_P_to_guide_words = {}
    for line in open(P_similar_file):
        print line
        P, Q = line.strip().split("-->")
        Q_list = Q.split(",")
        Q_list.append(P) # 与自己是互斥的
        # positive
        dict_P_to_guide_words[P] = {}
        dict_P_to_guide_words[P]["positive"] = dict_P_to_positive_guide_words[P]
        # negative
        negative_guide_words = set()
        for curr_P in dict_P_to_positive_guide_words:
            guide_words = dict_P_to_positive_guide_words[curr_P]
            if curr_P not in Q_list:
                negative_guide_words |= guide_words

        # 去掉正的有的
        negative_guide_words -= dict_P_to_positive_guide_words[P]

        dict_P_to_guide_words[P]["negative"] = negative_guide_words

    cPickle.dump(dict_P_to_guide_words, open(to_file, "wb"))


def get_62P_guide_words(to_file):

    fout = open(to_file, "w")

    for d in read_dict_from_csv("data/全网SPO挖掘通用领域P梳理文档2.csv"):
        P = "%s_%s" % (d["领域"], d["P"])
        guide_words = []
        # 1
        guide_words.append(d["P"])
        # 2
        if d["引导词"].strip():
            guide_words += d["引导词"].strip().split(";")
        # 3
        if d["引导词扩充"].strip():
            guide_words += d["引导词扩充"].strip().split(";")


        fout.write("%s-->%s\n" % (P, "\t".join(sorted(set(guide_words)))))

    fout.close()

def get_22P_guide_words(to_file):

    fout = open(to_file, "w")

    for line in open("data/guide.22.utf8"):
        line_list = line.strip().split("\t")
        P = "人物_" + line_list[0]
        guide_words = line_list[1:]

        fout.write("%s-->%s\n" % (P, "\t".join(sorted(set(guide_words)))))

    fout.close()


def get_84P_positive_negative_guide_words_to_pkl(P_similar_file, to_file):

    dict_P_to_positive_guide_words = {}

    # 62P的引导词
    for line in open("data/guide_words_for_62P.txt"):
        P, guide_words_str = line.strip().split("-->")
        guide_words = guide_words_str.split("\t")
        dict_P_to_positive_guide_words[P] = set(guide_words)

     # 22P的引导词
    for line in open("data/guide_words_for_22P.txt"):
        P, guide_words_str = line.strip().split("-->")
        guide_words = guide_words_str.split("\t")
        dict_P_to_positive_guide_words[P] = set(guide_words)


    dict_P_to_guide_words = {}
    for line in open(P_similar_file):
        print line
        P, Q = line.strip().split("-->")
        Q_list = Q.split(",")
        Q_list.append(P) # 与自己是互斥的
        # positive
        dict_P_to_guide_words[P] = {}
        dict_P_to_guide_words[P]["positive"] = dict_P_to_positive_guide_words[P]
        # negative
        negative_guide_words = set()
        for curr_P in dict_P_to_positive_guide_words:
            guide_words = dict_P_to_positive_guide_words[curr_P]
            if curr_P not in Q_list:
                negative_guide_words |= guide_words

        # 去掉正的有的
        negative_guide_words -= dict_P_to_positive_guide_words[P]
        # 去掉一些
        exclude = set(["#", "-", "15岁以上", "@", "AKS", "CM", "G", "HBS", "Hong Kong:IIB",
                       "KG", "MTV电影奖", "Mnet电视台", "PG", "PG-13", "Pop", "R", "South Korea:15",
                       "TVB", "USA:PG", "USA:R", "VS", "cm", "imdb编码", "imdb链接", "kg", "vs", "《", "》"])

        negative_guide_words -= exclude

        dict_P_to_guide_words[P]["negative"] = negative_guide_words

    cPickle.dump(dict_P_to_guide_words, open(to_file, "wb"))


def get_84P_positive_negative_guide_words_to_json(P_similar_file, to_file):

    dict_P_to_positive_guide_words = {}

    # 62P的引导词
    for line in open("data/guide_words_for_62P.txt"):
        P, guide_words_str = line.strip().split("-->")
        guide_words = guide_words_str.split("\t")
        dict_P_to_positive_guide_words[P] = set(guide_words)

     # 22P的引导词
    for line in open("data/guide_words_for_22P.txt"):
        P, guide_words_str = line.strip().split("-->")
        guide_words = guide_words_str.split("\t")
        dict_P_to_positive_guide_words[P] = set(guide_words)


    dict_P_to_guide_words = {}
    for line in open(P_similar_file):
        print line
        P, Q = line.strip().split("-->")
        Q_list = Q.split(",")
        Q_list.append(P) # 与自己是互斥的
        # positive
        dict_P_to_guide_words[P] = {}
        dict_P_to_guide_words[P]["positive"] = list(sorted(dict_P_to_positive_guide_words[P]))
        # negative
        negative_guide_words = set()
        for curr_P in dict_P_to_positive_guide_words:
            guide_words = dict_P_to_positive_guide_words[curr_P]
            if curr_P not in Q_list:
                negative_guide_words |= guide_words

        # 去掉正的有的
        negative_guide_words -= dict_P_to_positive_guide_words[P]
        # 去掉一些
        exclude = set(["#", "-", "15岁以上", "@", "AKS", "CM", "G", "HBS", "Hong Kong:IIB",
                       "KG", "MTV电影奖", "Mnet电视台", "PG", "PG-13", "Pop", "R", "South Korea:15",
                       "TVB", "USA:PG", "USA:R", "VS", "cm", "imdb编码", "imdb链接", "kg", "vs", "《", "》"])

        negative_guide_words -= exclude


        dict_P_to_guide_words[P]["negative"] = list(sorted(negative_guide_words))

    json.dump(dict_P_to_guide_words, open(to_file, "w"), ensure_ascii=False)










if __name__ == '__main__':
    # get_P_to_positive_guide_words("data/全网SPO挖掘通用领域P梳理文档2.csv")

    # get_guide_words_to_json("data/全网SPO挖掘通用领域P梳理文档2.csv", "data/P_similar", "data/guide_words.json")
    # get_guide_words_to_pkl("data/全网SPO挖掘通用领域P梳理文档2.csv", "data/P_similar", "data/guide_words.cPkl")

    # get_62P_guide_words("data/guide_words_for_62P.txt")
    # get_22P_guide_words("data/guide_words_for_22P.txt")

    get_84P_positive_negative_guide_words_to_pkl("data/P_similar", "data/guide_words.cPkl")
    get_84P_positive_negative_guide_words_to_json("data/P_similar", "data/guide_words.json")

    pass