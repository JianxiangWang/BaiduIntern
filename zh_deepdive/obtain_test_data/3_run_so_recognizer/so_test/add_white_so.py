#!/bin/env python
# -*- coding: utf-8 -*- 

import sys
import json

def add_entity(sentence, entity_name, entity_type, dest_list):
    dest_set = set( )
    for item in dest_list:
        dest_set.add('\t'.join([item[0], item[1], unicode(item[2]), unicode(item[3])]))
    entity_len = len(entity_name)
    beg_pos = 0
    while True:
        entity_pos = sentence.find(entity_name, beg_pos)
        if entity_pos == -1:
            break
        key = '\t'.join([entity_name, entity_type, unicode(entity_pos), unicode(entity_len)])
        if key not in dest_set:
            dest_list.append([entity_name, entity_type, entity_pos, entity_len])
            dest_set.add(key)
        beg_pos = entity_pos + entity_len
    return

reload(sys)
sys.setdefaultencoding('utf-8')

p_type_dict = {}
#o_prop
with open(sys.argv[1]) as in_file:
    for line in in_file:
        line = line.decode('utf-8').rstrip('\r\n')
        field = line.split('\t')
        domain = field[1]
        domain_property = domain + '_' + field[2]
        o_type = field[3]
        p_type_dict[domain_property] = {}
        p_type_dict[domain_property]['o'] = o_type.split(',')

#s_prop
with open(sys.argv[2]) as in_file:
    for line in in_file:
        line = line.decode('utf-8').rstrip('\r\n')
        field = line.split('\t')
        domain = field[0]
        s_type = field[1]
        for key in p_type_dict:
            if key.startswith(domain + '_'):
                p_type_dict[key]['s'] = s_type.split(',')

white_dict = {}
#white_sent
with open(sys.argv[3]) as in_file:
    for line in in_file:
        line = line.decode('utf-8').rstrip('\r\n')
        field = line.split('\t')
        sentence = field[0]
        url = field[1]
        spo_list = json.loads(field[2])
        white_dict[sentence] = {}
        for spo in spo_list:
            try:
                subject, domain_predicate, object = spo.split('-')
            except:
                print >> sys.stderr, line
                exit(-1)
            if domain_predicate not in white_dict[sentence]:
                white_dict[sentence][domain_predicate] = {}
            if 's' not in white_dict[sentence][domain_predicate]:
                white_dict[sentence][domain_predicate]['s'] = []
            white_dict[sentence][domain_predicate]['s'].append(subject)
            if 'o' not in white_dict[sentence][domain_predicate]:
                white_dict[sentence][domain_predicate]['o'] = []
            white_dict[sentence][domain_predicate]['o'].append(object)
#print json.dumps(white_dict, ensure_ascii = False)

for line in sys.stdin:
    line = line.decode('utf-8').rstrip('\r\n')
    field = line.split('\t')
    sentence_info = json.loads(field[0])
    sentence = sentence_info['sentence']
    if sentence in white_dict:
        for domain_predicate in white_dict[sentence]:
            if domain_predicate not in p_type_dict:
                continue
            if domain_predicate not in sentence_info['mars_ner']:
                sentence_info['mars_ner'][domain_predicate] = {}
                sentence_info['mars_ner'][domain_predicate]['s'] = []
                sentence_info['mars_ner'][domain_predicate]['o'] = []
            for subject in white_dict[sentence][domain_predicate]['s']:
                subject_type = p_type_dict[domain_predicate]['s'][0]
                add_entity(sentence, subject, subject_type, sentence_info['mars_ner'][domain_predicate]['s'])
            for object in white_dict[sentence][domain_predicate]['o']:
                object_type = p_type_dict[domain_predicate]['o'][0]
                add_entity(sentence, object, object_type, sentence_info['mars_ner'][domain_predicate]['o'])
    print json.dumps(sentence_info, ensure_ascii = False)

