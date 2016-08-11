# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import random


def main(end_words, p, to_file):

    print "=> %s" % p

    with open("../../data/org") as fin, open(to_file, "w") as fout:

        pos = []
        neg = []

        for line in fin:
            line_list = line.strip().split("\t")
            query = line_list[0]
            url   = line_list[1]
            label = line_list[2]

            if query.endswith(end_words) and "fakeurl" not in url:
                x = "%s\t%s\t%s" % (p, url, label)
                if label == "1":
                    pos.append(x)
                if label == "0":
                    neg.append(x)
        if len(pos) > 60:
            pos = random.sample(pos, 60)
        if len(neg) > 60:

            neg = random.sample(neg, 60)

        fout.write("\n".join(pos) + "\n")
        fout.write("\n".join(neg) + "\n")

if __name__ == '__main__':
    # main("吧", "吧", "ba.test.data")
    # main("视频", "视频", "shipin.test.data")
    # main("小说", "小说", "xiaoshuo.test.data")
    # main("下载", "下载", "xiazai.test.data")
    # main("歌曲", "音频", "yinpin.test.data")
    # main("评测", "评测", "pingce.test.data")
    # main("简介", "简介", "jianjie.test.data")
    # main("个人资料", "个人资料", "gerenziliao.test.data")
    # main("百科", "百科", "baike.test.data")
    # main("微博", "微博", "weibo.test.data")
    main("商品", "商品", "shangpin.test.data")
