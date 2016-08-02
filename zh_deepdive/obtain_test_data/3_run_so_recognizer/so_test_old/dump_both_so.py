#!/bin/env python
# -*- coding: utf -*-

import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')

for line in sys.stdin:
    line = line.decode('utf-8').rstrip('\r\n')
    field = line.split('\t')
    sentence_info = json.loads(field[0])
    for predicate in sentence_info['mars_ner']:
        if len(sentence_info['mars_ner'][predicate]['s']) and \
                len(sentence_info['mars_ner'][predicate]['o']):
            print predicate

