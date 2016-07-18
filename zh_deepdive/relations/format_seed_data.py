#!tools/python/bin/python
# coding: utf-8
import json
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



if __name__ == '__main__':

    format_seed_to_json("../data/seed.test.data", "../data/seed.test.json")
    format_seed_to_json("../data/seed.test.data.sample", "../data/seed.test.data.sample.json")


    # format_seed_to_pkl("seed.train.data", "seed.train.cPkl")
    # dict_P_to_seeds = cPickle.load(open("seed.train.cPkl", "rb"))
    #




