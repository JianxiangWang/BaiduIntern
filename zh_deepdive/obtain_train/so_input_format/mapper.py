#!/usr/bin/env python2.7
# coding: utf-8
import re
import sys
from subprocess import Popen, PIPE

reload(sys)
sys.setdefaultencoding('utf-8')
import json

fin = open("train_P.txt")
P_list = [line.strip() for line in fin]
fin.close()

def read_input(file):
    for line in file:
        yield line.strip().decode(encoding="gb18030", errors="ignore")

def main(separator='\t'):
    data = read_input(sys.stdin)

    for line in data:
        url = None
        title = None
        content = None
        publishTime = None
        linkFoundTime = None
        for item in line.split("\t"):
            if item.startswith("URL:"):
                url = item[4:]
            if item.startswith("REALTITLE:"):
                title = item[10:]
            if item.startswith("MAINCONT:"):
                content = item[9:]
            if item.startswith("PUBLISTHTIME:"):
                publishTime = item[13:]
            if item.startswith("LINKFOUNDTIME:"):
                linkFoundTime = item[14:]

        if url and title and content:

            # 分句
            sentCuter = u"[.|。|?|？|!|！]"
            cont = content + u"。" + title
            cont = cont.replace(u"\x01", u"。").replace(u"_", u"。").replace(u"_", u"。")
            sentList = re.split(sentCuter, cont)
            # 只保留词数>=5的句子
            sentList = [sent for sent in sentList if len(sent) >= 5]

            # 句子  \t url  \t publishTime  \t linkFoundTime \t depparser \t P_list
            for sent in sentList:
                print "%s\t%s\t%s\t%s\t%s\t%s" % (sent.strip(), url, publishTime, linkFoundTime, "[]", "[%s]" % ",".join(['"%s"' % x for x in P_list]))





if __name__ == '__main__':
    main()
