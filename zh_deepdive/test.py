# coding: utf-8
import pprint
import json
import sys
import codecs

import pypinyin

reload(sys)
sys.setdefaultencoding('utf-8')

def A():

    for i in range(10):
        if i == 3:
            yield i
            break


for x in A():
    print x