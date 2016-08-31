# encoding: utf-8
import sys
import bs4
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib2
from bs4 import BeautifulSoup



def main(url, s, p, o):

    s_annotate = ""
    o_annotate = ""

    # try:
    #     s_nodes = get_nodes_in_url(url, s)
    #     o_nodes = get_nodes_in_url(url, o)
    #     if s_nodes:
    #         s_annotate = str(s_nodes[0])
    #     if o_nodes:
    #         o_annotate = "<SEG>".join(map(str, o_nodes))
    # except:
    #
    # print "%s\t%s\t%s\t%s\t%s\t%s" % (url, s, p, o, s_annotate, o_annotate)


def get_nodes_in_url(url, name_list):


    page = urllib2.urlopen(url)
    contents = page.read()
    soup = BeautifulSoup(contents, "lxml")

    res = []
    for tag in soup.body.descendants:
        if tag.name in ["script"]:
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
                            res.append(tag.parent)
                            break
                        elif res[-1] != tag.parent:
                            res.append(tag.parent)
                            break
                    else:
                        if res == []:
                            res.append(tag)
                            break
                        elif res[-1] != tag:
                            res.append(tag)
                            break
    return res


if __name__ == '__main__':

    for line in sys.stdin:
        line_list = line.strip().split("\t")
        url, s, p, o = line_list[0], line_list[1], line_list[2], line_list[3]
        main(url, s, p, o)