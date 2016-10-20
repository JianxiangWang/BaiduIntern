#!python/bin/python
#encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json

# ba
def is_ba_domain(url):
    if "tieba.baidu.com" in url:
        return True
    return False

# weibo
def is_weibo_domain(url):
    if "weibo.com" in url:
        return True
    return False

# baike
def is_baike_domain(url):
    s = [
        'baike.baidu.com/item',
        'baike.baidu.com/view',
        'baike.baidu.com/subview',
        'baike.baidu.com/album',
        'wapbaike.baidu.com/item',
        'wapbaike.baidu.com/view',
        'wapbaike.baidu.com/subview',
        'm.baike.so.com/doc',
        'baike.so.com/doc',
        'www.baike.com/wiki',
        'baike.sogou.com'
    ]
    for x in s:
        if x in url:
            return True
    return False


for line in sys.stdin:
    line_list = line.strip().split("\t")

    url = unicode(line_list[0].strip(), errors="ignore")

    if is_ba_domain(url):
        print "%s\t1" % ("ba")

    if is_weibo_domain(url):
        print "%s\t1" % ("weibo")

    if is_baike_domain(url):
        print "%s\t1" % ("baike")











