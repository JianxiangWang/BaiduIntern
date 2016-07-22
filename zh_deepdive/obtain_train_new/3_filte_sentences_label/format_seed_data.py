#!tools/python/bin/python
# coding: utf-8
import json
import os
import uuid
import sys
import cPickle
import random

reload(sys)
sys.setdefaultencoding('utf-8')

def format_seed_to_json(in_file, to_file):
    dict_P_to_seeds = {}

    fin = open(in_file)
    for line in fin:
        num, P, seed_list = line.strip().split("\t")
        seed_list_temp = eval(seed_list)
        seed_list = [[s, o] for s, p, o in seed_list_temp]
        dict_P_to_seeds[P] = seed_list

    json.dump(dict_P_to_seeds, open(to_file, "w"), ensure_ascii=False)

def format_seed_to_pkl(in_file, to_file):
    dict_P_to_seeds = {}

    fin = open(in_file)
    for line in fin:
        num, P, seed_list = line.strip().split("\t")
        seed_list_temp = eval(seed_list)
        seed_set = set([(s, o) for s, _, o in seed_list_temp])
        dict_P_to_seeds[P] = seed_set

    cPickle.dump(dict_P_to_seeds, open(to_file, "wb"))


def format_22P_seed_to_json(in_dir, to_file):
    dict_P_to_seeds = {}
    for file_name in listdir_no_hidden(in_dir):
        with open("%s/%s" % (in_dir, file_name)) as fin:
            for line in fin:
                S, O, P = line.strip().split("\t")

                if P not in dict_P_to_seeds:
                    dict_P_to_seeds[P] = []
                dict_P_to_seeds[P].append([S, O])

    json.dump(dict_P_to_seeds, open(to_file, "w"), ensure_ascii=False)


def format_22P_seed_to_pkl(in_dir, to_file):
    dict_P_to_seeds = {}
    for file_name in listdir_no_hidden(in_dir):
        with open("%s/%s" % (in_dir, file_name)) as fin:
            for line in fin:
                S, O, P = line.strip().split("\t")
                if P not in dict_P_to_seeds:
                    dict_P_to_seeds[P] = set([])
                dict_P_to_seeds[P].add((S, O))

    cPickle.dump(dict_P_to_seeds, open(to_file, "wb"))


def format_84P_seed_to_json(seed_62P_file, seed_22P_dir, to_file):

    dict_P_to_seeds = {}

    fin = open(seed_62P_file)
    for line in fin:
        num, P, seed_list = line.strip().split("\t")
        seed_list_temp = eval(seed_list)
        seed_list = [[s, o] for s, p, o in seed_list_temp]
        dict_P_to_seeds[P] = seed_list
    fin.close()

    for file_name in listdir_no_hidden(seed_22P_dir):
        with open("%s/%s" % (seed_22P_dir, file_name)) as fin:
            for line in fin:
                S, O, P = line.strip().split("\t")

                P = "人物_" + P

                if P not in dict_P_to_seeds:
                    dict_P_to_seeds[P] = []
                dict_P_to_seeds[P].append([S, O])


    json.dump(dict_P_to_seeds, open(to_file, "w"), ensure_ascii=False)


def format_84P_seed_to_pkl(seed_62P_file, seed_22P_dir, to_file):

    dict_P_to_seeds = {}

    fin = open(seed_62P_file)
    for line in fin:
        num, P, seed_list = line.strip().split("\t")
        seed_list_temp = eval(seed_list)
        seed_set = set([(s, o) for s, _, o in seed_list_temp])
        dict_P_to_seeds[P] = seed_set
    fin.close()

    for file_name in listdir_no_hidden(seed_22P_dir):
        with open("%s/%s" % (seed_22P_dir, file_name)) as fin:
            for line in fin:
                S, O, P = line.strip().split("\t")

                P = "人物_" + P

                if P not in dict_P_to_seeds:
                    dict_P_to_seeds[P] = set([])
                dict_P_to_seeds[P].add((S, O))


    cPickle.dump(dict_P_to_seeds, open(to_file, "wb"))


def listdir_no_hidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f


# 17995.9352518
def get_average_so_num_for_each_P(in_file):
    dict_P_to_seeds = cPickle.load(open(in_file, "rb"))

    total = 0
    for P in dict_P_to_seeds:
        total += len(dict_P_to_seeds[P])

    return total / float(len(dict_P_to_seeds))


def sample_heyan_seed_train_data(in_file, N, to_file):

    with open(in_file) as fin, \
         open(to_file, "w") as fout:

        s_o_p_list = []
        for line in fin:
            S, P, O, _ = line.strip().split("\t")
            s_o_p_list.append((S, O, P))

        sampled = random.sample(s_o_p_list, N)

        fout.write("\n".join(["\t".join(item) for item in sampled]))


def format_heyan_seed_test_data(in_file, to_file):

    with open(in_file) as fin, \
         open(to_file, "w") as fout:

        s_o_p_list = []
        for line in fin:
            S, P, O, _ = line.strip().split("\t")
            s_o_p_list.append((S, O, P))


        fout.write("\n".join(["\t".join(item) for item in s_o_p_list]))







if __name__ == '__main__':

    # format_22P_seed_to_json("../../data/seed_22P_for_train", "../../data/seed_22P_for_train.json")

    # format_seed_to_json("seed.train.data", "seed.train.json")
    # format_seed_to_pkl("seed.train.data", "seed.train.cPkl")

    # dict_P_to_seeds = cPickle.load(open("seed.train.cPkl", "rb"))
    #
    # print dict_P_to_seeds["历史人物_配偶"]

    # format_84P_seed_to_json("../../data/seed.train.data.cleaned", "../../data/seed_22P_for_train", "seed_train_for_84P.json")
    # format_84P_seed_to_pkl("../../data/seed.train.data.cleaned", "../../data/seed_22P_for_train", "seed_train_for_84P.cPkl")

    # print get_average_so_num_for_each_P("seed_train_for_84P.cPkl")

    # 对合演的train种子,进行采样
    sample_heyan_seed_train_data("../../data/heyan.train.all", 17000, "../../data/seed_22P_for_train/heyan.seed.utf8.train")
    # 对合演的test种子,全部
    format_heyan_seed_test_data("../../data/heyan.test.seed", "../../data/seed_22P_for_test/heyan.seed.utf8.test")





