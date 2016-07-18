# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pickle

def main(to_file):
    dict_P_to_seeds = {}

    fin = open("input/seed.train.data")
    for line in fin:
        num, P, seed_list = line.strip().split("\t")
        seed_list = eval(seed_list)
        if P not in dict_P_to_seeds:
            dict_P_to_seeds[P] = set()

        for s, p, o in seed_list:
            if s.strip() != "" and o.strip() != "":
                dict_P_to_seeds[P].add((s, o))

    fin.close()

    fin = open("input/seed.test.data")
    for line in fin:
        num, P, seed_list = line.strip().split("\t")
        seed_list = eval(seed_list)
        if P not in dict_P_to_seeds:
            dict_P_to_seeds[P] = set()

        for s, p, o in  seed_list:
            if s.strip() != "" and o.strip() != "":
                dict_P_to_seeds[P].add((s, o))

    fin.close()

    pickle.dump(dict_P_to_seeds, open(to_file, "wb"))

    # fout = open(to_file, "w")
    # for P in dict_P_to_seeds:
    #     num = len(dict_P_to_seeds[P])
    #     s = "{%s}" % ", ".join(["(\"%s\", \"%s\")"  % (s.replace('"','\\"'), o.replace('"','\\"')) for s, o in dict_P_to_seeds[P]])
    #
    #     fout.write("%s\t%d\t%s\n" % (P, num, s))
    #
    # fout.close()



if __name__ == '__main__':
    main("input/seed.all.data.pkl")

