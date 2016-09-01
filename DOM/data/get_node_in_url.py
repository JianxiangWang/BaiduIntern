# encoding: utf-8
import sys

import bs4

reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2
from bs4 import BeautifulSoup


def main(url, name_list, want_common_node=False):

    page = urllib2.urlopen(url)
    contents = page.read()
    soup = BeautifulSoup(contents, "lxml")
    if soup is None:
        soup = BeautifulSoup(contents.decode("gb18030"), "lxml")


    res = []
    for tag in soup.body.descendants:
        if tag.name == "script":
            continue
        if tag.string:
            for name in name_list:
                if unicode(name) in tag.string:
                    flag = 0
                    if not isinstance(tag, bs4.element.NavigableString):
                        for child in tag.children:
                            if unicode(name) in child.string:
                                flag = 1
                    if flag == 1:
                        continue
                    if tag.name is None:
                        if res == []:
                            if tag.parent.name != "script":
                                res.append(tag.parent)
                                break
                        elif res[-1] != tag.parent:
                            if tag.parent.name != "script":
                                res.append(tag.parent)
                                break
                    else:
                        if res == []:
                            res.append(tag)
                            break
                        elif res[-1] != tag:
                            res.append(tag)
                            break

    for tag in res:
        print tag

    if want_common_node:
        print
        print "===" * 30
        print "####" * 40
        s = str(lowest_common_node(res))
        print s.strip()
        print len(res)
        print "####" * 40
        print "".join([x.strip() for x in s.strip().split("\n")])


def lowest_common_node(nodes):
    parents_list = []
    min_length = None
    for node in nodes:
        parents = list(node.parents)[::-1] + [node]

        if min_length is None:
            min_length = len(parents)
        else:
            if len(parents) < min_length:
                min_length = len(parents)
        parents_list.append(parents)

    common_node = None
    for i in range(min_length):
        if len(set([parents[i] for parents in parents_list])) == 1:
            common_node = parents_list[0][i]
        else:
            break

    return common_node




if __name__ == '__main__':

    # url = sys.argv[1]
    # name_str = sys.argv[2]

    # url = 'http://zhidao.baidu.com/question/753612773777598844.html'
    # name_str = "张氏"
    # main(url, name_str.split(","))

    url, s, p, o = \
        "http://www.iqiyi.com/lib/m_204780514.html	校园大人物	综艺节目_主持人	钟昀呈,陈汉典,蔡小洁"\
            .split("\t")

    print "url: %s" % (url)
    print "==> s -------------------------------"
    main(url, s.split(","), want_common_node=False)
    print "\n==> o -------------------------------"
    main(url, o.split(","), want_common_node=True)
    print "\n\nurl: %s" % (url)


