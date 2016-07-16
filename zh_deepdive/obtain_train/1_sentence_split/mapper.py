#!/usr/bin/env python2.7
# coding: utf-8
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import uuid


def read_input(file):
    for line in file:
        yield line.strip().decode(encoding="gb18030", errors="ignore")

def main():
    data = read_input(sys.stdin)

    for line in data:
        doc_id = uuid.uuid1()
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

            for index, sent in enumerate(sentList):
                # 句子, index, url, publishTime, linkFoundTime, title, doc_id

                s = "%s\t%d\t%s\t%s\t%s\t%s\t%s" % \
                      (sent, index, url, publishTime, linkFoundTime, title, doc_id)

                print s



if __name__ == '__main__':
    main()



