#!/bin/env python
# -*- coding: utf-8 -*- 

import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')

for line in sys.stdin:
    line = line.decode('utf-8').rstrip('\r\n')
    field = line.split('\t')
    sentence = field[6]
    url = field[7]
    pub_time = field[8]
    link_time = field[9]
    p_list = field[10]
    print '\t'.join([sentence, url, pub_time, link_time, p_list])

