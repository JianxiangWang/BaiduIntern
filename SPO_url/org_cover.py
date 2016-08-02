# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# url级别的cover
def cover_1():

    golds_set = set()

    fin = open("data/org.positive")
    for line in fin:
        P, url = line.strip().split("\t")
        golds_set.add(url)
    fin.close()

    predicts_set = set()
    fin = open("data/org.positive.predicts")
    for line in fin:
        url, s, p, o = line.strip().split("\t")
        predicts_set.add(url)
    fin.close()

    coverage = len(golds_set & predicts_set) / float(len(golds_set)) * 100

    print "%d / %d = %.2f%%" % (len(golds_set & predicts_set), len(golds_set), coverage)


# url, p级别的cover
def cover_2():

    golds_set = set()

    fin = open("data/org.positive")
    for line in fin:
        p, url = line.strip().split("\t")
        golds_set.add((url, p))
    fin.close()

    predicts_set = set()
    fin = open("data/org.positive.predicts")
    for line in fin:
        url, s, p, o = line.strip().split("\t")
        predicts_set.add((url, p))
    fin.close()

    coverage = len(golds_set & predicts_set) / float(len(golds_set)) * 100

    print "%d / %d = %.2f%%" % (len(golds_set & predicts_set), len(golds_set), coverage)


if __name__ == '__main__':
    cover_1()
    cover_2()




