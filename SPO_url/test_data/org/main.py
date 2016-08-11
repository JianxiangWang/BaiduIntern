# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import random


def main(p, to_file):

    print "=> %s" % p

    with open("../../data/org") as fin, open(to_file, "w") as fout:

        pos = []
        neg = []

        for line in fin:
            line_list = line.strip().split("\t")
            query = line_list[0]
            url   = line_list[1]
            label = line_list[2]

            if query.endswith(p) and "fakeurl" not in url:
                x = "%s\t%s\t%s" % (p, url, label)
                if label == "1":
                    pos.append(x)
                if label == "0":
                    neg.append(x)

        pos = random.sample(pos, 60)
        neg = random.sample(neg, 60)

        fout.write("\n".join(pos) + "\n")
        fout.write("\n".join(neg) + "\n")

if __name__ == '__main__':
    # main("吧", "ba.test.data")
    main("视频", "shipin.test.data")
    # main("小说", "xiaoshuo.test.data")
    # main("下载", "xiazai.test.data")
    # main("音频", "音频.test.data")
