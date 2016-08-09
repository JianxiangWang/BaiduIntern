# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# 提取后的SPO中,
def main(fin):
    url_set = set()
    spo_set = set()
    dict_p_to_spo_set = {}

    for line in fin:
        line_list = line.strip().split("\t")
        url, s, p, o = line_list[0], line_list[1], line_list[2], line_list[3]

        url_set.add(url)
        spo_set.add((s, p, o))

        if p not in dict_p_to_spo_set:
            dict_p_to_spo_set[p] = set()
        dict_p_to_spo_set[p].add((s, p, o))

    print "url 数量: %d" % len(url_set)
    print "spo 数量: %d" % len(spo_set)
    print "==" * 40
    print "P: 数量"
    for p in dict_p_to_spo_set:
        print "%s: %d" % (p, len(dict_p_to_spo_set[p]))


if __name__ == '__main__':
    main(sys.stdin)

