#!/bin/env python
# -*- coding: utf-8 -*- 

import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')

total_num = 0
sentence_dict = {}
with open(sys.argv[1]) as in_file:
    for line in in_file:
        line = line.decode('utf-8').rstrip('\r\n')
        field = line.split('\t')
        predicate = field[3]
        s_info = json.loads(field[4])
        o_info = json.loads(field[5])
        sentence = field[6]
        label = unicode(int(float(field[8])))
        if field[9] == u'S识别':
            total_num += 1
            if sentence not in sentence_dict:
                sentence_dict[sentence] = set( )
            key = predicate + '\t' + '\t'.join(map(unicode, s_info))
            sentence_dict[sentence].add(key)

not_solve_num = 0
for line in sys.stdin:
    line = line.decode('utf-8').rstrip('\r\n')
    field = line.split('\t')
    sentence_info = json.loads(field[0])
    sentence = sentence_info['sentence']
    not_solve_flag = False
    if sentence in sentence_dict:
        for predicate in sentence_info['mars_ner']:
            for subject_info in sentence_info['mars_ner'][predicate]['s']:
                key = predicate + '\t' + '\t'.join(map(unicode, subject_info))
                if key in sentence_dict[sentence]:
                    not_solve_flag = True
                    break
    if not_solve_flag:
        not_solve_num += 1
        print line
print '%d, %d' % (not_solve_num, total_num)

