#!tools/python/bin/python
# coding: utf-8
import json
import os
import uuid
import sys
import cPickle

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
                    dict_P_to_seeds[P] = set([])
                dict_P_to_seeds[P].add((S, O))

    json.dump(dict_P_to_seeds, open(to_file, "w"), ensure_ascii=False)


def listdir_no_hidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f



if __name__ == '__main__':

    format_22P_seed_to_json()

    # format_seed_to_json("seed.train.data", "seed.train.json")
    # format_seed_to_pkl("seed.train.data", "seed.train.cPkl")

    dict_P_to_seeds = cPickle.load(open("seed.train.cPkl", "rb"))

    print dict_P_to_seeds["历史人物_配偶"]



