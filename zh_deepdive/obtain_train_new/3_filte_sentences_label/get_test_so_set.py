# coding: utf-8
import os
import sys
import cPickle
reload(sys)
sys.setdefaultencoding('utf-8')


def get_test_so_set_for_62P(in_file, to_file):
    so_set = set([])
    with open(in_file) as fin:
        for line in fin:
            _, _, spo_list = line.strip().split("\t")
            spo_list = eval(spo_list)

            so_set |= set([(s, o) for s, _, o in spo_list])

    cPickle.dump(so_set, open(to_file, "wb"))

def get_test_so_set_for_84P(seed_62P_file, seed_22P_dir, to_file):

    so_set = set([])

    fin = open(seed_62P_file)
    for line in fin:
        _, _, spo_list = line.strip().split("\t")
        spo_list = eval(spo_list)

        so_set |= set([(s, o) for s, _, o in spo_list])
    fin.close()

    for file_name in listdir_no_hidden(seed_22P_dir):
        with open("%s/%s" % (seed_22P_dir, file_name)) as fin:
            for line in fin:
                S, O, P = line.strip().split("\t")
                so_set.add((S, O))

    cPickle.dump(so_set, open(to_file, "wb"))


def listdir_no_hidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f


if __name__ == '__main__':
   # get_test_so_set_for_62P("seed.test.data", "test_so_set.cPkl")

   get_test_so_set_for_84P("../../data/seed.test.data", "../../data/seed_22P_for_test", "test_so_set_for_84P.cPkl")
