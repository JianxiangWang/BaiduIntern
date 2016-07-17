# coding: utf-8
import pprint
import json
import sys
import codecs

import pypinyin

reload(sys)
sys.setdefaultencoding('utf-8')



s = [1, 3,  5]

t = set([1, 4])

print t.intersection(s)