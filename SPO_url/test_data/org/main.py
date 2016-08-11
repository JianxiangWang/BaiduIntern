# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import random


def ba():

    with open("../../data/org") as fin, open("ba.test.data", "w") as fout:

        pos = []
        neg = []

        for line in fin:
            line_list = line.strip().split("\t")
            query = line_list[0]
            url   = line_list[1]
            label = line_list[2]

            if query.endswith("吧") and "fakeurl" not in url:
                x = "%s\t%s\t%s" % ("吧", url, label)
                if label == "1":
                    pos.append(x)
                if label == "0":
                    neg.append(x)

        pos = random.sample(pos, 50)
        neg = random.sample(neg, 50)

        fout.write("\n".join(pos) + "\n")
        fout.write("\n".join(neg) + "\n")

if __name__ == '__main__':
    ba()
