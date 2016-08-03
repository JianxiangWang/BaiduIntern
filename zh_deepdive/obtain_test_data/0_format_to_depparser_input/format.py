
# coding: utf-8
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import uuid

# 句子  \t url  \t publishTime  \t linkFoundTime
def format(in_file, to_file):

    with open(in_file) as fin, open(to_file, "w") as fout:

        for line in fin:
            line_list = line.strip().split("\t")
            sent, url = line_list[0], line_list[1]
            fout.write("%s\t%s\tpublishTime\tlinkFoundTime\n" % (sent, url))

if __name__ == '__main__':
    # format("sent_all_SPO.format.res.all", "test_500_sents")
    format("all_sent_all_SPO.format.res.all", "test.new_sents")