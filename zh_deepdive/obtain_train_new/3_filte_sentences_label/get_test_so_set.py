# coding: utf-8
import sys
import cPickle
reload(sys)
sys.setdefaultencoding('utf-8')


def get_test_so_set(in_file, to_file):
    so_set = set([])
    with open(in_file) as fin:
        for line in fin:
            _, _, spo_list = line.strip().split("\t")
            spo_list = eval(spo_list)

            so_set |= set([(s, o) for s, _, o in spo_list])

    cPickle.dump(so_set, open(to_file, "wb"))

if __name__ == '__main__':
   get_test_so_set("seed.test.data", "test_so_set.cPkl")
