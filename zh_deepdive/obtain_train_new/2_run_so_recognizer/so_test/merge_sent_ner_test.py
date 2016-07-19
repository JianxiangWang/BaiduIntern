#!/bin/env python
# -*- coding: utf-8 -*-

import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')

#ner结果
sent_dict = {}
with open(sys.argv[1]) as in_file:
    line_count = 0
    for line in in_file:
        line_count += 1
        line = line.decode('utf-8').rstrip('\r\n')
        field = line.split('\t')
        ner_result = field
        sent_dict[line_count] = ner_result

#种子spo和句子
with open(sys.argv[2]) as in_file:
    line_count = 0
    for line in in_file:
        line_count += 1
        line = line.decode('utf-8').rstrip('\r\n')
        field = line.split('\t')
        out_info = {}
        out_info['sentence'] = field[0]
        out_info['url'] = field[1]
        out_info['publishTime'] = field[2]
        out_info['linkFoundTime'] = field[3]
        out_info['depparser'] = json.loads(field[4])
        out_info['domain'] = json.loads(field[5])
        out_info['ner'] = sent_dict[line_count]
        print json.dumps(out_info, ensure_ascii = False)

