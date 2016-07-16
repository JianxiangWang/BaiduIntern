#!tools/python/bin/python
# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


fin = open("train_P.txt")
P_list = [line.strip() for line in fin]
P_list_str = "[%s]" % ",".join(map(lambda x: '"%s"' % x, P_list))
fin.close()

# 句子  \t url  \t publishTime  \t linkFoundTime \t depparser \t P_list
def main():

    for line in sys.stdin:
        line = line.strip()
        sent, index, url, publishTime, linkFoundTime, title, doc_id,_, depparser_makeup = line.split("\t")

        print "%s\t%s\t%s\t%s\t%s\t%s" % (sent.strip(), url, publishTime, linkFoundTime, depparser_makeup, P_list_str)


if __name__ == '__main__':
    main()